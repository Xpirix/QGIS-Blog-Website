#!/usr/bin/env python3
"""
WordPress.com REST API importer for blog.qgis.org -> Hugo

Fetches all published posts from the WordPress.com REST API, downloads all
media (featured images + content images) to static/, and writes Hugo Markdown
files to content/posts/.

Usage:
    python scripts/import_wordpress.py [options]

Options:
    --site SITE          WordPress.com site slug or ID (default: blog.qgis.org)
    --output-dir DIR     Hugo content directory for posts (default: content/posts)
    --authors-dir DIR    Hugo content directory for author pages (default: content/authors)
    --static-dir DIR     Static files directory for downloaded images (default: static)
    --no-images          Skip downloading images (keep original URLs)
    --dry-run            Print what would be created without writing any files
    --overwrite          Overwrite existing post files (default: skip)
    --batch-size N       Posts per API request (default: 100, max: 100)
"""

import argparse
import html as html_module
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://public-api.wordpress.com/rest/v1.1/sites"

WP_MEDIA_HOSTS = re.compile(
    r"https?://(?:qgisblog\.wordpress\.com|qgisblog\.files\.wordpress\.com|blog\.qgis\.org)"
)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def fetch_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; hugo-importer/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download_file(url: str, dest: Path) -> bool:
    if dest.exists():
        return True
    clean_url = url.split("?")[0]
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(
            clean_url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; hugo-importer/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            dest.write_bytes(resp.read())
        print(f"    Downloaded: {dest}")
        return True
    except Exception as exc:
        print(f"    WARNING: Could not download {clean_url}: {exc}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Post fetching
# ---------------------------------------------------------------------------

def fetch_all_posts(site: str, batch_size: int = 100) -> list:
    posts = []
    offset = 0
    total = None
    while True:
        url = (
            f"{API_BASE}/{site}/posts"
            f"?number={batch_size}&offset={offset}"
            f"&status=publish&order_by=date&order=DESC"
        )
        print(f"  Fetching posts {offset + 1}-{offset + batch_size} ...")
        data = fetch_json(url)
        batch = data.get("posts", [])
        if total is None:
            total = data.get("found", 0)
            print(f"  Total posts on site: {total}")
        posts.extend(batch)
        print(f"  Fetched so far: {len(posts)}")
        if not batch or len(posts) >= total:
            break
        offset += batch_size
        time.sleep(0.3)
    return posts


# ---------------------------------------------------------------------------
# Image URL helpers
# ---------------------------------------------------------------------------

def wp_url_to_local_path(url: str):
    m = re.match(
        r"https?://(?:qgisblog\.wordpress\.com|qgisblog\.files\.wordpress\.com|blog\.qgis\.org)"
        r"/(wp-content/uploads/[^\s\"'<>?#]+)",
        url,
    )
    return m.group(1) if m else None


_seen_urls: dict = {}


def localise_url(url: str, static_dir: Path, download: bool) -> str:
    rel = wp_url_to_local_path(url)
    if rel is None:
        return url
    base = url.split("?")[0]
    if base not in _seen_urls:
        dest = static_dir / rel
        if download:
            download_file(url, dest)
        _seen_urls[base] = f"/{rel}"
    return _seen_urls[base]


def rewrite_content_images(content: str, static_dir: Path, download: bool) -> str:
    single_attr_pattern = re.compile(
        r'((?:src|href|data-orig-file|data-large-file|data-medium-file|data-permalink)=")'
        r"(https?://(?:qgisblog\.wordpress\.com|qgisblog\.files\.wordpress\.com|blog\.qgis\.org)"
        r"/wp-content/uploads/[^\"'<>?#]*(?:\?[^\"'<>]*)?)"
        r'(")',
    )

    def _replace_attr(m):
        return m.group(1) + localise_url(m.group(2), static_dir, download) + m.group(3)

    content = single_attr_pattern.sub(_replace_attr, content)

    srcset_pattern = re.compile(r'(srcset=")([^"]+)(")')

    def _replace_srcset(m):
        parts = []
        for part in m.group(2).split(","):
            part = part.strip()
            tokens = part.split(None, 1)
            if tokens and WP_MEDIA_HOSTS.match(tokens[0]):
                tokens[0] = localise_url(tokens[0], static_dir, download)
            parts.append(" ".join(tokens))
        return m.group(1) + ", ".join(parts) + m.group(3)

    content = srcset_pattern.sub(_replace_srcset, content)
    return content


# ---------------------------------------------------------------------------
# YAML / front-matter helpers
# ---------------------------------------------------------------------------

def escape_yaml(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def build_front_matter(
    title, date, author_slug, categories, tags, featured_image="", draft=False
):
    lines = ["---"]
    lines.append(f"title: {escape_yaml(title)}")
    lines.append(f'date: "{date}"')
    lines.append(f"draft: {'true' if draft else 'false'}")
    if author_slug:
        lines.append(f'authors: ["{author_slug}"]')
    if categories:
        lines.append("categories: [" + ", ".join(escape_yaml(c) for c in categories) + "]")
    if tags:
        lines.append("tags: [" + ", ".join(escape_yaml(t) for t in tags) + "]")
    if featured_image:
        lines.append(f"featured_image: {escape_yaml(featured_image)}")
    lines.append("---")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Author helpers
# ---------------------------------------------------------------------------

def ensure_author(slug, name, authors_dir, dry_run):
    author_file = authors_dir / slug / "_index.md"
    if author_file.exists():
        return
    print(f"  Creating author file: {author_file}")
    if dry_run:
        return
    author_file.parent.mkdir(parents=True, exist_ok=True)
    safe_name = name.replace('"', '\\"')
    author_file.write_text(
        f'---\ntitle: "{slug}"\ndisplay_name: "{safe_name}"\nbio: ""\n---\n',
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Main import routine
# ---------------------------------------------------------------------------

def import_from_api(
    site="blog.qgis.org",
    output_dir="content/posts",
    authors_dir="content/authors",
    static_dir="static",
    download_images=True,
    dry_run=False,
    overwrite=False,
    batch_size=100,
):
    out_dir = Path(output_dir)
    authors_path = Path(authors_dir)
    static_path = Path(static_dir)

    print(f"Fetching all posts from {site} ...")
    posts = fetch_all_posts(site, batch_size)
    print(f"\nTotal posts fetched: {len(posts)}\n")

    stats = {"total": len(posts), "imported": 0, "skipped": 0, "errors": 0}

    for post in posts:
        slug = post.get("slug", "").strip()
        title = html_module.unescape(post.get("title", "").strip())
        date = post.get("date", "").strip()

        author = post.get("author") or {}
        author_slug = author.get("login", "").strip()
        author_name = author.get("name", author_slug).strip()

        content = post.get("content", "").strip()

        categories = [v["name"] for v in (post.get("categories") or {}).values()]
        tags = [v["name"] for v in (post.get("tags") or {}).values()]

        post_thumbnail = post.get("post_thumbnail") or {}
        featured_image = (
            post_thumbnail.get("URL", "")
            or post.get("featured_image", "")
            or ""
        )

        if not slug:
            slug = re.sub(r"[^\w-]", "-", title.lower())[:80].strip("-") or f"post-{stats['total']}"

        local_featured = ""
        if download_images:
            content = rewrite_content_images(content, static_path, download=not dry_run)
            if featured_image:
                local_featured = localise_url(featured_image, static_path, download=not dry_run)
        else:
            local_featured = featured_image

        if author_slug and not dry_run:
            ensure_author(author_slug, author_name, authors_path, dry_run)

        fm = build_front_matter(
            title=title,
            date=date,
            author_slug=author_slug,
            categories=categories,
            tags=tags,
            featured_image=local_featured,
        )
        file_content = f"{fm}\n\n{content}\n"
        filename = f"{slug}.md"
        out_file = out_dir / filename

        if dry_run:
            print(f"  [DRY RUN] {out_file}")
            print(f"    title:         {title}")
            print(f"    date:          {date}")
            print(f"    author:        {author_slug}")
            print(f"    categories:    {categories}")
            print(f"    featured_img:  {local_featured or '(none)'}")
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

    print()
    print("=" * 60)
    print("Import complete!")
    print(f"  Total posts:  {stats['total']}")
    print(f"  Imported:     {stats['imported']}")
    print(f"  Skipped:      {stats['skipped']}")
    print(f"  Errors:       {stats['errors']}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Import blog.qgis.org posts via the WordPress.com REST API into Hugo.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--site", default="blog.qgis.org")
    parser.add_argument("--output-dir", default="content/posts", metavar="DIR")
    parser.add_argument("--authors-dir", default="content/authors", metavar="DIR")
    parser.add_argument("--static-dir", default="static", metavar="DIR")
    parser.add_argument("--no-images", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--batch-size", type=int, default=100, metavar="N")
    args = parser.parse_args()

    import_from_api(
        site=args.site,
        output_dir=args.output_dir,
        authors_dir=args.authors_dir,
        static_dir=args.static_dir,
        download_images=not args.no_images,
        dry_run=args.dry_run,
        overwrite=args.overwrite,
        batch_size=min(args.batch_size, 100),
    )


if __name__ == "__main__":
    main()
