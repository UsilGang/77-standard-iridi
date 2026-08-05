---
type: machine_readable_bridge
status: proposal
project: 77 Standard iRidi
project_id: "001"
created: 2026-08-05
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]]"
---

# Machine-readable bridge: Standard book architecture candidates

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]] и [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-05_Standard_As_Code_Architecture_Review]].

## Artifact

[standard_book_manifest_candidate_v1.yaml](standard_book_manifest_candidate_v1.yaml) — draft machine-readable inventory of the 17 chapters and Buffer, including stable candidate UIDs, Google tab IDs, archetypes, source status and object counts.

[standard_template_contract_candidate_v1.yaml](standard_template_contract_candidate_v1.yaml) — draft executable contract for legacy/normalized layers, build profiles, shared slots, archetypes, missing policies and refactoring guardrails.

[editorial_assignment_schema_candidate_v1.yaml](editorial_assignment_schema_candidate_v1.yaml) — draft contract for EDT intake, content/visual plan, outputs, acceptance, trace chain and book/unit/build versioning.

[agent_knowledge_package_schema_candidate_v1.yaml](agent_knowledge_package_schema_candidate_v1.yaml) — draft contract for physical layer separation, human audiences, machine consumers, generated indexes, query/audit outputs and access profiles.

## Status and allowed use

- `proposal`, не канон;
- собран по live read-only inventory Google Doc 2026-08-05;
- разрешен для architecture review и планирования migration pilot;
- запрещен как production build input до approve и schema validation;
- не содержит текста книги или raw confidential sources.
- template candidate не разрешает автоматически исправлять legacy content.

## Human projection

Объяснение полей, findings и выводов: [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]].

Проектная модель, в которую должен перейти manifest: [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]].

Правила рефакторинга: [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]].

Модель редакционного задания и версий: [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]].

Модель потребителей и доступа агентов: [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]].
