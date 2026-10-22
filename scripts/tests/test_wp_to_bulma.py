#!/usr/bin/env python3
"""Unit tests for the WordPress to Bulma markup transform.

Each fixture is a short HTML string taken from the real corpus; the source file
is cited in a comment so a reader can go and look at the original.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import wp_to_bulma as w  # noqa: E402

FIXTURES: list[str] = []


def fixture(html: str) -> str:
    """Register a fixture so the idempotency test covers it automatically."""
    FIXTURES.append(html)
    return html


def tag_sequence(html: str) -> list[str]:
    return re.findall(r"</?([a-zA-Z][a-zA-Z0-9]*)", html)


def classes_of(html: str, tag: str) -> list[str]:
    m = re.search(rf"<{tag}\b[^>]*>", html)
    if not m:
        return []
    c = re.search(r'class="([^"]*)"', m.group(0))
    return c.group(1).split() if c else []


class TestBlockClassRemoval(unittest.TestCase):
    """Bulma's .content styles the bare element, so the class just goes."""

    def test_paragraph_class_removed_and_attribute_dropped(self):
        got = w.transform_html(fixture('<p class="wp-block-paragraph">x</p>'))
        self.assertEqual(got, "<p>x</p>")
        self.assertNotIn('class=""', got)

    def test_heading_list_quote_separator_preformatted(self):
        cases = {
            '<h2 class="wp-block-heading">H</h2>': "<h2>H</h2>",
            '<ul class="wp-block-list"><li>a</li></ul>': "<ul><li>a</li></ul>",
            '<ol class="wp-block-list"><li>a</li></ol>': "<ol><li>a</li></ol>",
            '<blockquote class="wp-block-quote">q</blockquote>': "<blockquote>q</blockquote>",
            '<pre class="wp-block-preformatted">p</pre>': "<pre>p</pre>",
            '<hr class="wp-block-separator" />': "<hr />",
        }
        for src, want in cases.items():
            self.assertEqual(w.transform_html(fixture(src)), want, src)

    def test_wp_image_id_and_size_classes_removed(self):
        got = w.transform_html(
            fixture('<img class="alignnone size-full wp-image-1930" src="/a.png" />')
        )
        self.assertEqual(got, '<img src="/a.png" />')

    def test_layout_plumbing_removed(self):
        got = w.transform_html(
            fixture(
                '<div class="wp-block-group__inner-container is-layout-constrained'
                ' wp-block-group-is-layout-constrained">x</div>'
            )
        )
        self.assertEqual(got, "<div>x</div>")


class TestPaletteAndFontSizeAreRemovedNotMapped(unittest.TestCase):
    """The governing principle: remove is rendering-neutral, add is not.

    These WordPress palette and font-size classes render as plain default text
    today, because the WordPress CSS was never ported. Mapping them to Bulma
    equivalents would newly colour and resize text that is currently untouched.
    """

    def test_palette_colour_classes_removed(self):
        for token in (
            "has-vivid-cyan-blue-color",
            "has-vivid-green-cyan-color",
            "has-white-color",
        ):
            got = w.transform_html(fixture(f'<span class="{token}">x</span>'))
            self.assertEqual(got, "<span>x</span>", token)
            self.assertNotIn("has-text-", got)

    def test_font_size_classes_removed(self):
        for token in ("has-medium-font-size", "has-small-font-size"):
            got = w.transform_html(fixture(f'<p class="{token}">x</p>'))
            self.assertEqual(got, "<p>x</p>", token)
            self.assertNotIn("is-size-", got)

    def test_inline_colour_marker_removed_but_style_kept(self):
        got = w.transform_html(
            fixture('<span class="has-inline-color" style="color:#339966">x</span>')
        )
        self.assertEqual(got, '<span style="color:#339966">x</span>')


