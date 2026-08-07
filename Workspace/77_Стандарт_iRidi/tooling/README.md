---
graph_exempt: true
---

# Standard book tooling

`standard_book.py` is the single deterministic entrypoint for capture, inventory, extraction, validation, dual-profile build, agent indexing, query, audit, diff, and release-candidate preparation.

Install `requirements.txt` into the project `.venv`, then use the operator contract in `Skills/standard-book-operator/references/command-contract.md`. Google capture is read-only and uses the existing authenticated `C:/AI/mcp-google` environment. Generated full-book content and release outputs remain private until a separate publication approval.

For a contract pilot, `build --section <section-uid>` renders one or more selected sections with the same renderer and profile used for the full book. A section build is a review surface, not a separate template or proof of full-book acceptance.

The normalized HTML and DOCX builds derive one navigation outline from section, topic, and fragment semantic UIDs. HTML renders a sticky table of contents plus previous/next controls; DOCX renders a static clickable table of contents plus internal hyperlinks. `audit-migration` fails when any generated internal link has no matching anchor or bookmark.

`render_browser_audit.js` applies `std_render_parity_audit_contract_v1` to the complete HTML at desktop, tablet, and mobile widths. It reports critical, material, and cosmetic discrepancies as JSON and fails on broken images, anchors, heading hierarchy, overflow, or unusable table/image geometry.
