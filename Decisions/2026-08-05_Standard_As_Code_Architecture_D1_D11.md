---
type: decision
status: applied_to_backlog
created: 2026-08-05
project: 77 Standard iRidi
project_id: "001"
privacy: internal
origin: human
source_ref: "[[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-08-05_Standard_As_Code_Architecture_Review]]"
approval_ref: "user: аппрув на все; D8 сейчас не выполняем; остальное реализовать"
approved_decisions: [D1, D2, D3, D4, D5, D6, D7, D9, D10, D11]
deferred_execution: [D8]
---

# Решение: реализовать архитектуру Standard as Code

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]] и [[01_Projects/001_77_Standard_iRidi/Archive/Backlog/Done/DO-001-STD-AS-CODE-001_Implement_Approved_Architecture]].

## Принято

- D1–D7: source-of-truth, dual run, UID, гранулярность, versioning, full-book scope с первым deep slice «Освещение», единый CLI и skill;
- D9: lossless legacy layer плюс normalized canon с transformation trace;
- D10: EDT, changeset и release trace;
- D11: физическое разделение control/content/tooling/build/releases и released agent package.

## Граница решения

- Google Doc пока остается действующим опубликованным каноном;
- внешняя публикация новой книги, Wiki и изменение Google Doc не разрешены этим решением;
- полный текст книги можно читать и мигрировать локально, но его публикация в открытый GitHub требует отдельного publication approve;
- Buffer не мигрируется автоматически;
- Project Tool compiler требует отдельного typed engineering contract;
- D8 не выполняется в текущем Do, но остается обязательным cutover gate.

## Исполнение

Исполнен master Do [[01_Projects/001_77_Standard_iRidi/Archive/Backlog/Done/DO-001-STD-AS-CODE-001_Implement_Approved_Architecture]]. Он оставил воспроизводимый source/build/query toolchain и доказательства готовности для последующего независимого D8.