class TestAlignment(unittest.TestCase):
    def test_align_left_right_become_is_pulled(self):
        self.assertEqual(
            w.transform_html(fixture('<img class="alignleft" src="/a.png" />')),
            '<img class="is-pulled-left" src="/a.png" />',
        )
        self.assertEqual(
            w.transform_html(fixture('<img class="alignright" src="/a.png" />')),
            '<img class="is-pulled-right" src="/a.png" />',
        )

    def test_aligncenter_on_img_uses_block_and_auto_margin(self):
        # text-align cannot centre the image element itself.
        got = w.transform_html(fixture('<img class="aligncenter" src="/a.png" />'))
        self.assertEqual(classes_of(got, "img"), ["is-block", "mx-auto"])

    def test_aligncenter_on_figure_adds_nothing(self):
        # Bulma's `.content figure { text-align: center }` already does it.
        got = w.transform_html(fixture('<figure class="aligncenter"><img src="/a.png" /></figure>'))
        self.assertEqual(got, '<figure><img src="/a.png" /></figure>')

    def test_aligncenter_on_div_uses_has_text_centered(self):
        got = w.transform_html(fixture('<div class="aligncenter">x</div>'))
        self.assertEqual(classes_of(got, "div"), ["has-text-centered"])


class TestTables(unittest.TestCase):
    def test_wp_block_table_figure_becomes_table_container(self):
        got = w.transform_html(
            fixture('<figure class="wp-block-table"><table class="has-fixed-layout">'
                    "<tbody><tr><td>a</td></tr></tbody></table></figure>")
        )
        self.assertEqual(classes_of(got, "figure"), ["table-container"])
        self.assertEqual(
            classes_of(got, "table"), ["table", "is-fullwidth", "is-striped", "is-hoverable"]
        )

    def test_bare_table_gains_a_class_attribute(self):
        got = w.transform_html(fixture("<table><tr><td>a</td></tr></table>"))
        self.assertEqual(
            classes_of(got, "table"), ["table", "is-fullwidth", "is-striped", "is-hoverable"]
        )

    def test_hand_authored_bulma_table_class_is_not_duplicated(self):
        # content/posts/lets-make-a-big-funding-push-for-qgis-3-0.md:41
        got = w.transform_html(fixture('<table class="table" border="0"><tr><td>a</td></tr></table>'))
        self.assertEqual(classes_of(got, "table").count("table"), 1)
        self.assertIn('border="0"', got)


class TestYouTubeEmbeds(unittest.TestCase):
    # content/posts/qgis-3-30-s-hertogenbosch-is-released.md:20
    LEGACY = (
        '<span class="embed-youtube" style="text-align:center; display: block;">'
        '<iframe loading="lazy" class="youtube-player" width="640" height="360" '
        'src="https://www.youtube.com/embed/q7O819lFKc4?version=3&#038;rel=1&#038;showsearch=0" '
        'allowfullscreen="true" style="border:0;"></iframe></span>'
    )
    # content/posts/qgis-3-28-firenze-is-released.md
    GUTENBERG = (
        '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
        'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n'
        + LEGACY
        + "\n</div></figure>"
    )

    def test_ratio_box_lands_directly_around_the_iframe(self):
        for src in (self.LEGACY, self.GUTENBERG):
            got = w.transform_html(fixture(src))
            self.assertEqual(classes_of(got, "span"), ["image", "is-16by9"], src[:40])
            self.assertIn("has-ratio", classes_of(got, "iframe"))
            # Exactly one ratio box, so `has-ratio` always has a positioned parent.
            self.assertEqual(got.count("is-16by9"), 1)

    def test_youtube_src_entities_are_byte_identical(self):
        """&#038; must survive. A tree parser would normalise it to &amp;."""
        want = (
            'src="https://www.youtube.com/embed/q7O819lFKc4'
            '?version=3&#038;rel=1&#038;showsearch=0"'
        )
        for src in (self.LEGACY, self.GUTENBERG):
            self.assertIn(want, w.transform_html(src))

    def test_iframe_without_youtube_player_class_still_gets_has_ratio(self):
        got = w.transform_html(
            fixture('<div class="embed-youtube"><iframe title="t" src="https://y/e/Y"></iframe></div>')
        )
        self.assertEqual(classes_of(got, "div"), ["image", "is-16by9"])
        self.assertIn("has-ratio", classes_of(got, "iframe"))

    def test_unrelated_iframe_does_not_get_has_ratio(self):
        """An orphaned .has-ratio is position:absolute and would break layout."""
        got = w.transform_html(
            fixture('<p><iframe src="https://docs.google.com/forms/d/e/x/viewform"></iframe></p>')
        )
        self.assertNotIn("has-ratio", got)


