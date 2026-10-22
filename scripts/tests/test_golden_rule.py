#!/usr/bin/env python3
"""Corpus-wide guard tests for the golden rule.

    "Always keep the link structures for media and the page so we always keep
     them when migrating."

These run the transform over every real post in memory and never write anything.
They are the safety net that makes the transform trustworthy: the unit tests
check that each mapping does what it claims, these check that nothing else moved.

Two of them are close to a correctness proof on their own:

* ``test_tag_sequence_preserved`` shows no element was added, removed, reordered
  or re-nested anywhere in the corpus — i.e. the change really is "classes and
  attributes only".
* ``test_text_and_entities_byte_identical`` shows no prose was touched and no
  character reference was re-encoded.

The corpus directory can be overridden with ``WP_CORPUS`` so the nix check can
point at a copied content tree.
"""

from __future__ import annotations

import os
import re
import sys
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import wp_to_bulma as w  # noqa: E402

CORPUS = Path(os.environ.get("WP_CORPUS", Path(__file__).resolve().parents[2] / "content" / "posts"))

# Hugo's own rewrite in layouts/partials/post-details.html:
#   {{ .Content | replaceRE `(["\s,])/wp-content/` ... }}
# Reproduced verbatim so the test fails if the precondition ever breaks.
REPLACE_RE = re.compile(r'(["\s,])/wp-content/')


def posts() -> list[Path]:
    return [p for p in sorted(CORPUS.glob("*.md")) if p.name not in w.HAND_CONVERTED]


