---
type: project_inbox_item
status: routed
project: 77 Standard iRidi
created: 2026-07-10
privacy: internal
source_ref: "[[01_Projects/000_CORD_System/Do_Backlog]]"
proposal_ref: "[[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-07-08_standard-book-publishing-pipeline/proposal]]"
routed_at: 2026-07-17
route_status: "workspace proposal is already in review; no canonical/public changes applied"
---

# Standard Book Subagent Intake

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[03_Resources/Standard_Book/Standard_Book_MOC]], [[03_Resources/Standard_Book/Publishing_Pipeline_Design]] и [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-07-08_standard-book-publishing-pipeline/proposal]].

## Смысл

Это не задача CORD-System. Это входящая работа для агента/субагента 77 Standard: по входящим данным формировать стандарт, готовить proposal и только после approve менять canonical/published слой.

## Что делать целевому агенту

1. Взять входящие данные из 77 Standard workspace inbox или явно указанного source package.
2. Сформировать/обновить `proposal.md` в workflow 77 Standard.
3. Если входящих данных недостаточно, вернуть intake questions вместо самостоятельного дописывания стандарта.
4. После approve собрать/подготовить нужный output: MD section, Google Doc draft, PDF или knowledge package.

## Граница

CORD-System только передал route. Исполнение, review и archive trace должны жить в проекте [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]] и workspace `77_Стандарт_iRidi`.

## Processed route

- `2026-07-17`: верхнеуровневый handoff закрыт как `routed`.
- Workspace item уже находится в `review`: `01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-07-08_standard-book-publishing-pipeline/proposal.md`.
- Google Doc, Wiki, remarks и canonical/public слой не менялись.