class TestButtons(unittest.TestCase):
    # content/posts/qgis-sustaining-member-campaign-2026.md
    SRC = (
        '<div class="wp-block-buttons has-custom-font-size has-medium-font-size '
        'is-content-justification-center is-layout-flex '
        'wp-container-core-buttons-is-layout-fe48e5de wp-block-buttons-is-layout-flex">\n'
        '<div class="wp-block-button"><a class="wp-block-button__link has-white-color '
        'has-text-color has-background has-link-color wp-element-button" '
        'href="https://qgis.org/funding/membership" '
        'style="background-color:#589632">Become a sustaining member</a></div>\n</div>'
    )

    def test_buttons_mapped_to_bulma(self):
        got = w.transform_html(fixture(self.SRC))
        self.assertEqual(classes_of(got, "div"), ["buttons", "is-centered"])
        self.assertEqual(classes_of(got, "a"), ["button", "is-success"])

    def test_brand_background_style_dropped_because_is_success_matches(self):
        # #589632 is exactly params.primary1 / params.success in config.toml.
        got = w.transform_html(self.SRC)
        self.assertNotIn("background-color:#589632", got)

    def test_href_untouched(self):
        self.assertIn('href="https://qgis.org/funding/membership"', w.transform_html(self.SRC))


class TestCaptions(unittest.TestCase):
    # content/posts/happy-new-year-2017.md:11 — a [caption] leftover: a <div>
    # illegally nested inside a <p>.
    SRC = (
        '<p><div data-shortcode="caption" id="attachment_632" style="width: 1034px" '
        'class="wp-caption alignnone"><img aria-describedby="caption-attachment-632" '
        'class="wp-image-632 size-large" src="/wp-content/uploads/a.jpg" />'
        '<p id="caption-attachment-632" class="wp-caption-text">Cap</p></div></p>'
    )

    def test_caption_div_centred_and_caption_text_styled(self):
        got = w.transform_html(fixture(self.SRC))
        self.assertEqual(classes_of(got, "div"), ["has-text-centered"])
        self.assertIn("is-size-7", got)

    def test_accessibility_ids_preserved(self):
        got = w.transform_html(self.SRC)
        self.assertIn('id="attachment_632"', got)
        self.assertIn('id="caption-attachment-632"', got)
        self.assertIn('aria-describedby="caption-attachment-632"', got)

    def test_bogus_pixel_width_dropped(self):
        self.assertNotIn("1034px", w.transform_html(self.SRC))

    def test_illegal_div_in_p_is_not_restructured(self):
        """A tree builder would hoist the <div> out of the <p>. We must not."""
        got = w.transform_html(self.SRC)
        self.assertEqual(tag_sequence(got), tag_sequence(self.SRC))