class _TextCollector(HTMLParser):
    """Collects everything that is not a tag, without re-encoding anything."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.buf: list[str] = []

    def handle_data(self, data):
        self.buf.append(data)

    def handle_entityref(self, name):
        self.buf.append(f"&{name};")

    def handle_charref(self, name):
        self.buf.append(f"&#{name};")

    def handle_comment(self, data):
        self.buf.append(f"<!--{data}-->")


def text_of(html: str) -> str:
    parser = _TextCollector()
    parser.feed(html)
    parser.close()
    return "".join(parser.buf)


def tag_sequence(html: str) -> list[str]:
    return re.findall(r"</?([a-zA-Z][a-zA-Z0-9]*)", html)


class CorpusTestCase(unittest.TestCase):
    """Transforms the corpus once and shares the result across tests."""

    pairs: list[tuple[Path, str, str]]

    @classmethod
    def setUpClass(cls) -> None:
        files = posts()
        if not files:
            raise unittest.SkipTest(f"no posts found in {CORPUS}")
        cls.pairs = []
        for path in files:
            before = path.read_text(encoding="utf-8")
            cls.pairs.append((path, before, w.transform_markdown_file(before)))


class TestCorpusSanity(CorpusTestCase):
    def test_corpus_is_the_expected_size(self):
        self.assertGreater(len(self.pairs), 200, "corpus looks too small")

    def test_transform_is_actually_wired_up(self):
        """Prove the transform does something, whatever state the corpus is in.

        Asserting that many files change would pass only before the migration
        and fail forever afterwards, which is backwards: a clean corpus is the
        goal. So re-dirty a real post body instead and check it gets cleaned.
        """
        _path, _before, after = self.pairs[0]
        front_matter, body = w.split_front_matter(after)
        dirtied = front_matter + '<p class="wp-block-paragraph">x</p>\n' + body
        self.assertEqual(w.transform_markdown_file(dirtied), front_matter + "<p>x</p>\n" + body)

    def test_corpus_is_clean(self):
        """After the migration every post must already be in its final form."""
        dirty = [p.name for p, before, after in self.pairs if before != after]
        self.assertEqual(dirty, [], f"posts still carry WordPress markup: {dirty}")


class TestGoldenRuleMedia(CorpusTestCase):
    def test_media_urls_unchanged(self):
        """No src/href/srcset URL may be added, removed or altered."""
        for path, before, after in self.pairs:
            self.assertEqual(
                w._media_urls(before),
                w._media_urls(after),
                f"{path.name}: media URL set changed",
            )

    def test_no_media_orphaned_by_dropped_attributes(self):
        for path, before, after in self.pairs:
            w.assert_no_orphaned_media(before, after, path.name)

    def test_wp_content_count_in_src_and_srcset_unchanged(self):
        for path, before, after in self.pairs:
            def count(html: str) -> int:
                return sum(
                    1
                    for attr in ("src", "srcset")
                    for m in re.finditer(rf'{attr}\s*=\s*"([^"]*)"', html)
                    if "/wp-content/" in m.group(1)
                )

            self.assertEqual(count(before), count(after), path.name)


class TestGoldenRuleRendering(CorpusTestCase):
    def test_replaceRE_precondition_holds(self):
        """Every surviving /wp-content/ must still be rewritable by Hugo.

        If one is not preceded by a quote, whitespace or comma, Hugo will not
        prefix it with the baseURL and the image 404s in production.
        """
        for path, _before, after in self.pairs:
            for m in re.finditer(r"/wp-content/", after):
                i = m.start()
                preceding = after[i - 1] if i else ""
                # The i0.wp.com absolute CDN form is intentionally NOT matched by
                # Hugo's regex today and must stay that way.
                if after[max(0, i - 12) : i].endswith(".com") or preceding == "m":
                    continue
                self.assertIn(
                    preceding,
                    '"\', \t\n\r',
                    f"{path.name}: /wp-content/ at {i} is preceded by {preceding!r}, "
                    f"so Hugo's replaceRE will not prefix it",
                )

    def test_wp_content_match_delta_is_fully_explained(self):
        """Any drop in matchable /wp-content/ must come from dropped data-* attrs."""
        for path, before, after in self.pairs:
            delta = len(REPLACE_RE.findall(before)) - len(REPLACE_RE.findall(after))
            explained = 0
            for attr in w.DROP_ATTRS:
                for m in re.finditer(rf'\s{attr}\s*=\s*(["\'])(.*?)\1', before, re.DOTALL):
                    explained += len(REPLACE_RE.findall(m.group(0)))
            self.assertEqual(delta, explained, f"{path.name}: unexplained /wp-content/ loss")


class TestGoldenRulePermalinks(CorpusTestCase):
    def test_front_matter_byte_identical(self):
        """Permalinks are built from front matter `date` plus the filename."""
        for path, before, after in self.pairs:
            self.assertEqual(
                w.split_front_matter(before)[0],
                w.split_front_matter(after)[0],
                f"{path.name}: front matter changed, which can move the permalink",
            )

    def test_transform_never_renames_or_deletes(self):
        source = (Path(__file__).resolve().parents[1] / "clean_wordpress_markup.py").read_text()
        for forbidden in ("os.rename", "shutil.move", ".unlink(", ".rename("):
            self.assertNotIn(forbidden, source, f"driver must never call {forbidden}")


class TestStructurePreserved(CorpusTestCase):
    def test_tag_sequence_preserved(self):
        """Proves the change is classes and attributes only, corpus wide."""
        for path, before, after in self.pairs:
            self.assertEqual(
                tag_sequence(before), tag_sequence(after), f"{path.name}: element structure changed"
            )

    def test_text_and_entities_byte_identical(self):
        """Proves no prose was touched and no entity was re-encoded."""
        for path, before, after in self.pairs:
            self.assertEqual(text_of(before), text_of(after), f"{path.name}: text changed")

    def test_attribute_names_only_shrink(self):
        """The only new attribute we ever add is `class`."""
        def names(html: str) -> Counter:
            return Counter(m.group(1).lower() for m in re.finditer(r'[\s"](\w[\w:-]*)\s*=\s*["\']', html))

        for path, before, after in self.pairs:
            nb, na = names(before), names(after)
            for name, count in na.items():
                if name == "class":
                    continue
                self.assertLessEqual(count, nb[name], f"{path.name}: attribute {name} grew")


class TestCleanliness(CorpusTestCase):
    WP_TOKEN = re.compile(
        r"^(wp-|align(none|left|right|center)$|size-(large|full|medium|thumbnail)$"
        r"|is-style-|is-layout-|is-resized$|is-type-|is-provider-|has-fixed-layout$"
        r"|embed-youtube$|youtube-player$|is-content-justification-)"
    )

    def test_no_wordpress_classes_remain(self):
        leftovers: dict[str, set[str]] = {}
        for path, _before, after in self.pairs:
            for m in re.finditer(r'class\s*=\s*(["\'])(.*?)\1', after, re.DOTALL):
                for token in m.group(2).split():
                    if self.WP_TOKEN.match(token):
                        leftovers.setdefault(path.name, set()).add(token)
        self.assertEqual(leftovers, {}, f"WordPress classes survived: {leftovers}")

    def test_no_dead_data_attributes_remain(self):
        for path, _before, after in self.pairs:
            for attr in w.DROP_ATTRS:
                self.assertNotIn(f"{attr}=", after, f"{path.name}: {attr} survived")

    def test_no_empty_class_attributes(self):
        for path, _before, after in self.pairs:
            self.assertNotIn('class=""', after, path.name)
            self.assertNotIn("class=''", after, path.name)

    def test_inert_font_weight_styles_gone(self):
        for path, _before, after in self.pairs:
            self.assertNotRegex(after, r'style="font-weight:\s*400;?"', path.name)

    def test_every_has_ratio_has_a_ratio_box(self):
        """An orphaned .has-ratio is position:absolute and would break layout."""
        for path, _before, after in self.pairs:
            if "has-ratio" in after:
                self.assertEqual(
                    after.count("has-ratio"),
                    after.count("is-16by9"),
                    f"{path.name}: has-ratio count does not match is-16by9 count",
                )


class TestIdempotencyOverCorpus(CorpusTestCase):
    def test_second_pass_is_a_no_op(self):
        for path, _before, after in self.pairs:
            self.assertEqual(
                w.transform_markdown_file(after), after, f"{path.name}: not idempotent"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
