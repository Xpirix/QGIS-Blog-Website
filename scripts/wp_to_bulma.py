#!/usr/bin/env python3
"""Translate WordPress markup in imported blog posts into Bulma classes.

Why this exists
---------------
``import_wordpress.py`` writes WordPress rendered HTML into ``content/posts/*.md``
verbatim. No stylesheet in this repo or in the theme styles a single WordPress
class, so every ``wp-block-*``, ``alignnone``, ``size-large`` and ``wp-caption``
is inert: the layout intent is silently dropped and posts render unstyled.

The post body is already wrapped in Bulma's ``.content``
(``layouts/partials/post-details.html``), and Bulma's ``.content`` styles ``p``,
``ul``, ``ol``, ``blockquote``, ``pre``, ``table`` and ``h1``-``h6`` natively. So
for most blocks, *removing* the dead class is the complete fix. Only tables,
embeds, buttons and alignment need a Bulma class added.

The governing principle
-----------------------
Because no stylesheet styles any WordPress class today, **removing a class can
never change rendering, but adding one can.** A class is therefore only added
where we deliberately decided to improve something. A WordPress class is never
mapped to a "Bulma equivalent" as a reflex. This is why the WordPress palette
classes (``has-vivid-cyan-blue-color`` and friends) and the WordPress font size
classes are removed rather than mapped: they render as plain default text today,
so mapping them would newly colour and resize text that is currently untouched.

Corollary, and an invariant the tests enforce: **every class we add is gated on a
WordPress token that the same pass removes.** That is what makes the transform
idempotent.

The golden rule
---------------
Page and media link structures must survive unchanged.

* Page permalinks come from the front matter ``date`` plus the filename
  (``config.toml``: ``posts = "/:year/:month/:day/:slug/"``). This module never
  touches front matter and never renames a file.
* ``post-details.html`` rewrites media paths at render time with
  ``replaceRE `(["\\s,])/wp-content/` ...``, which needs a quote, whitespace or
  comma immediately before ``/wp-content/``. So attribute quoting is never
  reformatted, and a deleted attribute is removed together with its leading
  whitespace.
* ``src``, ``href`` and ``srcset`` values stay byte-identical, including the
  entity-escaped ampersands (``&#038;``) in legacy YouTube iframe URLs.

How it avoids collateral damage
-------------------------------
This is a *tokenizer*, not a tree builder. ``html.parser.HTMLParser`` is used
only to find where each start tag begins and ends; ``get_starttag_text()`` then
gives the exact original bytes of that tag. We record edit spans and splice them
into the original string. Only ``class``, ``style`` and dead ``data-*``
attributes are ever rewritten; every other attribute is never regenerated, so its
bytes survive by construction.

Two consequences worth stating:

* There is **no entity policy**, because no entity is ever re-encoded.
* The 7 posts that illegally nest ``<div class="wp-caption">`` inside a ``<p>``
  keep that exact (invalid) structure. A tree builder would hoist the div out of
  the paragraph. Browsers already apply their own fix-up today and will continue
  to apply the identical fix-up afterwards, so rendering is unchanged. Not
  restructuring is the *default* here rather than something we must defend.

Deliberately out of scope
-------------------------
Classes pasted in from Gmail, GitHub and Sphinx (``reference``, ``external``,
``gmail_default``, ``task-list-item``, ``position-relative``, ``issue-link``,
``moz-txt-link-freetext``, ``Apple-converted-space``, ``glightbox`` ...) are left
alone. They are not WordPress, they are inert for the same reason, and removing
them would add hundreds of edits of pure diff noise without changing rendering.
Please do not "finish the job" later without a reason to.

Also out of scope: converting the HTML to Markdown syntax. That would re-route
every link through the theme's ``render-link.html`` hook, which injects
``target="_blank" rel="noopener" class="external-link"`` and so would change the
rendered output of all ~2100 links.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# Files converted by hand, never by this module
# ---------------------------------------------------------------------------

# Three gallery/slideshow posts. These are nested row/group/tile div grids with
# schema.org microdata and pixel-perfect inline widths; converting them to Bulma
# columns is genuine restructuring, not a class rewrite.
#
# They are also load-bearing for the golden rule. Eight full-size originals are
# reachable *only* through a data-orig-file / data-large-file attribute and
# appear in no src, href or srcset anywhere in the corpus. Stripping those
# attributes here would make those eight assets unreachable. All eight live in
# the two tiled-gallery files below, so the rule holds *because* of this list.
# assert_no_orphaned_media() enforces the coupling rather than trusting it.
HAND_CONVERTED = frozenset(
    {
        "new-qgis-3-0-logo-candidate.md",
        "report-back-on-the-20th-qgis-hackfest-in-zanzibar.md",
        # Jetpack slideshow. The JS was never ported, so this page currently
        # renders only its "This slideshow requires JavaScript." fallback, i.e.
        # it is already broken live. Hand conversion fixes it.
        "report-back-on-the-3rd-qgis-conference-in-nodebo-denmark.md",
    }
)

# ---------------------------------------------------------------------------
# Class mapping
# ---------------------------------------------------------------------------

# Tokens removed everywhere, regardless of element. Removal is rendering-neutral.
DROP_CLASSES = frozenset(
    {
        # Gutenberg block markers. Bulma's .content styles the bare element.
        "wp-block-paragraph",
        "wp-block-heading",
        "wp-block-list",
        "wp-block-quote",
        "wp-block-quote-is-layout-flow",
        "wp-block-preformatted",
        "wp-block-separator",
        "wp-block-image",
        "wp-block-group",
        "wp-block-group__inner-container",
        "wp-block-group-is-layout-constrained",
        "wp-block-file",
        "wp-block-file__embed",
        "wp-block-embed__wrapper",
        # Consumed by the figure and table addition rules below, which read the
        # pre-filter token set, so dropping them here is safe.
        "wp-block-table",
        "wp-block-file__button",
        # WordPress registered image size names. The real dimensions live in
        # width/height/sizes/srcset, which we keep.
        "size-full",
        "size-large",
        "size-medium",
        "size-thumbnail",
        "is-resized",
        "alignnone",  # explicitly means "no alignment"
        # Block style / layout plumbing.
        "is-style-default",
        "is-style-stripes",  # re-expressed as is-striped on the child table
        "is-layout-flow",
        "is-layout-flex",
        "is-layout-constrained",
        "has-alpha-channel-opacity",
        # Legacy caption wrappers. Bulma styles .content figcaption.
        "wp-caption-text",
        "wp-element-caption",
        # Embed markers, re-expressed as .image.is-16by9 + .has-ratio.
        "wp-block-embed",
        "wp-block-embed-youtube",
        "wp-embed-aspect-16-9",
        "wp-has-aspect-ratio",
        "is-type-video",
        "is-provider-youtube",
        "has-fixed-layout",  # table-layout:fixed was an editor choice
        # Button markers, re-expressed as .buttons / .button.
        "wp-block-buttons",
        "wp-block-buttons-is-layout-flex",
        "wp-block-button",
        "wp-block-button__link",
        "wp-element-button",
        "is-content-justification-center",
        # Colour and font-size flag classes. These render as DEFAULT text today
        # because the WordPress palette CSS was never ported. Mapping them to a
        # Bulma has-text-* / is-size-* would newly colour and resize text that is
        # currently untouched, so they are removed, not mapped.
        "has-text-color",
        "has-link-color",
        "has-background",
        "has-inline-color",  # only a marker; the inline style:color does the work
        "has-custom-font-size",
        "has-medium-font-size",
        "has-small-font-size",
        "has-white-color",
        "has-vivid-cyan-blue-color",
        "has-vivid-green-cyan-color",
    }
)

# Generated per-attachment ids, e.g. wp-image-2831. Meaningless outside WordPress.
WP_IMAGE_RE = re.compile(r"^wp-image-\d+$")
# Generated layout container hashes, e.g. wp-container-core-buttons-is-layout-fe48e5de.
WP_CONTAINER_RE = re.compile(r"^wp-container-[\w-]+$")

# Unconditional renames.
RENAME_CLASSES = {
    "alignleft": "is-pulled-left",
    "alignright": "is-pulled-right",
    "has-text-align-center": "has-text-centered",
    "youtube-player": "has-ratio",
}

# Classes never to touch even though they look utility-ish: these are
# hand-authored Bulma or theme hooks already in the content.
KEEP_CLASSES = frozenset({"table", "pt-4", "social-share", "glightbox"})

# ---------------------------------------------------------------------------
# Attributes
# ---------------------------------------------------------------------------

# Dead WordPress payload, ~1950 attributes including entity-escaped JSON EXIF.
DROP_ATTRS = frozenset(
    {
        "data-attachment-id",
        "data-permalink",
        "data-orig-file",
        "data-orig-size",
        "data-image-meta",
        "data-image-title",
        "data-image-description",
        "data-image-caption",
        "data-comments-opened",
        "data-large-file",
        "data-medium-file",
        "data-shortcode",
        "data-carousel-extra",
        "data-original-width",
        "data-original-height",
        "data-wp-interactive",
        "data-wp-bind--hidden",
    }
)

# Attributes whose values hold a /wp-content/ path. Used by the orphan assertion.
MEDIA_ATTRS = ("src", "href", "srcset")
DROPPED_MEDIA_ATTRS = ("data-orig-file", "data-large-file", "data-medium-file")

# Inline style values that are provably inert, matched as whole normalised
# values rather than parsed as CSS. There are only ~40 distinct style values in
# the whole corpus, so an exact allowlist is auditable at a glance and cannot
# misfire on an authorial style we meant to keep.
#
# font-weight:400 is normal weight on a non-bold element, i.e. a literal no-op
# (437 occurrences). Corbel is a Microsoft font absent from the site's stack and
# from every Linux box. rgba(0,0,0,0) is transparent on transparent. The pixel
# widths sit on wp-caption wrappers and are the worst mobile-layout offender in
# the corpus. #589632 is exactly params.primary1 / params.success, so Bulma's
# is-success reproduces it.
DROP_STYLE_VALUES = frozenset(
    {
        "font-weight:400",                 # 437x: normal weight on a non-bold element
        "text-align:center;display:block",  # 19x: superseded by .image.is-16by9
        "font-family:corbel",               # 19x: a Microsoft font absent from the stack
        "border:0",                         # 19x: editor artifact on iframes
        "outline-width:0!important",        # 11x: editor artifact
        "background-color:rgba(0,0,0,0)",   # 7x: transparent on transparent
        "width:1034px",                     # 5x: breaks mobile; on wp-caption wrappers
        "margin:0px;padding:0px",           # 5x: editor artifact
        "background-color:#589632",         # 3x: exactly params.success, so is-success covers it
        "width:2648px",                     # 1x: breaks mobile
        "width:372px",                      # 1x: breaks mobile
    }
)

# Deliberately KEPT, for the record: `font-size:2em` / `font-size:4em` and
# `color:#339966` / `#ff0000` / `#808080` are authorial emphasis; a bare
# `text-align:center` is authorial centring; `width:100%;height:600px` sizes a
# PDF <object> and is load-bearing; the `width:NNNpx;height:NNNpx` tile sizes
# belong to the hand-converted gallery posts.


def _normalise_style(value: str) -> str:
    """Canonicalise a style attribute value for exact allowlist matching.

    Strips all whitespace, lowercases, and drops a trailing semicolon, so
    ``font-weight:400;``, ``font-weight: 400`` and ``FONT-WEIGHT : 400`` all
    collapse to the same key. There are only 39 distinct style values in the
    whole corpus, so matching whole canonical values is auditable at a glance
    and cannot misfire on a declaration we meant to keep -- unlike a general CSS
    parser, which would have to decide what to do with the ones it did not
    recognise.
    """
    return re.sub(r"\s+", "", value).strip().lower().rstrip(";")


# ---------------------------------------------------------------------------
# Class mapping, element aware
# ---------------------------------------------------------------------------

def map_classes(tag: str, tokens: list[str], in_embed: bool = False) -> list[str]:
    """Map one element's class tokens to their Bulma equivalents.

    ``tag`` matters: several WordPress classes mean different things depending on
    the element they sit on. ``in_embed`` is true when an ancestor element
    carried ``embed-youtube``, which is how an ``<iframe>`` learns that it needs
    ``has-ratio`` even when it never carried ``youtube-player``. Unknown tokens
    pass through untouched. The result is order-preserving and deduplicated,
    which is what keeps the transform idempotent when a rule adds a class.
    """
    original = set(tokens)
    out: list[str] = []

    def add(name: str) -> None:
        if name not in out:
            out.append(name)

    for token in tokens:
        if token in KEEP_CLASSES:
            add(token)
            continue
        if token in DROP_CLASSES:
            continue
        if WP_IMAGE_RE.match(token) or WP_CONTAINER_RE.match(token):
            continue
        if token in RENAME_CLASSES:
            add(RENAME_CLASSES[token])
            continue
        if token == "wp-caption":
            # A legacy [caption] leftover, always on a <div>. `.content figure`
            # does not reach a div, so these 7 images are the only ones in the
            # corpus that would be left uncentred while the 87 Gutenberg
            # <figure> images are centred. Centre them to match.
            add("has-text-centered")
            continue
        if token == "embed-youtube":
            # This span (or div) is the direct parent of the iframe in BOTH
            # embed generations, so it is the right place for Bulma's ratio box.
            # Putting it on the outer Gutenberg <figure> instead would leave the
            # iframe's `has-ratio` (position:absolute) without a positioned
            # ancestor, and the embed would collapse.
            add("image")
            add("is-16by9")
            continue
        if token == "aligncenter":
            # text-align cannot centre an image element itself, so an <img> needs
            # a block + auto margin instead. A <figure> is already centred by
            # Bulma's `.content figure { text-align: center }`, so it needs
            # nothing at all.
            if tag == "img":
                add("is-block")
                add("mx-auto")
            elif tag != "figure":
                add("has-text-centered")
            continue
        add(token)

    # --- additions, each gated on a WordPress token removed above -------------

    if tag == "figure" and "wp-block-table" in original:
        # .table-container gives overflow-x:auto, so the wide plugin-update
        # tables scroll on mobile instead of blowing out the layout.
        add("table-container")

    if tag == "table":
        # Every table in a post body gets Bulma's table styling. Tables are
        # currently completely unstyled, so this applies to the 14 that carried
        # `has-fixed-layout`, the 15 that carried no class at all, and the 1 that
        # a QGIS author had already hand-tagged `table` (the dedupe in add()
        # makes that a no-op). Doing it unconditionally also means the single
        # `is-style-stripes` figure needs no special case, and it avoids having
        # to track parent elements to find out whether a table sits inside a
        # `wp-block-table` figure.
        add("table")
        add("is-fullwidth")
        add("is-striped")
        add("is-hoverable")

    if tag == "iframe" and in_embed:
        # Covers the 19 iframes that carry `youtube-player` and the 1 that does
        # not, so every ratio box always has a positioned child.
        add("has-ratio")

    if tag == "div" and "wp-block-buttons" in original:
        add("buttons")
        add("is-centered")

    if tag == "a" and "wp-block-button__link" in original:
        # #589632 is params.primary1 and params.success, so is-success reproduces
        # the brand green that the inline background-color used to supply.
        add("button")
        add("is-success")

    if tag == "a" and "wp-block-file__button" in original:
        # Match the existing "Learn More" button in post-details.html.
        add("button")
        add("is-success")
        add("is-outlined")

    if tag == "p" and "wp-caption-text" in original:
        add("has-text-centered")
        add("is-size-7")

    return out


# ---------------------------------------------------------------------------
# Tag-level rewriting
# ---------------------------------------------------------------------------

# One attribute: leading whitespace, a name, optionally `=` and a quoted or bare
# value. The name pattern allows `--` so `data-wp-bind--hidden` matches; the bare
# value branch handles valueless attributes such as `itemscope` and the trailing
# `/` of `<img ... />`.
ATTR_RE = re.compile(r"""\s+([^\s=/>]+)(\s*=\s*(?:"[^"]*"|'[^']*'|[^\s/>]+))?""")

