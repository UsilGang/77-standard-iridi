#!/usr/bin/env python3
"""Deterministic Standard as Code CLI for the iRidi automation standard.

The CLI never writes to Google Docs. `capture-google` is read-only and creates an
immutable local baseline. All other commands operate on local artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import mimetypes
import os
import re
import shutil
import sys
import urllib.request
import zipfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install tooling/requirements.txt") from exc


TOOLING_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = TOOLING_DIR.parent
DEFAULT_SOURCE_DIR = WORKSPACE_DIR / "standard-src"
DEFAULT_BUILD_DIR = WORKSPACE_DIR / "build"
DEFAULT_RELEASES_DIR = WORKSPACE_DIR / "releases"
DEFAULT_MANIFEST_CANDIDATE = (
    WORKSPACE_DIR.parents[1]
    / "Artifacts"
    / "Machine_Readable"
    / "standard_book_manifest_candidate_v1.yaml"
)
SCHEMA_DIR = TOOLING_DIR / "schemas"
TABLE_LAYOUT_CONTRACT = TOOLING_DIR / "table_layout_contract.yaml"
TOKEN_RE = re.compile(r"[\w-]{2,}", re.UNICODE)
STOPWORDS = {
    "а", "без", "бы", "в", "во", "вот", "вы", "где", "да", "для", "до", "его", "ее", "если", "же", "за",
    "и", "из", "или", "их", "к", "как", "какие", "какой", "ко", "ли", "на", "над", "не", "но", "о", "об",
    "от", "по", "под", "при", "про", "с", "со", "так", "такой", "там", "то", "у", "уже", "что", "это",
    "the", "and", "for", "from", "how", "what", "where", "with",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def atomic_write_text(path: Path, text: str) -> None:
    atomic_write_bytes(path, text.encode("utf-8"))


def normalize_zip_archive(path: Path) -> None:
    """Rewrite an OOXML archive with stable member order and timestamps."""
    temp = path.with_suffix(path.suffix + ".normalized")
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(temp, "w") as target:
        for original in sorted(source.infolist(), key=lambda item: item.filename):
            info = zipfile.ZipInfo(original.filename, date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = original.external_attr
            info.create_system = original.create_system
            target.writestr(info, source.read(original.filename), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    temp.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any, *, compact: bool = False) -> None:
    if compact:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    atomic_write_text(path, text)


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_yaml(path: Path, value: Any) -> None:
    atomic_write_text(
        path,
        yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120),
    )


def slugify(text: str, *, fallback: str = "item", limit: int = 80) -> str:
    value = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    value = re.sub(r"[\s_]+", "-", value.strip()).strip("-")
    return (value or fallback)[:limit]


def stable_uid(prefix: str, *parts: str) -> str:
    raw = "|".join(parts)
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    readable_source = slugify(parts[-1] if parts else prefix, fallback="unit", limit=44).replace("-", "_")
    readable = re.sub(r"[^a-z0-9_]+", "_", readable_source.lower()).strip("_") or "unit"
    return f"{prefix}_{readable}_{digest}"


def iter_tabs(tabs: Iterable[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for tab in tabs or []:
        yield tab
        yield from iter_tabs(tab.get("childTabs") or [])


def tab_properties(tab: dict[str, Any]) -> dict[str, Any]:
    return tab.get("tabProperties") or {}


def document_tab(tab: dict[str, Any]) -> dict[str, Any]:
    return tab.get("documentTab") or {}


def image_objects(doc: dict[str, Any]) -> Iterable[tuple[str, str, dict[str, Any], str]]:
    """Yield tab_id, object_id, embedded object and placement kind."""
    for tab in iter_tabs(doc.get("tabs") or []):
        props = tab_properties(tab)
        tab_id = str(props.get("tabId") or "unknown")
        dtab = document_tab(tab)
        for object_id, item in (dtab.get("inlineObjects") or {}).items():
            embedded = ((item or {}).get("inlineObjectProperties") or {}).get("embeddedObject") or {}
            if embedded.get("imageProperties"):
                yield tab_id, object_id, embedded, "inline"
        for object_id, item in (dtab.get("positionedObjects") or {}).items():
            embedded = ((item or {}).get("positionedObjectProperties") or {}).get("embeddedObject") or {}
            if embedded.get("imageProperties"):
                yield tab_id, object_id, embedded, "positioned"


def extension_for(content_type: str | None, source_uri: str | None) -> str:
    if content_type:
        ext = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
        if ext:
            return ".jpg" if ext == ".jpe" else ext
    if source_uri:
        suffix = Path(source_uri.split("?", 1)[0]).suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
            return suffix
    return ".bin"


def capture_google(args: argparse.Namespace) -> int:
    google_root = Path(args.google_mcp_root or os.environ.get("GOOGLE_MCP_ROOT", r"C:\AI\mcp-google"))
    src = google_root / "src"
    if src.is_dir():
        sys.path.insert(0, str(src))
    try:
        from google_mcp.auth import get_credentials  # type: ignore
        from googleapiclient.discovery import build  # type: ignore
    except ImportError as exc:
        raise SystemExit("Run capture-google with the mcp-google Python environment") from exc

    creds = get_credentials(allow_interactive=False)
    docs = build("docs", "v1", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    doc = docs.documents().get(documentId=args.document_id, includeTabsContent=True).execute()
    metadata = (
        drive.files()
        .get(
            fileId=args.document_id,
            supportsAllDrives=True,
            fields="id,name,mimeType,createdTime,modifiedTime,version,size,webViewLink,lastModifyingUser(displayName)",
        )
        .execute()
    )
    revision = str(doc.get("revisionId") or metadata.get("version") or "unknown")
    revision_key = hashlib.sha256(revision.encode("utf-8")).hexdigest()[:16]
    out = Path(args.output).resolve() / f"rev-{revision_key}"
    if out.exists() and not args.force:
        print(f"EXISTS {out}")
        return 0
    out.mkdir(parents=True, exist_ok=True)

    previous_assets: dict[str, dict[str, Any]] = {}
    previous_manifest_path = out / "baseline-manifest.json"
    if previous_manifest_path.exists():
        previous_manifest = read_json(previous_manifest_path)
        previous_assets = {
            str(row.get("object_id")): row
            for row in previous_manifest.get("assets", [])
            if row.get("status") == "downloaded" and row.get("path")
        }

    document_bytes = json.dumps(doc, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    atomic_write_bytes(out / "document.json", document_bytes)
    write_json(out / "drive-metadata.json", metadata)

    assets_dir = out / "assets"

    def capture_asset(item: tuple[str, str, dict[str, Any], str]) -> dict[str, Any]:
        tab_id, object_id, embedded, placement = item
        image = embedded.get("imageProperties") or {}
        content_uri = image.get("contentUri")
        source_uri = image.get("sourceUri")
        previous = previous_assets.get(object_id)
        if previous:
            previous_path = out / str(previous["path"])
            if previous_path.is_file() and sha256_file(previous_path) == previous.get("sha256"):
                return {**previous, "tab_id": tab_id, "placement": placement, "reused": True}
        row: dict[str, Any] = {
            "object_id": object_id,
            "tab_id": tab_id,
            "placement": placement,
            "title": embedded.get("title"),
            "description": embedded.get("description"),
            "source_uri": source_uri,
            "size": embedded.get("size"),
            "status": "missing_content_uri" if not content_uri else "pending",
        }
        if content_uri:
            try:
                req = urllib.request.Request(content_uri, headers={"User-Agent": "standard-book/1.0"})
                with urllib.request.urlopen(req, timeout=90) as response:
                    data = response.read()
                    content_type = response.headers.get("Content-Type")
                ext = extension_for(content_type, source_uri)
                target = assets_dir / f"{object_id}{ext}"
                atomic_write_bytes(target, data)
                row.update(
                    {
                        "status": "downloaded",
                        "path": target.relative_to(out).as_posix(),
                        "mime_type": content_type,
                        "bytes": len(data),
                        "sha256": sha256_bytes(data),
                    }
                )
            except Exception as exc:  # noqa: BLE001 - evidence must retain individual failures
                row.update({"status": "download_failed", "error": f"{type(exc).__name__}: {exc}"})
        return row

    image_items = list(image_objects(doc))
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        # executor.map keeps the source order, making the manifest deterministic.
        asset_rows = list(pool.map(capture_asset, image_items))

    tabs = [
        {
            "tab_id": tab_properties(tab).get("tabId"),
            "title": tab_properties(tab).get("title"),
            "index": tab_properties(tab).get("index"),
        }
        for tab in iter_tabs(doc.get("tabs") or [])
    ]
    manifest = {
        "schema_version": "1.0",
        "baseline_uid": f"baseline_{args.document_id[:8]}_{revision_key}",
        "captured_at": utc_now(),
        "document_id": args.document_id,
        "title": doc.get("title") or metadata.get("name"),
        "revision_id": revision,
        "revision_key": revision_key,
        "modified_time": metadata.get("modifiedTime"),
        "document_json_sha256": sha256_bytes(document_bytes),
        "tabs": tabs,
        "assets": asset_rows,
        "asset_counts": dict(
            sorted(
                {
                    status: sum(1 for row in asset_rows if row.get("status") == status)
                    for status in {row.get("status") for row in asset_rows}
                }.items()
            )
        ),
    }
    write_json(out / "baseline-manifest.json", manifest)
    print(json.dumps({"baseline": str(out), "tabs": len(tabs), "assets": manifest["asset_counts"]}, ensure_ascii=False))
    return 0


def paragraph_block(paragraph: dict[str, Any], element: dict[str, Any]) -> dict[str, Any]:
    style = paragraph.get("paragraphStyle") or {}
    runs: list[dict[str, Any]] = []
    text_parts: list[str] = []
    inline_ids: list[str] = []
    for item in paragraph.get("elements") or []:
        if item.get("textRun"):
            run = item["textRun"]
            content = run.get("content") or ""
            text_parts.append(content)
            runs.append({"text": content, "style": run.get("textStyle") or {}})
        elif item.get("inlineObjectElement"):
            object_id = item["inlineObjectElement"].get("inlineObjectId")
            if object_id:
                inline_ids.append(object_id)
                text_parts.append(f"[[asset:{object_id}]]")
    return {
        "type": "paragraph",
        "start_index": element.get("startIndex"),
        "end_index": element.get("endIndex"),
        "style": style.get("namedStyleType") or "NORMAL_TEXT",
        "heading_id": style.get("headingId"),
        "bullet": paragraph.get("bullet"),
        "text": "".join(text_parts).rstrip("\n"),
        "runs": runs,
        "inline_object_ids": inline_ids,
        "raw": element,
    }


def structural_text(content: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for element in content or []:
        if element.get("paragraph"):
            parts.append(paragraph_block(element["paragraph"], element)["text"])
        elif element.get("table"):
            for row in element["table"].get("tableRows") or []:
                for cell in row.get("tableCells") or []:
                    parts.append(structural_text(cell.get("content") or []))
    return " ".join(p for p in parts if p).strip()


def table_block(table: dict[str, Any], element: dict[str, Any]) -> dict[str, Any]:
    rows: list[list[str]] = []
    for row in table.get("tableRows") or []:
        rows.append([structural_text(cell.get("content") or []) for cell in row.get("tableCells") or []])
    return {
        "type": "table",
        "start_index": element.get("startIndex"),
        "end_index": element.get("endIndex"),
        "rows": rows,
        "raw": element,
    }


def body_blocks(body: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for element in body.get("content") or []:
        if element.get("paragraph"):
            out.append(paragraph_block(element["paragraph"], element))
        elif element.get("table"):
            out.append(table_block(element["table"], element))
        elif element.get("tableOfContents"):
            out.append({"type": "table_of_contents", "raw": element})
        elif element.get("sectionBreak"):
            out.append({"type": "section_break", "raw": element})
        else:
            out.append({"type": "unknown", "raw": element})
    return out


def markdown_for_block(block: dict[str, Any], asset_paths: dict[str, str]) -> str:
    if block["type"] == "paragraph":
        text = block.get("text") or ""
        for object_id in block.get("inline_object_ids") or []:
            ref = asset_paths.get(object_id, f"missing/{object_id}")
            text = text.replace(f"[[asset:{object_id}]]", f"![{object_id}]({ref})")
        style = block.get("style") or "NORMAL_TEXT"
        if style.startswith("HEADING_"):
            try:
                level = max(1, min(6, int(style.split("_", 1)[1])))
            except ValueError:
                level = 2
            return f"{'#' * level} {text.strip()}" if text.strip() else ""
        if block.get("bullet") and text.strip():
            return f"- {text.strip()}"
        return text.strip()
    if block["type"] == "table":
        rows = block.get("rows") or []
        if not rows:
            return ""
        width = max(len(row) for row in rows)
        normalized = [row + [""] * (width - len(row)) for row in rows]
        normalized = [
            [
                re.sub(
                    r"\[\[asset:([^]]+)\]\]",
                    lambda match: f"![{match.group(1)}]({asset_paths.get(match.group(1), f'missing/{match.group(1)}')})",
                    cell,
                )
                for cell in row
            ]
            for row in normalized
        ]
        lines = ["| " + " | ".join(cell.replace("|", "\\|") for cell in normalized[0]) + " |"]
        lines.append("| " + " | ".join("---" for _ in range(width)) + " |")
        lines.extend("| " + " | ".join(cell.replace("|", "\\|") for cell in row) + " |" for row in normalized[1:])
        return "\n".join(lines)
    return ""


def load_section_map(path: Path | None) -> dict[str, dict[str, Any]]:
    if not path or not path.is_file():
        return {}
    data = read_yaml(path) or {}
    return {str(row.get("source_tab_id")): row for row in ((data.get("book") or {}).get("sections") or [])}


def split_topics(section_uid: str, section_title: str, blocks: list[dict[str, Any]], asset_paths: dict[str, str]) -> list[dict[str, Any]]:
    topics: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    boundary_occurrences: dict[str, int] = defaultdict(int)

    def flush() -> None:
        nonlocal current
        if not current:
            return
        content = "\n\n".join(x for x in current.pop("markdown") if x).strip()
        if content:
            current["content"] = content + "\n"
            topics.append(current)
        current = None

    for index, block in enumerate(blocks, start=1):
        style = block.get("style") if block.get("type") == "paragraph" else None
        is_boundary = style in {"HEADING_1", "HEADING_2"} and (block.get("text") or "").strip()
        if is_boundary:
            flush()
            title = (block.get("text") or "").strip()
            anchor = str(block.get("heading_id") or title)
            boundary_occurrences[anchor] += 1
            occurrence = boundary_occurrences[anchor]
            seed = f"{anchor}|{occurrence}"
            current = {
                "uid": stable_uid("std_topic", section_uid, seed, f"{title}-{occurrence}"),
                "title": title,
                "heading_id": block.get("heading_id"),
                "markdown": [markdown_for_block(block, asset_paths)],
            }
        else:
            if current is None:
                current = {
                    "uid": stable_uid("std_topic", section_uid, "preamble"),
                    "title": section_title,
                    "heading_id": None,
                    "markdown": [],
                }
            current["markdown"].append(markdown_for_block(block, asset_paths))
    flush()
    return topics


def extract(args: argparse.Namespace) -> int:
    baseline = Path(args.baseline).resolve()
    source_dir = Path(args.source_dir).resolve()
    if (source_dir / "book.yaml").exists() and not args.force:
        raise SystemExit(f"Source tree already exists: {source_dir}. Use --force only for a deliberate baseline regeneration.")
    if args.force and source_dir.exists():
        source_root = source_dir.resolve()
        for name in ("assets", "sections", "staging", "entities", "taxonomy"):
            target = (source_root / name).resolve()
            if target.parent != source_root:
                raise SystemExit(f"Unsafe generated-path reset refused: {target}")
            if target.exists():
                shutil.rmtree(target)
        for name in ("book.yaml", "import-report.json"):
            target = source_root / name
            if target.exists():
                target.unlink()
    manifest = read_json(baseline / "baseline-manifest.json")
    doc = read_json(baseline / "document.json")
    section_map = load_section_map(Path(args.manifest_candidate).resolve() if args.manifest_candidate else None)

    source_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = source_dir / "assets"
    assets_dir.mkdir(exist_ok=True)
    asset_paths: dict[str, str] = {}
    asset_manifest: list[dict[str, Any]] = []
    for row in manifest.get("assets") or []:
        if row.get("status") != "downloaded":
            asset_manifest.append(row)
            continue
        src = baseline / row["path"]
        target = assets_dir / src.name
        if not target.exists() or sha256_file(target) != row.get("sha256"):
            shutil.copy2(src, target)
        asset_paths[row["object_id"]] = f"../../assets/{target.name}"
        item = dict(row)
        item["source_path"] = row["path"]
        item["path"] = target.relative_to(source_dir).as_posix()
        asset_manifest.append(item)
    write_yaml(source_dir / "assets" / "manifest.yaml", {"baseline_uid": manifest["baseline_uid"], "assets": asset_manifest})

    section_refs: list[str] = []
    section_summaries: list[dict[str, Any]] = []
    staging_refs: list[str] = []
    for tab in iter_tabs(doc.get("tabs") or []):
        props = tab_properties(tab)
        tab_id = str(props.get("tabId") or "unknown")
        title = str(props.get("title") or tab_id)
        mapped = section_map.get(tab_id) or {}
        is_buffer = title.strip().lower() == "буфер" or mapped.get("archetype") == "staging_only"
        uid = str(mapped.get("uid") or stable_uid("std_ch", tab_id, title))
        target = (source_dir / "staging" / "buffer") if is_buffer else (source_dir / "sections" / uid)
        target.mkdir(parents=True, exist_ok=True)
        blocks = body_blocks((document_tab(tab).get("body") or {}))
        with (target / "blocks.jsonl").open("w", encoding="utf-8", newline="\n") as fh:
            for block in blocks:
                fh.write(json.dumps(block, ensure_ascii=False, sort_keys=True) + "\n")
        markdown = "\n\n".join(x for x in (markdown_for_block(block, asset_paths) for block in blocks) if x).strip() + "\n"
        atomic_write_text(target / "legacy.md", markdown)
        write_json(target / "source-tab.json", document_tab(tab))

        if is_buffer:
            write_yaml(
                target / "staging.yaml",
                {
                    "uid": "std_staging_buffer",
                    "type": "staging",
                    "status": "legacy_migrated",
                    "publish": False,
                    "auto_migrate": False,
                    "source_tab_id": tab_id,
                    "baseline_uid": manifest["baseline_uid"],
                },
            )
            staging_refs.append("std_staging_buffer")
            continue

        topic_asset_paths = {key: value.replace("../../assets/", "../../../../assets/") for key, value in asset_paths.items()}
        topics = split_topics(uid, title, blocks, topic_asset_paths)
        topic_refs: list[str] = []
        for topic in topics:
            topic_uid = topic["uid"]
            topic_dir = target / "topics" / topic_uid
            topic_dir.mkdir(parents=True, exist_ok=True)
            content_path = topic_dir / "content.md"
            atomic_write_text(content_path, topic["content"])
            topic_meta = {
                "uid": topic_uid,
                "type": "topic",
                "title": topic["title"],
                "parent_uid": uid,
                "status": "legacy_migrated",
                "revision": 1,
                "digest": sha256_file(content_path),
                "privacy": "internal",
                "source_refs": [f"google_doc:{args.document_id or manifest['document_id']}#tab={tab_id}", f"baseline:{manifest['baseline_uid']}"],
                "change_refs": [],
                "introduced_in": None,
                "last_changed_in": None,
                "allowed_outputs": ["legacy-fidelity", "internal_review"],
                "summary": topic["title"],
                "aliases": [],
                "audiences": ["integrator", "designer", "sales", "presales", "training"],
                "jobs": ["learn", "explain", "select", "audit"],
                "domains": [slugify(title).replace("-", "_")],
                "lifecycle": [],
                "entity_refs": [],
                "rule_refs": [],
                "coverage_status": "documented",
                "content_ref": content_path.relative_to(source_dir).as_posix(),
                "legacy_heading_id": topic.get("heading_id"),
            }
            write_yaml(topic_dir / "topic.yaml", topic_meta)
            write_yaml(topic_dir / "rules.yaml", {"topic_uid": topic_uid, "rules": []})
            topic_refs.append(topic_uid)
        section_meta = {
            "uid": uid,
            "type": "section",
            "title": mapped.get("title") or title,
            "display_order": int(mapped.get("display_order") or props.get("index", 0) + 1),
            "display_number": mapped.get("display_number"),
            "archetype": mapped.get("archetype") or "unclassified",
            "topic_refs": topic_refs,
            "source_tab_id": tab_id,
            "status": "legacy_migrated",
            "revision": 1,
            "digest": sha256_file(target / "legacy.md"),
            "privacy": "internal",
            "source_refs": [f"google_doc:{manifest['document_id']}#tab={tab_id}", f"baseline:{manifest['baseline_uid']}"],
            "change_refs": [],
            "introduced_in": None,
            "last_changed_in": None,
            "allowed_outputs": ["legacy-fidelity", "internal_review"],
        }
        write_yaml(target / "section.yaml", section_meta)
        section_refs.append(uid)
        section_summaries.append({"uid": uid, "title": section_meta["title"], "topics": len(topic_refs), "blocks": len(blocks)})

    book = {
        "uid": "std_iridi",
        "type": "book",
        "title": manifest.get("title") or "Стандарт автоматизации iRidi",
        "status": "legacy_migrated",
        "revision": 1,
        "digest": None,
        "privacy": "internal",
        "source_refs": [f"baseline:{manifest['baseline_uid']}"],
        "change_refs": [],
        "introduced_in": None,
        "last_changed_in": None,
        "allowed_outputs": ["legacy-fidelity", "internal_review"],
        "release": None,
        "baseline_uid": manifest["baseline_uid"],
        "source_revision_id": manifest["revision_id"],
        "section_refs": section_refs,
        "staging_refs": staging_refs,
    }
    write_yaml(source_dir / "book.yaml", book)
    write_json(source_dir / "import-report.json", {"created_at": utc_now(), "baseline_uid": manifest["baseline_uid"], "sections": section_summaries, "staging": staging_refs})
    print(json.dumps({"source_dir": str(source_dir), "sections": len(section_refs), "staging": len(staging_refs)}, ensure_ascii=False))
    return 0


def collect_units(source_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    book = read_yaml(source_dir / "book.yaml")
    sections = [read_yaml(path) for path in sorted((source_dir / "sections").glob("*/section.yaml"))]
    topics = [read_yaml(path) for path in sorted((source_dir / "sections").glob("*/topics/*/topic.yaml"))]
    rules: list[dict[str, Any]] = []
    for path in sorted((source_dir / "sections").glob("*/topics/*/rules.yaml")):
        data = read_yaml(path) or {}
        rules.extend(data.get("rules") or [])
    return book, sections, topics, rules


def validate(args: argparse.Namespace) -> int:
    source_dir = Path(args.source_dir).resolve()
    findings: list[dict[str, Any]] = []
    try:
        book, sections, topics, rules = collect_units(source_dir)
    except Exception as exc:  # noqa: BLE001
        findings.append({"severity": "error", "code": "load_failed", "message": str(exc)})
        book, sections, topics, rules = {}, [], [], []

    all_units = [book, *sections, *topics, *rules]
    seen: dict[str, str] = {}
    for unit in all_units:
        uid = str((unit or {}).get("uid") or "")
        if not uid:
            findings.append({"severity": "error", "code": "missing_uid"})
            continue
        if uid in seen:
            findings.append({"severity": "error", "code": "duplicate_uid", "uid": uid})
        seen[uid] = str((unit or {}).get("type") or "unknown")
    section_uids = {row.get("uid") for row in sections}
    for ref in book.get("section_refs") or []:
        if ref not in section_uids:
            findings.append({"severity": "error", "code": "missing_section_ref", "ref": ref})
    topic_uids = {row.get("uid") for row in topics}
    for section in sections:
        refs = section.get("topic_refs") or []
        if len(refs) != len(set(refs)):
            findings.append({"severity": "error", "code": "duplicate_topic_ref", "section": section.get("uid")})
        for ref in section.get("topic_refs") or []:
            if ref not in topic_uids:
                findings.append({"severity": "error", "code": "missing_topic_ref", "section": section.get("uid"), "ref": ref})
    referenced_topic_uids = {ref for section in sections for ref in (section.get("topic_refs") or [])}
    for orphan in sorted(topic_uids - referenced_topic_uids):
        findings.append({"severity": "error", "code": "orphan_topic", "uid": orphan})
    for topic in topics:
        content = source_dir / str(topic.get("content_ref") or "")
        if not content.is_file():
            findings.append({"severity": "error", "code": "missing_content", "uid": topic.get("uid"), "path": str(content)})
        elif topic.get("digest") and topic["digest"] != sha256_file(content):
            findings.append({"severity": "error", "code": "digest_mismatch", "uid": topic.get("uid")})
    asset_manifest = source_dir / "assets" / "manifest.yaml"
    if asset_manifest.is_file():
        for row in (read_yaml(asset_manifest) or {}).get("assets") or []:
            if row.get("status") == "downloaded":
                path = source_dir / row.get("path", "")
                if not path.is_file():
                    findings.append({"severity": "error", "code": "missing_asset", "object_id": row.get("object_id")})
                elif row.get("sha256") and sha256_file(path) != row["sha256"]:
                    findings.append({"severity": "error", "code": "asset_digest_mismatch", "object_id": row.get("object_id")})

    schema_errors: list[str] = []
    try:
        import jsonschema

        schema = read_json(SCHEMA_DIR / "standard.schema.json")
        for unit in all_units:
            try:
                jsonschema.validate(unit, schema)
            except jsonschema.ValidationError as exc:
                schema_errors.append(f"{unit.get('uid', '<missing>')}: {exc.message}")
    except ImportError:
        findings.append({"severity": "warning", "code": "jsonschema_not_installed"})
    findings.extend({"severity": "error", "code": "schema", "message": msg} for msg in schema_errors)
    report = {
        "status": "pass" if not any(x["severity"] == "error" for x in findings) else "fail",
        "checked_at": utc_now(),
        "counts": {"sections": len(sections), "topics": len(topics), "rules": len(rules)},
        "findings": findings,
    }
    out = Path(args.output).resolve() if args.output else DEFAULT_BUILD_DIR / "validation-report.json"
    write_json(out, report)
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["status"] == "pass" else 2


def ordered_section_topics(section: dict[str, Any], topics_by_uid: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return [topics_by_uid[uid] for uid in (section.get("topic_refs") or []) if uid in topics_by_uid]


def selected_section_refs(book: dict[str, Any], sections: list[dict[str, Any]], requested: list[str] | None = None) -> list[str]:
    """Return requested section UIDs in book order, or the complete book scope."""
    book_refs = list(book.get("section_refs") or [])
    if not requested:
        return book_refs
    known = {str(section.get("uid")) for section in sections}
    unknown = sorted(set(requested) - known)
    outside_book = sorted(set(requested) - set(book_refs))
    if unknown:
        raise SystemExit(f"Unknown section UID(s): {', '.join(unknown)}")
    if outside_book:
        raise SystemExit(f"Section UID(s) are not in book.section_refs: {', '.join(outside_book)}")
    requested_set = set(requested)
    return [ref for ref in book_refs if ref in requested_set]


def markdown_table_cells(line: str) -> list[str]:
    value = line.strip().strip("|")
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", value)]


def markdown_is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def load_table_layout_contract(path: Path = TABLE_LAYOUT_CONTRACT) -> dict[str, dict[int, dict[str, Any]]]:
    if not path.is_file():
        return {}
    data = read_yaml(path) or {}
    result: dict[str, dict[int, dict[str, Any]]] = defaultdict(dict)
    for row in data.get("overrides") or []:
        content_ref = str(row.get("content_ref") or "")
        table_index = int(row.get("table_index", -1))
        if content_ref and table_index >= 0:
            result[content_ref][table_index] = row
    return dict(result)


def table_cell_plain_text(cell: str) -> str:
    value = re.sub(r"!\[[^]]*\]\([^)]+\)", "", cell)
    return re.sub(r"https?://\S+", "", value).strip()


def infer_table_header_rows(rows: list[list[str]]) -> int:
    if len(rows) <= 1:
        return 0
    first = rows[0]
    if any("![" in cell for cell in first):
        return 0
    if any(len(table_cell_plain_text(cell)) > 80 for cell in first):
        return 0
    if any(not table_cell_plain_text(cell) for cell in first):
        return 0
    return 1


def infer_column_width_percent(rows: list[list[str]]) -> list[float]:
    width = max((len(row) for row in rows), default=1)
    if width <= 1:
        return [100.0]
    image_columns = [any("![" in row[index] for row in rows) for index in range(width)]
    if width == 2 and image_columns == [False, True]:
        return [60.0, 40.0]
    if width == 2 and image_columns == [True, False]:
        return [40.0, 60.0]
    scores: list[float] = []
    for index in range(width):
        lengths = [len(table_cell_plain_text(row[index])) for row in rows]
        text_score = max(lengths, default=0) ** 0.5 * 5
        scores.append(max(18.0, min(60.0, text_score) + (28.0 if image_columns[index] else 0.0)))
    total = sum(scores) or 1.0
    return [round(score * 100.0 / total, 3) for score in scores]


def analyze_table_rows(rows: list[list[str]], override: dict[str, Any] | None = None) -> tuple[list[list[str]], int, list[float]]:
    override = override or {}
    width = max((len(row) for row in rows), default=1)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    explicit_width = int(override.get("effective_columns") or 0)
    if explicit_width:
        width = max(1, min(explicit_width, width))
    else:
        while width > 1 and all(not row[width - 1].strip() for row in normalized):
            width -= 1
    normalized = [row[:width] for row in normalized]
    header_rows = int(override["header_rows"]) if "header_rows" in override else infer_table_header_rows(normalized)
    widths = [float(value) for value in (override.get("column_width_percent") or infer_column_width_percent(normalized))]
    if len(widths) != width or any(value <= 0 for value in widths):
        raise ValueError(f"Invalid table column width contract: expected {width} positive values, got {widths}")
    total = sum(widths)
    widths = [round(value * 100.0 / total, 3) for value in widths]
    return normalized, max(0, min(header_rows, len(normalized))), widths


def legacy_table_rows(rows: list[list[str]]) -> tuple[list[list[str]], int, list[float]]:
    width = max((len(row) for row in rows), default=1)
    normalized = [row + [""] * (width - len(row)) for row in rows]
    return normalized, min(1, len(normalized)), [round(100.0 / width, 3)] * width


def set_docx_table_geometry(table: Any, column_width_percent: list[float], total_width_dxa: int = 9072) -> list[int]:
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    widths = [round(total_width_dxa * value / 100.0) for value in column_width_percent]
    widths[-1] += total_width_dxa - sum(widths)
    table.autofit = False
    tbl_pr = table._tbl.tblPr
    for tag, attrs in (
        ("w:tblW", {"w:type": "dxa", "w:w": str(total_width_dxa)}),
        ("w:tblLayout", {"w:type": "fixed"}),
        ("w:tblInd", {"w:type": "dxa", "w:w": "0"}),
    ):
        element = tbl_pr.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            tbl_pr.append(element)
        for key, value in attrs.items():
            element.set(qn(key), value)
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        grid_col = OxmlElement("w:gridCol")
        grid_col.set(qn("w:w"), str(width))
        grid.append(grid_col)
    for row in table.rows:
        for index, cell in enumerate(row.cells):
            tc_pr = cell._tc.get_or_add_tcPr()
            tc_w = tc_pr.find(qn("w:tcW"))
            if tc_w is None:
                tc_w = OxmlElement("w:tcW")
                tc_pr.append(tc_w)
            tc_w.set(qn("w:type"), "dxa")
            tc_w.set(qn("w:w"), str(widths[index]))
    return widths


def markdown_heading(line: str) -> tuple[int, str] | None:
    match = re.fullmatch(r"(#{1,6})\s+(.+?)\s*", line.strip())
    if not match:
        return None
    return len(match.group(1)), match.group(2)


def rendered_heading_level(markdown_level: int, normalized: bool) -> int:
    """Normalize all headings inside an addressable topic to one subheading level."""
    if normalized:
        return 3
    return 2 if markdown_level <= 2 else 3


HTML_CSS = (
    "html{background:#F1F4F6}"
    "body{font-family:Arial,sans-serif;width:100%;max-width:1040px;margin:0 auto;"
    "padding:48px clamp(28px,6vw,80px) 96px;box-sizing:border-box;font-size:16px;"
    "line-height:1.55;color:#202124;background:#FFF;overflow-wrap:anywhere}"
    "h1,h2,h3{color:#153A5B;line-height:1.25}"
    "h1{margin:0 0 1.5rem}h2{margin:2.25rem 0 .9rem}h3{margin:1.75rem 0 .7rem}"
    "p{margin:.7rem 0 1rem}ul{margin:.6rem 0 1.2rem;padding-left:1.75rem}li{margin:.25rem 0}"
    "img{display:block;max-width:100%;height:auto;margin:1rem auto}figure{margin:1.25rem 0}"
    "table{width:100%;table-layout:fixed;border-collapse:collapse;margin:1.25rem 0;font-size:.95rem}"
    "td,th{border:1px solid #B8C4CE;padding:12px;vertical-align:top;overflow-wrap:anywhere}th{background:#EAF1F6}"
    "td.table-cell-image{font-size:.85rem;color:#4B5563}td.table-cell-image img{width:auto;max-width:100%;max-height:320px;object-fit:contain}"
    ".missing-asset{color:#9B1C1C}"
    "@media(max-width:640px){body{padding:28px 22px 64px;font-size:15px}h1{font-size:1.75rem}h2{font-size:1.4rem}}"
)


def markdown_cell_html(cell: str, source_path: Path) -> str:
    parts: list[str] = []
    cursor = 0
    for match in re.finditer(r"!\[([^]]*)\]\(([^)]+)\)", cell):
        parts.append(html.escape(cell[cursor:match.start()]))
        image_path = (source_path.parent / match.group(2)).resolve()
        if image_path.is_file():
            parts.append(f"<img src='assets/{html.escape(image_path.name)}' alt='{html.escape(match.group(1))}'>")
        else:
            parts.append(html.escape(match.group(0)))
        cursor = match.end()
    parts.append(html.escape(cell[cursor:]))
    return "".join(parts)


def markdown_html(
    path: Path,
    skip_initial_heading: str | None = None,
    table_layouts: dict[int, dict[str, Any]] | None = None,
) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    index = 0
    table_index = 0
    checked_initial_heading = False
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        if not checked_initial_heading:
            checked_initial_heading = True
            heading = markdown_heading(stripped)
            if skip_initial_heading and heading and heading[1] == skip_initial_heading:
                index += 1
                continue
        if stripped.startswith("| "):
            rows: list[list[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = markdown_table_cells(lines[index])
                if not markdown_is_separator(cells):
                    rows.append(cells)
                index += 1
            if rows:
                if skip_initial_heading is not None:
                    rows, header_rows, column_widths = analyze_table_rows(rows, (table_layouts or {}).get(table_index))
                else:
                    rows, header_rows, column_widths = legacy_table_rows(rows)
                out.append("<table class='table-headered'>" if header_rows else "<table class='table-headerless'>")
                out.append("<colgroup>" + "".join(f"<col style='width:{width:g}%'>" for width in column_widths) + "</colgroup>")
                if header_rows:
                    out.append("<thead>")
                    for row in rows[:header_rows]:
                        out.append("<tr>" + "".join(f"<th>{markdown_cell_html(cell, path)}</th>" for cell in row) + "</tr>")
                    out.append("</thead>")
                out.append("<tbody>")
                for row in rows[header_rows:]:
                    cells_html = []
                    for cell in row:
                        cell_class = " class='table-cell-image'" if "![" in cell else ""
                        cells_html.append(f"<td{cell_class}>{markdown_cell_html(cell, path)}</td>")
                    out.append("<tr>" + "".join(cells_html) + "</tr>")
                out.append("</tbody></table>")
                table_index += 1
            continue
        image_match = re.search(r"!\[([^]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            out.append(f"<p>{markdown_cell_html(stripped, path)}</p>")
        elif heading := markdown_heading(stripped):
            level = rendered_heading_level(heading[0], normalized=skip_initial_heading is not None)
            out.append(f"<h{level}>{html.escape(heading[1])}</h{level}>")
        elif stripped.startswith("- "):
            items: list[str] = []
            while index < len(lines):
                candidate = lines[index].strip()
                if candidate.startswith("- "):
                    items.append(candidate[2:])
                    index += 1
                    continue
                if not candidate:
                    probe = index + 1
                    while probe < len(lines) and not lines[probe].strip():
                        probe += 1
                    if probe < len(lines) and lines[probe].strip().startswith("- "):
                        index = probe
                        continue
                break
            out.append("<ul>" + "".join(f"<li>{markdown_cell_html(item, path)}</li>" for item in items) + "</ul>")
            continue
        else:
            out.append(f"<p>{html.escape(stripped)}</p>")
        index += 1
    return out


def render_html(source_dir: Path, output: Path, profile: str, section_uids: list[str] | None = None) -> None:
    book, sections, topics, _ = collect_units(source_dir)
    topics_by_uid = {row["uid"]: row for row in topics}
    section_by_uid = {row["uid"]: row for row in sections}
    table_layout_contract = load_table_layout_contract()
    body: list[str] = [f"<h1>{html.escape(book['title'])}</h1>"]
    for ref in selected_section_refs(book, sections, section_uids):
        section = section_by_uid[ref]
        body.append(f"<h1>{html.escape(str(section.get('display_number') or ''))} {html.escape(section['title'])}</h1>")
        if profile == "legacy-fidelity":
            body.extend(markdown_html(source_dir / "sections" / ref / "legacy.md"))
        else:
            for topic in ordered_section_topics(section, topics_by_uid):
                body.append(f"<h2>{html.escape(topic['title'])}</h2>")
                body.extend(
                    markdown_html(
                        source_dir / topic["content_ref"],
                        skip_initial_heading=str(topic["title"]),
                        table_layouts=table_layout_contract.get(str(topic["content_ref"])),
                    )
                )
    atomic_write_text(output, "<!doctype html><html lang='ru'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><style>" + HTML_CSS + "</style><body>" + "\n".join(body) + "</body></html>\n")


def render_docx(source_dir: Path, output: Path, profile: str, section_uids: list[str] | None = None) -> None:
    try:
        from docx import Document
        from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
        from docx.shared import Mm, Pt
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("python-docx is required for DOCX build") from exc
    book, sections, topics, _ = collect_units(source_dir)
    doc = Document()
    fixed_time = datetime(2000, 1, 1, tzinfo=timezone.utc)
    doc.core_properties.created = fixed_time
    doc.core_properties.modified = fixed_time
    doc.core_properties.revision = 1
    sec = doc.sections[0]
    sec.top_margin, sec.right_margin, sec.bottom_margin, sec.left_margin = Mm(18), Mm(18), Mm(20), Mm(20)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    doc.add_heading(book["title"], 0)
    if profile == "standard-normalized":
        doc.add_paragraph("Нормализованное представление: единая структура разделов и адресуемых тем.")
    section_by_uid = {row["uid"]: row for row in sections}
    topics_by_uid = {row["uid"]: row for row in topics}
    table_layout_contract = load_table_layout_contract()
    for section_index, ref in enumerate(selected_section_refs(book, sections, section_uids)):
        section = section_by_uid[ref]
        if profile == "standard-normalized" and section_index:
            doc.add_page_break()
        doc.add_heading(f"{section.get('display_number') or ''} {section['title']}".strip(), 1)
        entries: list[tuple[Path, str | None, dict[int, dict[str, Any]] | None]]
        if profile == "legacy-fidelity":
            entries = [(source_dir / "sections" / ref / "legacy.md", None, None)]
        else:
            entries = [
                (
                    source_dir / topic["content_ref"],
                    str(topic["title"]),
                    table_layout_contract.get(str(topic["content_ref"])),
                )
                for topic in ordered_section_topics(section, topics_by_uid)
            ]
        for path, normalized_topic_title, table_layouts in entries:
            if normalized_topic_title:
                doc.add_heading(normalized_topic_title, 2)
            lines = path.read_text(encoding="utf-8").splitlines()
            index = 0
            table_index = 0
            checked_initial_heading = False
            while index < len(lines):
                line = lines[index]
                stripped = line.strip()
                if not stripped:
                    index += 1
                    continue
                if not checked_initial_heading:
                    checked_initial_heading = True
                    heading = markdown_heading(stripped)
                    if normalized_topic_title and heading and heading[1] == normalized_topic_title:
                        index += 1
                        continue
                if stripped.startswith("| "):
                    rows: list[list[str]] = []
                    while index < len(lines) and lines[index].strip().startswith("|"):
                        cells = markdown_table_cells(lines[index])
                        if not markdown_is_separator(cells):
                            rows.append(cells)
                        index += 1
                    if rows:
                        if normalized_topic_title:
                            rows, header_rows, column_widths = analyze_table_rows(rows, (table_layouts or {}).get(table_index))
                        else:
                            rows, header_rows, column_widths = legacy_table_rows(rows)
                        table_index += 1
                        width = len(rows[0])
                        table = doc.add_table(rows=len(rows), cols=width)
                        table.style = "Table Grid"
                        set_docx_table_geometry(table, column_widths)
                        for row_index, row in enumerate(rows):
                            for col_index in range(width):
                                cell = table.cell(row_index, col_index)
                                column_width_mm = 160 * column_widths[col_index] / 100.0
                                cell.width = Mm(column_width_mm)
                                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                                value = row[col_index] if col_index < len(row) else ""
                                image_matches = list(re.finditer(r"!\[([^]]*)\]\(([^)]+)\)", value))
                                if image_matches:
                                    paragraph = cell.paragraphs[0]
                                    paragraph.clear()
                                    plain = re.sub(r"!\[[^]]*\]\([^)]+\)", "", value).strip()
                                    if plain:
                                        paragraph.add_run(plain)
                                    for image_match in image_matches:
                                        image_path = (path.parent / image_match.group(2)).resolve()
                                        if image_path.is_file():
                                            try:
                                                image_width_mm = max(20.0, min(70.0, column_width_mm - 6.0))
                                                paragraph.add_run().add_picture(str(image_path), width=Mm(image_width_mm))
                                            except Exception:  # noqa: BLE001
                                                paragraph.add_run(f" [Изображение: {image_path.name}]")
                                else:
                                    cell.text = value
                                if row_index < header_rows:
                                    for run in cell.paragraphs[0].runs:
                                        run.bold = True
                    continue
                image_matches = list(re.finditer(r"!\[([^]]*)\]\(([^)]+)\)", stripped))
                if image_matches:
                    plain = re.sub(r"!\[[^]]*\]\([^)]+\)", "", stripped).strip()
                    heading = markdown_heading(plain)
                    if heading:
                        doc.add_heading(heading[1], rendered_heading_level(heading[0], normalized=bool(normalized_topic_title)))
                    elif plain.startswith("- "):
                        doc.add_paragraph(plain[2:], style="List Bullet")
                    elif plain:
                        doc.add_paragraph(plain)
                    for image_match in image_matches:
                        image_path = (path.parent / image_match.group(2)).resolve()
                        if image_path.is_file():
                            try:
                                doc.add_picture(str(image_path), width=Mm(160))
                            except Exception:  # noqa: BLE001
                                doc.add_paragraph(f"[Изображение: {image_path.name}]")
                        else:
                            doc.add_paragraph(image_match.group(0))
                elif heading := markdown_heading(stripped):
                    doc.add_heading(heading[1], rendered_heading_level(heading[0], normalized=bool(normalized_topic_title)))
                elif stripped.startswith("- "):
                    doc.add_paragraph(stripped[2:], style="List Bullet")
                elif stripped.startswith("| "):
                    doc.add_paragraph(stripped)
                else:
                    doc.add_paragraph(stripped)
                index += 1
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    normalize_zip_archive(output)


def build_cmd(args: argparse.Namespace) -> int:
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    requested_sections = list(getattr(args, "sections", None) or [])
    book, sections, topics, _ = collect_units(source_dir)
    section_refs = selected_section_refs(book, sections, requested_sections)
    section_by_uid = {row["uid"]: row for row in sections}
    topics_by_uid = {row["uid"]: row for row in topics}
    topic_refs = [
        topic["uid"]
        for ref in section_refs
        for topic in ordered_section_topics(section_by_uid[ref], topics_by_uid)
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    source_assets = source_dir / "assets"
    if source_assets.is_dir():
        shutil.copytree(source_assets, output_dir / "assets", dirs_exist_ok=True)
    if args.format in {"html", "all"}:
        render_html(source_dir, output_dir / f"standard-{args.profile}.html", args.profile, section_refs)
    if args.format in {"docx", "all"}:
        render_docx(source_dir, output_dir / f"standard-{args.profile}.docx", args.profile, section_refs)
    manifest = {
        "profile": args.profile,
        "built_at": utc_now(),
        "source_book_digest": sha256_file(source_dir / "book.yaml"),
        "scope": "full_book" if not requested_sections else "selected_sections",
        "section_refs": section_refs,
        "counts": {"sections": len(section_refs), "topics": len(topic_refs)},
        "outputs": [
            {"path": path.name, "sha256": sha256_file(path), "bytes": path.stat().st_size}
            for path in sorted(output_dir.glob(f"standard-{args.profile}.*"))
        ],
    }
    write_json(output_dir / f"build-{args.profile}.json", manifest)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


def index_cmd(args: argparse.Namespace) -> int:
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        if not (output_dir / "package.yaml").exists() and not args.force:
            raise SystemExit(f"Refusing to replace a non-package directory: {output_dir}. Use --force only for a deliberate generated target.")
        for name in ("content", "indexes", "assets"):
            target = (output_dir / name).resolve()
            if target.parent != output_dir:
                raise SystemExit(f"Unsafe package reset refused: {target}")
            if target.exists():
                shutil.rmtree(target)
        for name in ("topics.jsonl", "rules.jsonl", "entities.jsonl", "relations.jsonl", "aliases.json", "changes.json", "navigation.json", "package.yaml", "START_HERE.md"):
            target = output_dir / name
            if target.exists():
                target.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)
    content_dir = output_dir / "content" / "by-uid"
    content_dir.mkdir(parents=True, exist_ok=True)
    if (source_dir / "assets").is_dir():
        shutil.copytree(source_dir / "assets", output_dir / "assets", dirs_exist_ok=True)
    book, sections, topics, rules = collect_units(source_dir)
    section_by_uid = {row["uid"]: row for row in sections}
    topic_rows: list[dict[str, Any]] = []
    indexes: dict[str, dict[str, list[str]]] = {name: defaultdict(list) for name in ["audience", "job", "domain", "lifecycle", "entity"]}
    for topic in topics:
        row = dict(topic)
        source_content = source_dir / row["content_ref"]
        target_content = content_dir / f"{row['uid']}.md"
        content_text = source_content.read_text(encoding="utf-8")
        content_text = re.sub(
            r"(!\[[^]]*\])\(([^)]+)\)",
            lambda match: f"{match.group(1)}(../../assets/{(source_content.parent / match.group(2)).resolve().name})",
            content_text,
        )
        atomic_write_text(target_content, content_text)
        row["content_ref"] = target_content.relative_to(output_dir).as_posix()
        row["section_title"] = section_by_uid.get(row.get("parent_uid"), {}).get("title")
        topic_rows.append(row)
        for field, index_name in [("audiences", "audience"), ("jobs", "job"), ("domains", "domain"), ("lifecycle", "lifecycle"), ("entity_refs", "entity")]:
            for value in row.get(field) or []:
                indexes[index_name][str(value)].append(row["uid"])
    for filename, rows in [("topics.jsonl", topic_rows), ("rules.jsonl", rules), ("entities.jsonl", []), ("relations.jsonl", [])]:
        atomic_write_text(output_dir / filename, "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows))
    write_json(output_dir / "aliases.json", {row["uid"]: row.get("aliases") or [] for row in topic_rows})
    write_json(output_dir / "changes.json", [])
    write_json(output_dir / "navigation.json", {"book": book, "sections": sections})
    for name, values in indexes.items():
        write_json(output_dir / "indexes" / f"by_{name}.json", dict(sorted(values.items())))
    package = {
        "schema_version": "1.0",
        "package_uid": stable_uid("std_pkg", str(book.get("baseline_uid")), args.release),
        "release": args.release,
        "generated_at": utc_now(),
        "source_book_digest": sha256_file(source_dir / "book.yaml"),
        "counts": {"sections": len(sections), "topics": len(topics), "rules": len(rules)},
        "drafts_included": False,
        "private_sources_included": False,
    }
    write_yaml(output_dir / "package.yaml", package)
    atomic_write_text(
        output_dir / "START_HERE.md",
        "# Standard knowledge package\n\n"
        f"Release: `{args.release}`. Read `package.yaml`, then route by audience/job/domain indexes. "
        "Use `topics.jsonl` and `rules.jsonl`; cite UID and content_ref. Never infer a documented rule from absence.\n",
    )
    print(json.dumps(package, ensure_ascii=False))
    return 0


def propose_rules_cmd(args: argparse.Namespace) -> int:
    source_dir = Path(args.source_dir).resolve()
    section_dir = source_dir / "sections" / args.section
    section = read_yaml(section_dir / "section.yaml")
    patterns = [
        (re.compile(r"\b(не допускается|нельзя|не следует|не рекомендуется)\b", re.I), "prohibition", "must_not"),
        (re.compile(r"\b(должен|должна|должны|должно|необходимо|обязательно)\b", re.I), "requirement", "must"),
        (re.compile(r"\b(следует|рекомендуется|рекомендуются|рекомендуемое|рекомендуется)\b", re.I), "recommendation", "should"),
    ]
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    topic_paths = {path.parent.name: path for path in section_dir.glob("topics/*/content.md")}
    for topic_uid in section.get("topic_refs") or []:
        path = topic_paths.get(topic_uid)
        if not path:
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            plain = re.sub(r"^\s*(?:[-#]+|\|)\s*", "", line).strip(" |").strip()
            if not plain:
                continue
            for statement in re.split(r"(?<=[.!?])\s+", plain):
                normalized = re.sub(r"\s+", " ", statement).strip()
                if len(normalized) < 20:
                    continue
                for pattern, claim_type, normative_level in patterns:
                    match = pattern.search(normalized)
                    if not match:
                        continue
                    key = normalized.casefold()
                    if key in seen:
                        break
                    seen.add(key)
                    candidates.append(
                        {
                            "candidate_uid": stable_uid("rule_candidate", topic_uid, str(line_number), normalized),
                            "status": "needs_expert_review",
                            "parent_uid": topic_uid,
                            "claim_type_suggestion": claim_type,
                            "normative_level_suggestion": normative_level,
                            "statement": normalized,
                            "trigger": match.group(1),
                            "source_ref": f"{path.relative_to(source_dir).as_posix()}#L{line_number}",
                            "confidence": 0.55,
                            "warning": "Lexical candidate only; context, scope, applicability, exceptions and authority are not approved.",
                        }
                    )
                    break
    report = {
        "schema_version": "1.0",
        "section_uid": section["uid"],
        "generated_at": utc_now(),
        "status": "review_required",
        "candidate_count": len(candidates),
        "approved_rule_count": 0,
        "candidates": candidates,
    }
    write_yaml(Path(args.output).resolve(), report)
    print(json.dumps({key: report[key] for key in ("section_uid", "status", "candidate_count", "approved_rule_count")}, ensure_ascii=False))
    return 0


def token_set(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text) if token.lower() not in STOPWORDS}


def query_cmd(args: argparse.Namespace) -> int:
    package_dir = Path(args.package_dir).resolve()
    query_tokens = token_set(args.text)
    rows: list[tuple[int, dict[str, Any], str]] = []
    for line in (package_dir / "topics.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        topic = json.loads(line)
        if args.audience and args.audience not in (topic.get("audiences") or []):
            continue
        if args.job and args.job not in (topic.get("jobs") or []):
            continue
        content = (package_dir / topic["content_ref"]).read_text(encoding="utf-8")
        haystack = " ".join([topic.get("title") or "", topic.get("summary") or "", " ".join(topic.get("aliases") or []), content])
        tokens = token_set(haystack)
        score = len(query_tokens & tokens) * 10
        score += sum(5 for token in query_tokens if token in (topic.get("title") or "").lower())
        if score:
            rows.append((score, topic, content))
    rows.sort(key=lambda item: (-item[0], item[1]["uid"]))
    if not rows:
        answer = {
            "answer_status": "gap",
            "release": (read_yaml(package_dir / "package.yaml") or {}).get("release", "unknown"),
            "answer": "В опубликованном пакете не найден подтвержденный ответ.",
            "applicability": [],
            "citations": [],
            "normative_levels": [],
            "next_step": "Создать editorial gap candidate; не формулировать новую норму автоматически.",
        }
    else:
        selected = rows[: min(args.limit, len(rows))]
        answer = {
            "answer_status": "documented",
            "release": (read_yaml(package_dir / "package.yaml") or {}).get("release", "unknown"),
            "answer": selected[0][2][: args.max_chars].strip(),
            "applicability": [x for x in [args.audience, args.job] if x],
            "citations": [{"uid": topic["uid"], "title": topic["title"], "content_ref": topic["content_ref"]} for _, topic, _ in selected],
            "normative_levels": [],
            "next_step": None,
        }
    print(json.dumps(answer, ensure_ascii=False, indent=2))
    return 0


def audit_cmd(args: argparse.Namespace) -> int:
    package_dir = Path(args.package_dir).resolve()
    project = read_yaml(Path(args.input).resolve()) or {}
    rules = [json.loads(line) for line in (package_dir / "rules.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    missing = [field for field in ("requirements", "components") if field not in project]
    result = {
        "audit_status": "needs_input" if missing or not rules else "pass",
        "release": (read_yaml(package_dir / "package.yaml") or {}).get("release", "unknown"),
        "checked_inputs": project,
        "applicable_rule_uids": [row["uid"] for row in rules],
        "violations": [],
        "missing_inputs": missing + (["approved_typed_rules"] if not rules else []),
        "citations": [{"uid": row["uid"], "statement": row.get("statement")} for row in rules],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["audit_status"] == "pass" else 3


def inventory_cmd(args: argparse.Namespace) -> int:
    baseline = Path(args.baseline).resolve()
    manifest = read_json(baseline / "baseline-manifest.json")
    doc = read_json(baseline / "document.json")
    totals = {"tabs": 0, "paragraphs": 0, "tables": 0, "characters": 0, "inline_images": 0, "positioned_images": 0}
    tabs_out: list[dict[str, Any]] = []
    for tab in iter_tabs(doc.get("tabs") or []):
        props = tab_properties(tab)
        blocks = body_blocks((document_tab(tab).get("body") or {}))
        row = {
            "tab_id": props.get("tabId"),
            "title": props.get("title"),
            "paragraphs": sum(1 for x in blocks if x["type"] == "paragraph"),
            "tables": sum(1 for x in blocks if x["type"] == "table"),
            "characters": sum(len(x.get("text") or "") for x in blocks if x["type"] == "paragraph"),
            "inline_images": len(document_tab(tab).get("inlineObjects") or {}),
            "positioned_images": len(document_tab(tab).get("positionedObjects") or {}),
        }
        tabs_out.append(row)
        totals["tabs"] += 1
        for key in totals:
            if key != "tabs":
                totals[key] += int(row.get(key) or 0)
    report = {"baseline_uid": manifest["baseline_uid"], "revision_id": manifest["revision_id"], "totals": totals, "tabs": tabs_out}
    if args.output:
        write_json(Path(args.output).resolve(), report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def diff_cmd(args: argparse.Namespace) -> int:
    before = read_json(Path(args.from_manifest).resolve())
    after = read_json(Path(args.to_manifest).resolve())
    diff = {
        "from": before.get("baseline_uid") or before.get("package_uid"),
        "to": after.get("baseline_uid") or after.get("package_uid"),
        "changed": before != after,
        "from_digest": sha256_bytes(json.dumps(before, sort_keys=True).encode()),
        "to_digest": sha256_bytes(json.dumps(after, sort_keys=True).encode()),
    }
    print(json.dumps(diff, ensure_ascii=False, indent=2))
    return 0


def release_candidate_cmd(args: argparse.Namespace) -> int:
    if not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        raise SystemExit("--version must be SemVer X.Y.Z")
    source_dir = Path(args.source_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    if output_dir.exists() and any(output_dir.iterdir()) and not args.force:
        raise SystemExit(f"Candidate directory is not empty: {output_dir}. Use --force for deliberate regeneration.")
    output_dir.mkdir(parents=True, exist_ok=True)
    book, sections, topics, rules = collect_units(source_dir)
    units = [book, *sections, *topics, *rules]
    manifest_rows = [
        {
            "uid": unit["uid"],
            "type": unit["type"],
            "revision": unit.get("revision"),
            "digest": unit.get("digest"),
            "status": unit.get("status"),
        }
        for unit in units
    ]
    manifest_bytes = json.dumps(manifest_rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    included_changesets = list(dict.fromkeys(args.include_changeset or []))
    release = {
        "uid": stable_uid("std_release", args.version),
        "type": "release",
        "status": "draft",
        "revision": 1,
        "digest": None,
        "privacy": "internal",
        "source_refs": list(book.get("source_refs") or []),
        "change_refs": included_changesets,
        "introduced_in": None,
        "last_changed_in": None,
        "allowed_outputs": ["internal_review"],
        "version": args.version,
        "included_changesets": included_changesets,
        "manifest_digest": sha256_bytes(manifest_bytes),
        "published_at": None,
    }
    write_json(output_dir / "content-manifest.json", manifest_rows)
    write_yaml(output_dir / "release.yaml", release)
    atomic_write_text(
        output_dir / "CHANGELOG.md",
        f"# Release candidate {args.version}\n\n"
        "Status: internal review; not published.\n\n"
        f"- Sections: {len(sections)}\n- Topics: {len(topics)}\n- Typed rules: {len(rules)}\n"
        f"- Included changesets: {len(included_changesets)}\n- Manifest: `{release['manifest_digest']}`\n",
    )
    result = {"candidate": str(output_dir), "release": release, "counts": {"sections": len(sections), "topics": len(topics), "rules": len(rules)}}
    print(json.dumps(result, ensure_ascii=False))
    return 0


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="standard_book", description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("capture-google", help="Read Google Docs API and create immutable baseline")
    p.add_argument("--document-id", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--google-mcp-root")
    p.add_argument("--force", action="store_true")
    p.add_argument("--workers", type=int, default=8, help="Parallel image downloads (default: 8)")
    p.set_defaults(func=capture_google)

    p = sub.add_parser("inventory")
    p.add_argument("--baseline", required=True)
    p.add_argument("--output")
    p.set_defaults(func=inventory_cmd)

    p = sub.add_parser("extract")
    p.add_argument("--baseline", required=True)
    p.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    p.add_argument("--manifest-candidate", default=str(DEFAULT_MANIFEST_CANDIDATE))
    p.add_argument("--document-id")
    p.add_argument("--force", action="store_true", help="Deliberately regenerate the imported baseline tree")
    p.set_defaults(func=extract)

    p = sub.add_parser("validate")
    p.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    p.add_argument("--output")
    p.set_defaults(func=validate)

    p = sub.add_parser("build")
    p.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    p.add_argument("--output-dir", default=str(DEFAULT_BUILD_DIR))
    p.add_argument("--profile", choices=["legacy-fidelity", "standard-normalized"], required=True)
    p.add_argument("--format", choices=["html", "docx", "all"], default="all")
    p.add_argument("--section", action="append", dest="sections", help="Build only this section UID; repeat for multiple sections")
    p.set_defaults(func=build_cmd)

    p = sub.add_parser("index")
    p.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    p.add_argument("--output-dir", required=True)
    p.add_argument("--release", default="0.0.0-baseline")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=index_cmd)

    p = sub.add_parser("query")
    p.add_argument("--package-dir", required=True)
    p.add_argument("--text", required=True)
    p.add_argument("--audience")
    p.add_argument("--job")
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--max-chars", type=int, default=1600)
    p.set_defaults(func=query_cmd)

    p = sub.add_parser("audit")
    p.add_argument("--package-dir", required=True)
    p.add_argument("--input", required=True)
    p.set_defaults(func=audit_cmd)

    p = sub.add_parser("diff")
    p.add_argument("--from-manifest", required=True)
    p.add_argument("--to-manifest", required=True)
    p.set_defaults(func=diff_cmd)

    p = sub.add_parser("release-candidate", help="Create an internal immutable release candidate manifest; never publishes")
    p.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    p.add_argument("--output-dir", required=True)
    p.add_argument("--version", required=True)
    p.add_argument("--include-changeset", action="append", default=[])
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=release_candidate_cmd)

    p = sub.add_parser("propose-rules", help="Extract lexical rule candidates for expert review; never approves or publishes them")
    p.add_argument("--source-dir", default=str(DEFAULT_SOURCE_DIR))
    p.add_argument("--section", required=True)
    p.add_argument("--output", required=True)
    p.set_defaults(func=propose_rules_cmd)
    return ap


def main() -> int:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    args = parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