class TestAttributes(unittest.TestCase):
    def test_dead_data_attrs_removed(self):
        src = (
            '<img data-attachment-id="1" data-permalink="http://x/" '
            'data-orig-size="1,2" data-comments-opened="0" data-image-title="t" '
            'data-image-description="" data-image-caption="" data-shortcode="caption" '
            'data-original-width="5" data-original-height="6" src="/a.png" />'
        )
        got = w.transform_html(fixture(src))
        self.assertEqual(got, '<img src="/a.png" />')

    def test_entity_escaped_json_exif_blob_removed(self):
        src = (
            '<img data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,'
            '&quot;iso&quot;:&quot;0&quot;}" src="/a.png" />'
        )
        self.assertEqual(w.transform_html(fixture(src)), '<img src="/a.png" />')

    def test_double_dash_attribute_name_matches(self):
        src = '<div data-wp-interactive="core" data-wp-bind--hidden="x">y</div>'
        self.assertEqual(w.transform_html(fixture(src)), "<div>y</div>")

    def test_unknown_data_attr_kept(self):
        src = '<a data-type="fragment-mention" data-username="mbernasocchi" href="/x">m</a>'
        self.assertEqual(w.transform_html(fixture(src)), src)

    def test_srcset_sizes_loading_kept(self):
        src = (
            '<img loading="lazy" class="wp-image-1" src="/a.png" '
            'srcset="/a.png 780w, /a.png 150w" sizes="(max-width: 780px) 100vw, 780px" />'
        )
        got = w.transform_html(fixture(src))
        self.assertIn('srcset="/a.png 780w, /a.png 150w"', got)
        self.assertIn('sizes="(max-width: 780px) 100vw, 780px"', got)
        self.assertIn('loading="lazy"', got)

    def test_inert_styles_removed(self):
        for value in (
            "font-weight:400;",
            "font-weight: 400",
            "font-family:Corbel;",
            "border:0;",
            "outline-width:0 !important;",
            "background-color:rgba(0, 0, 0, 0)",
        ):
            got = w.transform_html(fixture(f'<span style="{value}">x</span>'))
            self.assertEqual(got, "<span>x</span>", value)

    def test_meaningful_styles_kept(self):
        for value in ("font-size:2em;", "color:#ff0000", "width:100%;height:600px"):
            src = f'<span style="{value}">x</span>'
            self.assertEqual(w.transform_html(fixture(src)), src, value)

    def test_empty_class_attribute_dropped(self):
        got = w.transform_html(fixture('<div class="">x</div>'))
        self.assertEqual(got, "<div>x</div>")

    def test_attribute_order_quoting_and_self_closing_preserved(self):
        src = (
            "<img  alt='a'  data-attachment-id=\"9\"  title=\"t\"  "
            'src="/wp-content/uploads/a.png"  width="10" />'
        )
        got = w.transform_html(fixture(src))
        self.assertIn("alt='a'", got)  # single quotes survive
        self.assertIn('title="t"', got)
        self.assertTrue(got.rstrip().endswith("/>"))
        self.assertLess(got.index('title="t"'), got.index('src="/wp-content'))

    def test_single_quoted_href_preserved_byte_for_byte(self):
        # content/posts/qgis-annual-general-meeting-2020.md
        src = "<a href='https://x/mentions/mbernasocchi/' class='__p2-hovercard mention'>m</a>"
        self.assertIn("href='https://x/mentions/mbernasocchi/'", w.transform_html(fixture(src)))


class TestForeignClassesUntouched(unittest.TestCase):
    """Residue from pasted Gmail, GitHub and Sphinx content is out of scope."""

    def test_foreign_classes_pass_through(self):
        for token in (
            "reference external",
            "gmail_default",
            "task-list-item position-relative border-right-0",
            "issue-link js-issue-link",
            "moz-txt-link-freetext",
            "Apple-converted-space",
            "glightbox",
            "external-link",
        ):
            src = f'<span class="{token}">x</span>'
            self.assertEqual(w.transform_html(fixture(src)), src, token)

    def test_hand_authored_bulma_helpers_kept(self):
        for token in ("pt-4", "social-share"):
            src = f'<div class="{token}">x</div>'
            self.assertEqual(w.transform_html(fixture(src)), src, token)