# Splits `<tagname` off the front of a start tag so we know where attributes begin.
TAG_HEAD_RE = re.compile(r"^<([a-zA-Z][a-zA-Z0-9]*)")


def rewrite_tag(raw: str, in_embed: bool = False) -> str:
    """Rewrite one start tag's class/style/data-* attributes, in place.

    ``raw`` is the exact original source text of a single start tag, as returned
    by ``HTMLParser.get_starttag_text()``. Everything we do not deliberately
    change is copied byte for byte, so ``src``/``href``/``srcset`` values and any
    character references inside them are untouched.
    """
    head = TAG_HEAD_RE.match(raw)
    if not head:
        return raw
    tag = head.group(1).lower()

    # Collect attributes with their spans, so edits can be spliced by offset.
    attrs: list[tuple[str, str | None, int, int]] = []
    pos = head.end()
    while pos < len(raw):
        m = ATTR_RE.match(raw, pos)
        if not m:
            break
        name = m.group(1).lower()
        value = m.group(2)
        if value is not None:
            value = value.split("=", 1)[1].strip()
        attrs.append((name, value, m.start(), m.end()))
        pos = m.end()

    def unquote(v: str | None) -> tuple[str, str]:
        """Return (inner_value, quote_char). quote_char is '' when unquoted."""
        if v and len(v) >= 2 and v[0] in "\"'" and v[-1] == v[0]:
            return v[1:-1], v[0]
        return (v or ""), ""

    existing_classes = [a for a in attrs if a[0] == "class"]
    current_tokens: list[str] = []
    if existing_classes:
        inner, _ = unquote(existing_classes[0][1])
        current_tokens = inner.split()

    new_tokens = map_classes(tag, current_tokens, in_embed)

    edits: list[tuple[int, int, str]] = []

    for name, value, start, end in attrs:
        if name in DROP_ATTRS:
            # Delete the attribute together with its leading whitespace, so the
            # surviving neighbours keep exactly one separating space and the
            # `replaceRE` precondition in post-details.html still holds.
            edits.append((start, end, ""))
        elif name == "style":
            inner, _ = unquote(value)
            if _normalise_style(inner) in DROP_STYLE_VALUES:
                edits.append((start, end, ""))
        elif name == "class":
            if new_tokens:
                inner, quote = unquote(value)
                quote = quote or '"'
                edits.append((start, end, f' class={quote}{" ".join(new_tokens)}{quote}'))
            else:
                # Drop the attribute entirely rather than leaving class="".
                edits.append((start, end, ""))

    # A rule may add classes to an element that had no class attribute at all
    # (the 15 bare <table> elements). Insert one directly after the tag name.
    if not existing_classes and new_tokens:
        edits.append((head.end(), head.end(), f' class="{" ".join(new_tokens)}"'))

    if not edits:
        return raw

    out = raw
    for start, end, replacement in sorted(edits, key=lambda e: e[0], reverse=True):
        out = out[:start] + replacement + out[end:]
    return out


