---
type: implementation_do
status: done
id: DO-001-STD-AS-CODE-001
project: 77 Standard iRidi
project_id: "001"
created: 2026-08-05
started_at: 2026-08-05
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-05_Standard_As_Code_Architecture_D1_D11]]"
action_id: operate_standard_book
goal: "Реализовать D1-D7,D9-D11 как воспроизводимый Standard as Code toolchain; D8 оставить отдельным последующим gate."
target: "Workspace/77_Стандарт_iRidi/standard-src, tooling, build, releases and project skills"
tool_plan: "Google Drive read-only source access; project-local standard_book CLI; JSON Schema; deterministic render/index/query; Git; Codex skill"
tool_gap: "action/tool route must be registered after CLI contract stabilizes"
approval: "local implementation and read-only source migration approved; Google Doc/Wiki writes and public full-book publication not approved"
interaction_mode: durable_product
---

# DO-001-STD-AS-CODE-001: реализовать утвержденную архитектуру

Связано с [[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-05_Standard_As_Code_Architecture_D1_D11]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]], [[03_Resources/CORD_Methodology/Do_Execution_And_Tools]], [[03_Resources/Tool_Registry/Tool_Registry_MOC]] и [[03_Resources/Action_Registry/Action_Registry_MOC]].

## Definition of Done текущего Do

- [x] approved JSON Schemas для book/section/topic/rule/entity/asset/EDT/changeset/release/query/audit;
- [x] versioned design tokens и templates;
- [x] один CLI `standard_book` с inventory/extract/validate/build/index/query/audit/diff/release-candidate;
- [x] lossless full-book source tree без Buffer auto migration;
- [x] immutable baseline metadata и assets manifest;
- [x] структурный deep slice раздела 5 «Освещение» и private expert-review candidates без auto-approval норм;
- [x] generated human views `legacy-fidelity` и `standard-normalized`;
- [x] generated agent package и фасетные индексы;
- [x] query/audit smoke tests, включая documented/gap/needs_input и metadata contract для conflict/out_of_scope;
- [x] skill `standard-book-operator` и project copy;
- [x] зарегистрированные tool/action routes;
- [x] migration/build report с точными remaining blockers;
- [x] локальная реализация готова к Git commit; full-book artifacts исключены из public push.

## Milestones

1. `M1 decision`: approval trace, Do, approved-design statuses.
2. `M2 contracts`: schemas, tokens, templates, CLI skeleton and tests.
3. `M3 source`: read-only Google baseline, lossless full-book tree and assets inventory.
4. `M4 lighting`: normalized Lighting topics/rules/entities and dual-profile build.
5. `M5 access`: released agent package, query and presales audit.
6. `M6 hardening`: validation, deterministic rebuild, tool/skill registration and handoff to D8.

## Excluded

- независимое выполнение D8;
- изменение действующего Google Doc или Wiki;
- публикация полного текста книги в открытый GitHub без отдельного approve;
- автоматическое содержательное исправление legacy errors;
- MCP до стабильного local package/query contract.

## Evidence

Результат, hashes, проверки и blockers: [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Implementation_Report_2026-08-05]].