class TestProseAndEntities(unittest.TestCase):
    def test_prose_entities_never_re_encoded(self):
        src = fixture(
            '<p class="wp-block-paragraph">That&#8217;s &#8220;quoted&#8221; '
            "&amp; spaced&nbsp;out.</p>"
        )
        got = w.transform_html(src)
        for entity in ("&#8217;", "&#8220;", "&#8221;", "&amp;", "&nbsp;"):
            self.assertIn(entity, got)

    def test_comments_preserved(self):
        src = fixture("<div>a</div>\n<!-- close row -->\n<div>b</div>")
        self.assertIn("<!-- close row -->", w.transform_html(src))

    def test_carriage_returns_do_not_desynchronise_offsets(self):
        """getpos() counts only \\n, so line offsets must use split('\\n').

        content/posts/phasing-out-32-bit-support-in-qgis.md contains \\r.
        """
        src = fixture(
            'line one\rstill line one\n<p class="wp-block-paragraph">x</p>\n'
            '\r\n<img class="wp-image-7" src="/a.png" />'
        )
        got = w.transform_html(src)
        self.assertIn("<p>x</p>", got)
        self.assertIn('<img src="/a.png" />', got)
        self.assertIn("still line one", got)


class TestFrontMatter(unittest.TestCase):
    POST = (
        "---\n"
        'title: "A post"\n'
        'date: "2017-01-10T08:48:22+00:00"\n'
        "draft: false\n"
        'featured_image: "/wp-content/uploads/2017/01/x.png"\n'
        "---\n"
        "\n"
        '<p class="wp-block-paragraph">Body</p>\n'
    )

    def test_front_matter_byte_identical(self):
        got = w.transform_markdown_file(self.POST)
        fm_in, _ = w.split_front_matter(self.POST)
        fm_out, _ = w.split_front_matter(got)
        self.assertEqual(fm_in, fm_out)
        self.assertIn('date: "2017-01-10T08:48:22+00:00"', got)
        self.assertIn('featured_image: "/wp-content/uploads/2017/01/x.png"', got)

    def test_body_still_transformed(self):
        self.assertIn("<p>Body</p>", w.transform_markdown_file(self.POST))

    def test_file_with_no_front_matter(self):
        self.assertEqual(w.transform_html("<p>x</p>"), "<p>x</p>")


class TestGoldenRuleAssertion(unittest.TestCase):
    def test_orphaned_media_raises(self):
        """An asset reachable only via data-orig-file must not be dropped silently."""
        src = '<img data-orig-file="/wp-content/uploads/2018/11/img_0199.jpg" src="/other.png" />'
        with self.assertRaises(AssertionError) as ctx:
            w.transform_markdown_file("---\ntitle: x\n---\n\n" + src)
        self.assertIn("img_0199.jpg", str(ctx.exception))
        self.assertIn("HAND_CONVERTED", str(ctx.exception))

    def test_duplicate_data_orig_file_is_fine(self):
        src = (
            '<img data-orig-file="/wp-content/uploads/a.png" '
            'src="/wp-content/uploads/a.png" />'
        )
        got = w.transform_markdown_file("---\ntitle: x\n---\n\n" + src)
        self.assertIn('src="/wp-content/uploads/a.png"', got)

    def test_hand_converted_hook_still_exists(self):
        """The galleries are converted, so the set is empty, but the hook stays.

        If a future import reintroduces a gallery, its filename goes here. The
        orphan assertion above is what tells you that is needed.
        """
        self.assertIsInstance(w.HAND_CONVERTED, frozenset)
        self.assertEqual(w.HAND_CONVERTED, frozenset())


class TestIdempotency(unittest.TestCase):
    def test_every_fixture_is_idempotent(self):
        self.assertGreater(len(FIXTURES), 35, "fixtures did not register")
        for src in FIXTURES:
            once = w.transform_html(src)
            self.assertEqual(w.transform_html(once), once, src[:80])


if __name__ == "__main__":
    unittest.main(verbosity=2)
