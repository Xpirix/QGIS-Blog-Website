#!/usr/bin/env python3
"""
WordPress WXR to Hugo Markdown importer for blog.qgis.org

Usage:
    python scripts/import_wordpress.py <wordpress-export.xml> [options]

Options:
    --output-dir DIR     Content directory for posts (default: content/posts)
    --download-images    Download images from wp-content/uploads to static/
                         and rewrite image URLs in post content.
    --dry-run            Show what would be created without writing any files.
    --overwrite          Overwrite existing post files (default: skip).
"""

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# WordPress WXR namespaces
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc":      "http://purl.org/dc/elements/1.1/",
    "wp":      "http://wordpress.org/export/1.2/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}

# WordPress also exports with 1.1 namespace in some versions
NS_ALT = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc":      "http://purl.org/dc/elements/1.1/",
    "wp":      "http://wordpress.org/export/1.1/",
    "excerpt": "http://wordpress.org/export/1.1/excerpt/",
}


def detect_ns(root: ET.Element) -> dict:
    """Detect the correct WXR namespace version from the root element."""
    channel = root.find("channel")
    if channel is None:
        return NS
    # Try to find a wp:post_type element to confirm namespace
    for ns in (NS, NS_ALT):
        if channel.find(".//wp:post_type", ns) is not None:
            return ns
    return NS


def parse_date(date_str: str) -> datetime | None:
    """Parse a WordPress post date string into a datetime object."""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def escape_yaml_string(s: str) -> str:
    """Wrap a string in YAML double-quotes, escaping internal quotes."""
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def build_front_matter(
    title: str,
    date: datetime,
    author_slug: str,
    categories: list,
    tags: list,
    draft: bool = False,
) -> str:
    """Build Hugo YAML front matter block."""
    lines = ["---"]
    lines.append(f"title: {escape_yaml_string(title)}")
    lines.append(f'date: "{date.strftime("%Y-%m-%dT%H:%M:%S+00:00")}"')
    lines.append(f"draft: {'true' if draft else 'false'}")
    if author_slug:
        lines.append(f'authors: ["{author_slug}"]')
    if categories:
        cat_list = ", ".join(escape_yaml_string(c) for c in categories)
        lines.append(f"categories: [{cat_list}]")
    if tags:
        tag_list = ", ".join(escape_yaml_string(t) for t in tags)
        lines.append(f"tags: [{tag_list}]")
    lines.append("---")
    return "\n".join(lines)


def rewrite_image_urls(content: str, static_dir: Path) -> str:
    """
    Download images from blog.qgis.org/wp-content/uploads and rewrite
    their URLs in the HTML content to point to local static paths.
    Requires the `requests` package.
    """
    try:
        import requests
    except ImportError:
        print("  WARNING: `requests` not installed; skipping image downloads.", file=sys.stderr)
        print("  Install with: pip install requests", file=sys.stderr)
        return content

    img_url_pattern = re.compile(
        r'(https?://blog\.qgis\.org/(wp-content/uploads/[^\s"\'<>?]+)(?:\?[^\s"\'<>]*)?)'
    )
    seen: dict = {}

    def download_and_replace(match: re.Match) -> str:
        full_url = match.group(1)
        rel_path = match.group(2)  # wp-content/uploads/YYYY/MM/filename.ext

        if full_url in seen:
            return seen[full_url]

        local_path = static_dir / rel_path
        if not local_path.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                response = requests.get(full_url, timeout=20)
                response.raise_for_status()
                local_path.write_bytes(response.content)
                print(f"    Downloaded: {rel_path}")
            except Exception as exc:
                print(f"    WARNING: Could not download {full_url}: {exc}", file=sys.stderr)
                seen[full_url] = full_url
                return full_url

        local_url = f"/{rel_path}"
        seen[full_url] = local_url
        return local_url

    return img_url_pattern.sub(download_and_replace, content)