# HTML void elements never push onto the open-element stack.
VOID_TAGS = frozenset(
    {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }
)


def _class_tokens(raw: str) -> list[str]:
    """Read a start tag's class tokens from its original source text."""
    head = TAG_HEAD_RE.match(raw)
    if not head:
        return []
    pos = head.end()
    while pos < len(raw):
        m = ATTR_RE.match(raw, pos)
        if not m:
            break
        if m.group(1).lower() == "class" and m.group(2):
            value = m.group(2).split("=", 1)[1].strip()
            if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
                value = value[1:-1]
            return value.split()
        pos = m.end()
    return []


class _TagScanner(HTMLParser):
    """Finds start tags and records (start, end, replacement) edit spans.

    Used purely as a tokenizer. No tree is ever built, so malformed nesting such
    as a ``<div>`` inside a ``<p>`` is preserved exactly as written.
    """

    def __init__(self, text: str) -> None:
        # convert_charrefs=False keeps `&#038;` and friends out of the callbacks
        # entirely; we never re-encode an entity.
        super().__init__(convert_charrefs=False)
        self.text = text
        self.edits: list[tuple[int, int, str]] = []
        # Open-element stack, tracking only whether an ancestor carried
        # `embed-youtube`. This is the single parent-to-child relation the
        # mapping needs; no document tree is built.
        self.embed_depth: list[bool] = []
        # getpos() counts only "\n", so line offsets must be computed the same
        # way. str.splitlines() also breaks on \r, \x0b, \x0c,   and  ,
        # which would desynchronise every offset after the first such character.
        # content/posts/phasing-out-32-bit-support-in-qgis.md contains \r.
        offsets = [0]
        for line in text.split("\n"):
            offsets.append(offsets[-1] + len(line) + 1)
        self.line_offsets = offsets

    def _handle(self, tag: str, self_closing: bool) -> None:
        raw = self.get_starttag_text()
        if not raw:
            return
        line, col = self.getpos()
        start = self.line_offsets[line - 1] + col
        if self.text[start : start + len(raw)] != raw:
            # Offsets must be exact; a mismatch means the assumptions above broke.
            raise AssertionError(f"tag offset mismatch at line {line} col {col}: {raw!r}")

        in_embed = any(self.embed_depth)
        new = rewrite_tag(raw, in_embed)
        if new != raw:
            self.edits.append((start, start + len(raw), new))

        tag = tag.lower()
        if not self_closing and tag not in VOID_TAGS:
            tokens = _class_tokens(raw)
            self.embed_depth.append("embed-youtube" in tokens)

    def handle_starttag(self, tag, attrs):  # noqa: D102
        self._handle(tag, False)

    def handle_startendtag(self, tag, attrs):  # noqa: D102
        self._handle(tag, True)

    def handle_endtag(self, tag):  # noqa: D102
        if tag.lower() not in VOID_TAGS and self.embed_depth:
            self.embed_depth.pop()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def transform_html(html: str) -> str:
    """Translate WordPress classes and strip dead attributes in a body of HTML.

    Byte-identical wherever no rule applies. Idempotent.
    """
    scanner = _TagScanner(html)
    scanner.feed(html)
    scanner.close()
    if not scanner.edits:
        return html
    out = html
    for start, end, replacement in sorted(scanner.edits, key=lambda e: e[0], reverse=True):
        out = out[:start] + replacement + out[end:]
    return out


