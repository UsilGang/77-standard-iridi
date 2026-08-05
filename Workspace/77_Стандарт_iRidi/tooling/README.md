---
graph_exempt: true
---

# Standard book tooling

`standard_book.py` is the single deterministic entrypoint for capture, inventory, extraction, validation, dual-profile build, agent indexing, query, audit, diff, and release-candidate preparation.

Install `requirements.txt` into the project `.venv`, then use the operator contract in `Skills/standard-book-operator/references/command-contract.md`. Google capture is read-only and uses the existing authenticated `C:/AI/mcp-google` environment. Generated full-book content and release outputs remain private until a separate publication approval.
