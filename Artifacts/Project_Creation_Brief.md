---
type: project_creation_brief
status: active
project: 77 Standard iRidi
project_id: 001
project_type_id: C7
created: 2026-07-20
updated: 2026-07-20
owner: Василий
reviewer: Василий
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Sources/Key_Task_Log_N31_kt_e61095d3fb09]]"
key_task_uids: ""
passport_uid: "needs_passport_review:77_standard_iridi"
project_route: existing_project
---
# Project Creation Brief: 77 Standard iRidi

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Passport]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/README]], [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/README]] и [[05_Templates/Project_Creation_Brief]].

## Кратко

`001_77_Standard_iRidi` - существующий проект ведения книги и стандарта автоматизации iRidi. Это не разовая задача написания текста, а живой knowledge-cycle типа `C7`: новые продуктовые, монтажные, Wiki и полевые сигналы попадают в review, затем в proposal стандарта, после approve - в публикацию или archive trace.

## Основание

| Поле | Значение |
| --- | --- |
| Источник проекта | [[01_Projects/001_77_Standard_iRidi/Sources/Key_Task_Log_N31_kt_e61095d3fb09]] |
| ККЗ | `kt_e61095d3fb09` |
| Ключевая задача | Подготовить, согласовать и опубликовать материалы по книге "Стандарт автоматизации", этап 1 |
| Критерий результата | Опубликован согласованный этап 1: состав типового объекта, правила проектирования, щит, маркировка, сценарии, ПНР, документация, границы ответственности инсталлятора |
| Связанный workspace | [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/README]] |

## Бизнес-результат

У команды есть проверяемый и версионируемый стандарт автоматизации iRidi, который можно использовать для обучения, пресейла, проектирования, поддержки, Wiki и агентской обработки входящих.

## Границы проекта

| Входит | Не входит без отдельного approve |
| --- | --- |
| Сбор и review предложений по стандарту | Прямая публикация в Google Doc |
| Классификация изменений `E0-E7` | Публикация во внешнюю Wiki |
| Поддержка карты разделов и changelog | Перенос raw транскриптов в стандарт |
| Связь с P4, Wiki, Bus77 и ККЗ | Автоматическое изменение канона из одной встречи |

## Approve Gates

- Любое изменение канона стандарта: `proposal -> approve -> apply -> archive`.
- Публичные материалы Wiki: отдельный review на границы публикации.
- Внешние записи в Google Doc, Wiki, Google Sheets, Redmine, Bitrix или Telegram: только после явного approve.
- Личные, конфиденциальные и сырые источники: не переносить в канон; использовать только source locator и короткий approved extract.

## Текущий статус

| Область | Статус |
| --- | --- |
| Паспорт проекта | есть, требует уточнения `passport_uid` |
| Project type | `C7`, valid |
| Documentation package | оформлен как индекс в [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/README]] |
| Open review | [[01_Projects/001_77_Standard_iRidi/Reviews/2026-07-15_Transcribe_Backlog_Route_Review]] |
| Workspace proposals | [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-07-08_standard-book-publishing-pipeline/proposal]], [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-07-18_track-lighting-classification/proposal]] |

## Следующий gate

Закрыть содержательный review [[01_Projects/001_77_Standard_iRidi/Reviews/2026-07-15_Transcribe_Backlog_Route_Review]]: подтвердить, отклонить или уточнить, какие изменения по питанию/монтажу Bus77 можно превращать в proposal стандарта и какие идут только в Wiki-кандидаты.
