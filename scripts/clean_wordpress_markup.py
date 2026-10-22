#!/usr/bin/env python3
"""Rewrite WordPress markup in content/posts/ to Bulma classes.

The mapping and the reasoning behind it live in ``wp_to_bulma``. This is just the
driver: it walks the post files, applies the transform and writes the result.

Only ``content/posts/`` is touched. Everything else under ``content/`` (the
funder pages, the author pages, the section indexes) is already clean, so there
is nothing to do there and no reason to risk it.

Usage:

    python3 scripts/clean_wordpress_markup.py            # dry run, show a summary
    python3 scripts/clean_wordpress_markup.py --diff     # dry run, show the diff
    python3 scripts/clean_wordpress_markup.py --write    # apply the changes
    python3 scripts/clean_wordpress_markup.py --check    # exit 1 if anything would change

The bare invocation never writes, so a mistyped command cannot mutate content.
``--check`` is the CI mode: it fails the build if a re-import has reintroduced
WordPress markup.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import wp_to_bulma  # noqa: E402

POSTS_DIR = Path(__file__).resolve().parent.parent / "content" / "posts"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="apply the changes in place")
    mode.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if any file would change, without writing (for CI)",
    )
    parser.add_argument("--diff", action="store_true", help="print a unified diff")
    parser.add_argument(
        "--posts-dir",
        type=Path,
        default=POSTS_DIR,
        help="directory of post markdown files (default: content/posts)",
    )
    args = parser.parse_args()

    files = sorted(args.posts_dir.glob("*.md"))
    if not files:
        print(f"No markdown files found in {args.posts_dir}", file=sys.stderr)
        return 1

    changed: list[Path] = []
    skipped: list[Path] = []

    for path in files:
        if path.name in wp_to_bulma.HAND_CONVERTED:
            skipped.append(path)
            continue

        original = path.read_text(encoding="utf-8")
        try:
            result = wp_to_bulma.transform_markdown_file(original)
        except AssertionError as exc:
            print(f"ERROR {path.name}: {exc}", file=sys.stderr)
            return 1

        if result == original:
            continue

        changed.append(path)

        if args.diff:
            sys.stdout.writelines(
                difflib.unified_diff(
                    original.splitlines(keepends=True),
                    result.splitlines(keepends=True),
                    fromfile=f"a/{path.as_posix()}",
                    tofile=f"b/{path.as_posix()}",
                )
            )

        if args.write:
            path.write_text(result, encoding="utf-8")

    # --- report ------------------------------------------------------------

    for path in skipped:
        print(f"skipped (hand converted): {path.name}")

    if args.check:
        if changed:
            print(
                f"\n{len(changed)} file(s) still contain WordPress markup. "
                f"Run: make clean-wp-markup",
                file=sys.stderr,
            )
            for path in changed:
                print(f"  {path.as_posix()}", file=sys.stderr)
            return 1
        print(f"\nAll {len(files) - len(skipped)} posts are clean.")
        return 0

    verb = "rewrote" if args.write else "would rewrite"
    print(f"\n{verb} {len(changed)} of {len(files)} posts ({len(skipped)} hand converted)")
    if not args.write and changed:
        print("Nothing was written. Re-run with --write to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