def import_wxr(
    wxr_path: str,
    output_dir: str = "content/posts",
    download_images: bool = False,
    dry_run: bool = False,
    overwrite: bool = False,
) -> None:
    """Parse a WordPress WXR export file and create Hugo Markdown files."""
    wxr_file = Path(wxr_path)
    if not wxr_file.exists():
        print(f"ERROR: File not found: {wxr_path}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(output_dir)
    static_dir = Path("static") if download_images else None

    print(f"Parsing {wxr_file} ...")
    tree = ET.parse(wxr_file)
    root = tree.getroot()
    ns = detect_ns(root)

    channel = root.find("channel")
    if channel is None:
        print("ERROR: No <channel> element found in WXR file.", file=sys.stderr)
        sys.exit(1)

    # Collect author display names from <wp:author> elements
    author_names: dict = {}
    for author_el in channel.findall("wp:author", ns):
        login = (author_el.findtext("wp:author_login", namespaces=ns) or "").strip()
        display = (author_el.findtext("wp:author_display_name", namespaces=ns) or login).strip()
        if login:
            author_names[login] = display

    stats = {"total": 0, "imported": 0, "skipped": 0, "errors": 0}
    categories_seen: set = set()
    tags_seen: set = set()
    authors_seen: set = set()

    for item in channel.findall("item"):
        post_type = (item.findtext("wp:post_type", namespaces=ns) or "").strip()
        status = (item.findtext("wp:status", namespaces=ns) or "").strip()

        # Only import published posts (not pages, attachments, nav menus, etc.)
        if post_type != "post":
            continue

        stats["total"] += 1

        if status != "publish":
            print(f"  SKIP (status={status}): {item.findtext('title', '')}")
            stats["skipped"] += 1
            continue

        # --- Extract fields ---
        title = (item.findtext("title") or "").strip()
        post_name = (item.findtext("wp:post_name", namespaces=ns) or "").strip()
        post_date_str = (item.findtext("wp:post_date", namespaces=ns) or "").strip()
        author_slug = (item.findtext("dc:creator", namespaces=ns) or "").strip()
        content_encoded = (item.findtext("content:encoded", namespaces=ns) or "").strip()

        # Fall back to slugified title if post_name is empty
        if not post_name:
            post_name = slugify(title) if title else f"post-{stats['total']}"

        post_date = parse_date(post_date_str)
        if post_date is None:
            print(f"  WARNING: Unparseable date '{post_date_str}' for '{title}' — skipping.")
            stats["skipped"] += 1
            continue

        # --- Parse categories and tags ---
        # WordPress uses <category domain="category"> for categories
        # and <category domain="post_tag"> for tags
        post_categories: list = []
        post_tags: list = []
        for cat_el in item.findall("category"):
            domain = cat_el.get("domain", "category")
            value = (cat_el.text or "").strip()
            if not value:
                continue
            if domain == "post_tag":
                post_tags.append(value)
                tags_seen.add(value)
            else:
                post_categories.append(value)
                categories_seen.add(value)

        if author_slug:
            authors_seen.add(author_slug)

        # --- Process content ---
        content = content_encoded
        if static_dir is not None:
            content = rewrite_image_urls(content, static_dir)

        # --- Build output ---
        filename = f"{post_name}.md"
        out_file = out_dir / filename

        fm = build_front_matter(
            title=title,
            date=post_date,
            author_slug=author_slug,
            categories=post_categories,
            tags=post_tags,
        )
        file_content = f"{fm}\n\n{content}\n"

        if dry_run:
            print(f"  [DRY RUN] {out_file}")
            print(f"    title:      {title}")
            print(f"    date:       {post_date.strftime('%Y-%m-%d')}")
            print(f"    author:     {author_slug}")
            print(f"    categories: {post_categories}")
            print(f"    tags:       {post_tags}")
            stats["imported"] += 1
            continue

        out_dir.mkdir(parents=True, exist_ok=True)

        if out_file.exists() and not overwrite:
            print(f"  SKIP (exists): {out_file}")
            stats["skipped"] += 1
            continue

        try:
            out_file.write_text(file_content, encoding="utf-8")
            print(f"  Created: {out_file}")
            stats["imported"] += 1
        except OSError as exc:
            print(f"  ERROR writing {out_file}: {exc}", file=sys.stderr)
            stats["errors"] += 1

    # --- Summary ---
    print()
    print("=" * 60)
    print("Import complete!")
    print(f"  Total posts (published + draft): {stats['total']}")
    print(f"  Imported:                        {stats['imported']}")
    print(f"  Skipped:                         {stats['skipped']}")
    print(f"  Errors:                          {stats['errors']}")
    print(f"  Unique authors:                  {len(authors_seen)}")
    print(f"  Unique categories:               {len(categories_seen)}")
    print(f"  Unique tags:                     {len(tags_seen)}")

    if authors_seen:
        print()
        print("Authors found — verify content/authors/<slug>/_index.md exists for each:")
        for slug in sorted(authors_seen):
            display = author_names.get(slug, "(display name not found)")
            exists = Path(f"content/authors/{slug}/_index.md").exists()
            status_icon = "✓" if exists else "✗ MISSING"
            print(f"  {status_icon}  {slug}  ({display})")

    if categories_seen:
        print()
        print(f"Categories ({len(categories_seen)}):")
        for cat in sorted(categories_seen):
            print(f"  - {cat}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import a WordPress WXR export into Hugo content/posts/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "wxr_file",
        help="Path to the WordPress WXR export XML file",
    )
    parser.add_argument(
        "--output-dir",
        default="content/posts",
        metavar="DIR",
        help="Output directory for Hugo posts (default: content/posts)",
    )
    parser.add_argument(
        "--download-images",
        action="store_true",
        help="Download images from wp-content/uploads into static/ and rewrite URLs",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be imported without writing any files",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing post files (default: skip existing)",
    )
    args = parser.parse_args()

    import_wxr(
        wxr_path=args.wxr_file,
        output_dir=args.output_dir,
        download_images=args.download_images,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
