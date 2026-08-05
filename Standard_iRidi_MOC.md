---
type: project_moc
status: active
created: 2026-07-08
project: 77 Standard iRidi
project_id: "001"
folder_name: 001_77_Standard_iRidi
source_ref: "[[01_Projects/000_CORD_System/Archive/Reviews/Applied/2026-07-08_Project_77_Fit_Report]]"
owner: Василий
reviewer: Василий
privacy: internal
key_task_uids:
  - "kt_e61095d3fb09"
---

# 77 Standard iRidi

Связано с [[01_Projects/000_CORD_System/CORD_System_MOC]], [[03_Resources/Standard_Book/Standard_Book_MOC]], [[01_Projects/002_Panel_P4_BUS77/Panel_P4_MOC]], [[01_Projects/003_iRidi_Wiki_Docs/iRidi_Wiki_MOC]] и [[07_Source_Registry/Source_Registry]].

## Назначение

Проект поддерживает «Стандарт автоматизации iRidi» как живое ядро проверенных знаний для инсталляторов и интеграторов, проектировщиков, монтажа/ПНР, продаж, пресейла, Академии, продукта/разработки, Project Tool, Wiki и ИИ-агентов. Книга является обязательным human-readable представлением этого ядра, но не единственным способом потребления.

## Рабочая структура

- [[01_Projects/001_77_Standard_iRidi/Inbox/README]]
- [[01_Projects/001_77_Standard_iRidi/Sources/README]]
- [[01_Projects/001_77_Standard_iRidi/Artifacts/README]]
- [[01_Projects/001_77_Standard_iRidi/Reviews/README]]
- [[01_Projects/001_77_Standard_iRidi/Decisions/README]]
- [[01_Projects/001_77_Standard_iRidi/Backlog/README]]
- [[01_Projects/001_77_Standard_iRidi/Archive/README]]
- [[01_Projects/001_77_Standard_iRidi/Workspace/README]]

## Ключевые артефакты

- [[01_Projects/001_77_Standard_iRidi/Artifacts/Integration_Map]]
- [[01_Projects/001_77_Standard_iRidi/Artifacts/Quality_Gates]]
- [[01_Projects/001_77_Standard_iRidi/Artifacts/Review_Rhythm]]
- [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/README]]
- [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/AGENTS]]
- [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/VERSIONING]]
- [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]]

## Правила

- Канон стандарта меняется через proposal -> approve -> apply -> archive.
- Сырые транскрипты, внутренние протокольные таблицы, исходники устройств и личные данные не переносятся в стандарт напрямую.
- Для публичных/Wiki материалов требуется отдельный review на границы публикации.
- Workspace `77_Стандарт_iRidi` сохраняет свою историческую структуру; CORD связывает ее через MOC и source registry, а не перемешивает папки.
- Потребляющие агенты читают только released knowledge package; raw sources, control plane, drafts и unresolved proposals не являются содержимым стандарта.

## Текущий фокус

- Поддерживать связь стандартной книги с CORD-проектами.
- Принимать только approved explanations из [[01_Projects/008_Bus77_Protocol_Knowledge/Bus77_Protocol_Knowledge_MOC]].
- Передавать feedback из [[01_Projects/002_Panel_P4_BUS77/Panel_P4_MOC]] только через отдельный proposal.