FRONT_MATTER_RE = re.compile(r"\A(---\r?\n.*?\r?\n---\r?\n)", re.DOTALL)


def split_front_matter(text: str) -> tuple[str, str]:
    """Return (front_matter, body). Front matter is returned verbatim.

    Splitting before parsing makes it structurally impossible for the transform
    to touch `date` or `featured_image`, which is half the golden rule.
    """
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end() :]


def _media_urls(html: str) -> set[str]:
    """Every URL reachable from a surviving src/href/srcset."""
    urls: set[str] = set()
    for attr in MEDIA_ATTRS:
        for m in re.finditer(rf'{attr}\s*=\s*(["\'])(.*?)\1', html, re.DOTALL):
            value = m.group(2)
            if attr == "srcset":
                for candidate in value.split(","):
                    parts = candidate.strip().split()
                    if parts:
                        urls.add(parts[0])
            else:
                urls.add(value.strip())
    return urls


def assert_no_orphaned_media(before: str, after: str, label: str = "<html>") -> None:
    """Fail if stripping data-* attributes made any media file unreachable.

    This is the executable form of the golden rule. Eight full-size originals in
    the corpus are reachable *only* via a data-orig-file / data-large-file
    attribute, all of them inside the hand-converted gallery posts. If anyone
    shortens HAND_CONVERTED, this fires instead of silently orphaning assets.
    """
    surviving = _media_urls(after)
    for attr in DROPPED_MEDIA_ATTRS:
        for m in re.finditer(rf'{attr}\s*=\s*(["\'])(.*?)\1', before, re.DOTALL):
            url = m.group(2).strip()
            if "/wp-content/" not in url:
                continue
            if url not in surviving:
                raise AssertionError(
                    f"{label}: removing {attr} would orphan {url} — it appears in no "
                    f"surviving src/href/srcset. Add this file to HAND_CONVERTED and "
                    f"promote the original into a real <a href> by hand."
                )


def transform_markdown_file(text: str) -> str:
    """Transform one post's body, leaving its front matter byte-identical."""
    front_matter, body = split_front_matter(text)
    new_body = transform_html(body)
    assert_no_orphaned_media(body, new_body)
    result = front_matter + new_body
    # Cheap belt-and-braces check on the half of the golden rule that governs
    # permalinks: the front matter carries `date`, and the filename carries the
    # slug, so if front matter is untouched the URL cannot move.
    assert result.startswith(front_matter), "front matter was modified"
    return result
