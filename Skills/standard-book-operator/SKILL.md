---
name: standard-book-operator
description: Operate the iRidi Standard as Code project. Use for Google baseline capture, full-book extraction, schema validation, legacy or normalized builds, agent knowledge packages, documented/gap queries, presales audits, editorial assignments, changesets, versioning, and release preparation.
---

# Standard Book Operator

Operate the whole standard through deterministic artifacts and the project CLI. Keep the Google document read-only, preserve provenance, and never turn imported legacy prose into a new approved norm automatically.

## Start

1. Locate the project root containing `Workspace/77_Стандарт_iRidi/tooling/standard_book.py`.
2. Read the nearest `AGENTS.md`, the project decision, and the active Do before changing canonical artifacts.
3. Use the project `.venv` for local commands. Use the existing authenticated `C:/AI/mcp-google/.venv` only for read-only `capture-google`.
4. Keep `baseline-private`, extracted full text, images, builds, and releases private unless a separate publication approval explicitly permits promotion.

Read [references/command-contract.md](references/command-contract.md) before operating the CLI.

## Route the request

- New or changed Google source: capture an immutable revision, inventory it, then compare before extracting.
- Initial machine-readable migration: extract once, validate, build both profiles, and generate the agent package.
- Market, development, or owner signal: create an editorial assignment; do not edit a topic without a source and change reference.
- User question: query the generated package and return `documented`, `gap`, `conflict`, or `needs_input`; cite UIDs and content references.
- Presales check: run `audit`; never report `pass` when approved typed rules or required project inputs are absent.
- Release request: validate the source tree, resolve approved changesets, build artifacts, write release notes, then stop at the publication gate.
- Parity certification: route to independent D8 acceptance. The same implementation agent must not self-certify visual/content parity.

## Canonical boundaries

- Google Docs capture is evidence, not an automatic canonical change.
- `staging/buffer` is non-published and must never auto-migrate.
- Human prose, imported machine representation, agent synthesis, and approved rules retain explicit provenance.
- Rule extraction is a reviewed editorial operation. An empty `rules.jsonl` means the audit must return `needs_input`.
- Changes to Google Docs, Wiki, external systems, or public full-book publication require explicit approval.
- A book version changes only through an approved release; section/topic revisions may advance earlier through traceable changesets.

## Completion evidence

For implementation work, record the source revision, checksums, inventory, validation report, both build manifests, package manifest, query smoke tests, audit result, unresolved gaps, and D8 status.

Never describe a generated DOCX as visually certified when the render-and-compare gate has not passed.
