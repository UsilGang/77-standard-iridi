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
            args = argparse.Namespace(package_dir=str(package), text="поддерживается ли квантовый телепортатор для бассейна", audience="presales", job="audit", limit=3, max_chars=500)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                standard_book.query_cmd(args)
            self.assertEqual(json.loads(output.getvalue())["answer_status"], "gap")

    def test_markdown_table_separator_is_not_data(self) -> None:
        self.assertTrue(standard_book.markdown_is_separator(["---", ":---:"]))
        self.assertFalse(standard_book.markdown_is_separator(["DALI", "---"]))

    def test_google_soft_break_does_not_split_markdown_table(self) -> None:
        content = "| Device | IP-Hub/\vLH-Hub |\n| --- | --- |\n| Camera | yes |\n"
        lines = standard_book.logical_markdown_lines(content)
        self.assertEqual(len([line for line in lines if line.startswith("|")]), 3)
        self.assertIn("IP-Hub/ LH-Hub", lines[0])

    def test_migrated_nodes_are_classified_without_inventing_content(self) -> None:
        self.assertEqual(standard_book.topic_classification("5. Lighting", "# 5. Lighting\n", "5.1 General"), "container")
        self.assertEqual(standard_book.topic_classification("5.9 Missing", "# 5.9 Missing\n"), "gap")
        self.assertEqual(standard_book.topic_classification("[[asset:kix.image]]", "# [[asset:kix.image]]\n\n![x](x.png)"), "attachment")
        self.assertEqual(standard_book.topic_classification("\ue907\ue907", "# \ue907\ue907\n"), "artifact")

    def test_semantic_uid_is_ascii_and_stable(self) -> None:
        first = standard_book.topic_semantic_uid("lighting", "5.3.2.1. Диммируемое освещение", "legacy-1", "content", set())
        second = standard_book.topic_semantic_uid("lighting", "5.3.2.1. Диммируемое освещение", "legacy-1", "content", set())
        self.assertEqual(first, second)
        self.assertRegex(first, r"^std_topic_[a-z0-9_]+$")

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

    def test_deep_markdown_headings_are_normalized_as_topic_subheadings(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "topic.md"
            path.write_text(
                "# 5.3.2 Topic\n\n##### 5.3.2.1.1. General\n\n#### 5.3.2.1.2. Phase dimming\n",
                encoding="utf-8",
            )
            rendered = standard_book.markdown_html(path, skip_initial_heading="5.3.2 Topic")
            self.assertEqual(
                rendered,
                ["<h3>5.3.2.1.1. General</h3>", "<h3>5.3.2.1.2. Phase dimming</h3>"],
            )

    def test_html_contract_has_readable_page_margins(self) -> None:
        self.assertIn("max-width:1040px", standard_book.HTML_CSS)
        self.assertIn("padding:48px clamp(28px,6vw,80px) 96px", standard_book.HTML_CSS)

    def test_headerless_image_table_contract_restores_effective_columns(self) -> None:
        rows = [
            ["Monochrome Long description", "![image](image.png) Caption", ""],
            ["Tunable White Long description", "![image2](image2.png) Caption", ""],
        ]
        normalized, header_rows, widths = standard_book.analyze_table_rows(
            rows,
            {"header_rows": 0, "effective_columns": 2, "column_width_percent": [60, 40]},
        )
        self.assertEqual(header_rows, 0)
        self.assertEqual([len(row) for row in normalized], [2, 2])
        self.assertEqual(widths, [60.0, 40.0])

    def test_normalized_html_renders_headerless_table_with_colgroup(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            folder = Path(raw)
            (folder / "image.png").write_bytes(b"image")
            path = folder / "topic.md"
            path.write_text(
                "# Topic\n\n| Description | ![scheme](image.png) Caption |  |\n| --- | --- | --- |\n| More | ![scheme](image.png) Caption 2 |  |\n",
                encoding="utf-8",
            )
            rendered = "".join(
                standard_book.markdown_html(
                    path,
                    skip_initial_heading="Topic",
                    table_layouts={0: {"header_rows": 0, "effective_columns": 2, "column_width_percent": [60, 40]}},
                )
            )
            self.assertIn("<table class='table-headerless'>", rendered)
            self.assertIn("<col style='width:60%'><col style='width:40%'>", rendered)
            self.assertNotIn("<thead>", rendered)
            self.assertNotIn("<th>", rendered)
            self.assertIn("class='table-cell-image'", rendered)

    def test_docx_table_geometry_uses_fixed_60_40_columns(self) -> None:
        from docx import Document

        table = Document().add_table(rows=1, cols=2)
        widths = standard_book.set_docx_table_geometry(table, [60, 40])
        self.assertEqual(sum(widths), 9072)
        self.assertEqual(widths, [5443, 3629])

    def test_query_domain_prevents_cross_domain_false_positive(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            package = Path(raw)
            (package / "content").mkdir()
            (package / "content" / "ventilation.md").write_text("Интеграция вентустановки по Modbus.", encoding="utf-8")
            (package / "content" / "voice.md").write_text("Поддерживается голосовой помощник.", encoding="utf-8")
            rows = [
                {
                    "uid": "std_topic_ventilation_modbus_interface_modules",
                    "title": "Интеграция вентиляции",
                    "aliases": ["вентиляционная установка"],
                    "answers_questions": ["Какие вентиляционные установки поддерживаются?"],
                    "summary": "Modbus для вентиляции",
                    "domains": ["ventilation"],
                    "node_kind": "content",
                    "queryable": True,
                    "content_ref": "content/ventilation.md",
                },
                {
                    "uid": "std_topic_voice_assistant",
                    "title": "Голосовой помощник",
                    "aliases": ["поддержка"],
                    "answers_questions": ["Что поддерживается?"],
                    "summary": "Голосовое управление",
                    "domains": ["architecture"],
                    "node_kind": "content",
                    "queryable": True,
                    "content_ref": "content/voice.md",
                },
            ]
            (package / "topics.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
            standard_book.write_yaml(package / "package.yaml", {"release": "test"})
            args = argparse.Namespace(package_dir=str(package), text="Какие вентиляционные установки поддерживаются?", audience=None, job=None, limit=3, max_chars=500)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                standard_book.query_cmd(args)
            result = json.loads(output.getvalue())
            self.assertEqual(result["answer_status"], "documented")
            self.assertEqual(result["citations"][0]["uid"], "std_topic_ventilation_modbus_interface_modules")
            self.assertEqual(result["detected_domains"], ["ventilation"])


if __name__ == "__main__":
    unittest.main()
