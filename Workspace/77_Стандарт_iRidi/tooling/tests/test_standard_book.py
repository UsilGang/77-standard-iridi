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


if __name__ == "__main__":
    unittest.main()
