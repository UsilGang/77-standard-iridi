from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "standard_book.py"
SPEC = importlib.util.spec_from_file_location("standard_book", MODULE_PATH)
assert SPEC and SPEC.loader
standard_book = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(standard_book)


class StandardBookTests(unittest.TestCase):
    def test_uid_is_ascii_and_distinguishes_duplicate_anchors(self) -> None:
        first = standard_book.stable_uid("std_topic", "std_ch_lighting", "h.same|1", "Освещение-1")
        second = standard_book.stable_uid("std_topic", "std_ch_lighting", "h.same|2", "Освещение-2")
        self.assertRegex(first, r"^[a-z][a-z0-9_:-]+$")
        self.assertNotEqual(first, second)

    def test_stopwords_do_not_create_false_documented_answer(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            package = Path(raw)
            (package / "content").mkdir()
            (package / "content" / "topic.md").write_text("Управление шторами для спальни", encoding="utf-8")
            row = {
                "uid": "std_topic_curtains",
                "title": "Шторы",
                "summary": "Шторы",
                "aliases": [],
                "audiences": ["presales"],
                "jobs": ["audit"],
                "content_ref": "content/topic.md",
            }
            (package / "topics.jsonl").write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
            standard_book.write_yaml(package / "package.yaml", {"release": "test"})
            args = argparse.Namespace(package_dir=str(package), text="квантовый телепортатор для бассейна", audience="presales", job="audit", limit=3, max_chars=500)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                standard_book.query_cmd(args)
            self.assertEqual(json.loads(output.getvalue())["answer_status"], "gap")

    def test_markdown_table_separator_is_not_data(self) -> None:
        self.assertTrue(standard_book.markdown_is_separator(["---", ":---:"]))
        self.assertFalse(standard_book.markdown_is_separator(["DALI", "---"]))

    def test_selected_section_refs_preserve_book_order(self) -> None:
        book = {"section_refs": ["std_ch_a", "std_ch_b", "std_ch_c"]}
        sections = [{"uid": uid} for uid in book["section_refs"]]
        self.assertEqual(
            standard_book.selected_section_refs(book, sections, ["std_ch_c", "std_ch_a"]),
            ["std_ch_a", "std_ch_c"],
        )

    def test_selected_section_refs_reject_unknown_uid(self) -> None:
        with self.assertRaises(SystemExit):
            standard_book.selected_section_refs(
                {"section_refs": ["std_ch_a"]},
                [{"uid": "std_ch_a"}],
                ["std_ch_missing"],
            )

    def test_normalized_html_skips_repeated_topic_heading_and_groups_list(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "topic.md"
            path.write_text("# 5.1 Topic\n\nIntro\n\n- one\n\n- two\n", encoding="utf-8")
            rendered = standard_book.markdown_html(path, skip_initial_heading="5.1 Topic")
            self.assertNotIn("<h2>5.1 Topic</h2>", rendered)
            self.assertIn("<ul><li>one</li><li>two</li></ul>", rendered)

    def test_grouped_html_list_preserves_inline_image(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            (folder / "image.png").write_bytes(b"image")
            path = folder / "topic.md"
            path.write_text("- text\n\n- ![scheme](image.png)\n", encoding="utf-8")
            rendered = standard_book.markdown_html(path)
            self.assertIn("<img src='assets/image.png' alt='scheme'>", rendered[0])


if __name__ == "__main__":
    unittest.main()
