---
type: project_source_route_review
status: review
project: 77 Standard iRidi
project_id: "001"
created: 2026-07-15
updated: 2026-07-15
source_type: transcribe
privacy: internal
blocker: needs_human_decision
source_register: "01_Projects/000_CORD_System/Reviews/2026-07-13_Transcribe_Backlog_Full_Content_Route_Register.tsv"
source_review_ref: "[[01_Projects/000_CORD_System/Archive/Reviews/Applied/2026-07-13_Transcribe_Backlog_Full_Content_Route_Review]]"
---

# Transcribe Backlog Route Review: 001_77_Standard_iRidi

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[07_Source_Registry/Transcribe_Source]], [[01_Projects/000_CORD_System/Reviews/2026-07-13_Transcribe_Backlog_Full_Content_Route_Register]] и [[01_Projects/000_CORD_System/Archive/Reviews/Applied/2026-07-13_Transcribe_Backlog_Full_Content_Route_Review]].

## Назначение

Этот пакет разносит approved Transcribe backlog в scope проекта `001_77_Standard_iRidi`. Он не канонизирует содержание записей и не пишет во внешние системы. Задача проектного агента: открыть только свои `source_ref`, отделить факт от интерпретации, предложить изменения в проект и дождаться approve перед Do.

## Что сделать в проекте

1. Проверить каждую запись по `source_id`, `collect_ref` и `source_ref`.
2. разобрать записи как кандидаты в изменение стандарта монтажа/питания Bus77 и отдельный Wiki-кандидат, без маршрута в Bus77 Protocol.
3. Для `possible_multi` и secondary routes сделать split, а не смешивать зависимость с primary route.
4. Не копировать raw transcript в проект; хранить source locator и короткий approved extract.
5. Не писать в Google Sheet, Redmine, Telegram, Wiki или другие внешние системы без отдельного approve.

## Сводка

- Записей в пакете: 2.
- Категории: `approved_route_correction`=2.
- Источник маршрута: `01_Projects/000_CORD_System/Reviews/2026-07-13_Transcribe_Backlog_Full_Content_Route_Register.tsv`.

## Источники

| Source | Запись | Категория | Что извлечь | Secondary routes | Collect item | Source ref |
| --- | --- | --- | --- | --- | --- | --- |
| `transcribe:2026-06-08_20-22-09_recording_a916d40e` | `2026/06/2026_06_08_20_22_09.mp3` | `approved_route_correction` | bus77_power_and_cabling_installation_rule | `003_iRidi_Wiki_Docs` | `00_Inbox/Raw_Collector/Archive/2026/07/20260708_transcribe_recording_2026-06-08_20-22-09_reco_acc66ea986.md` | `C:/AI/transcribe/outbox/recordings/inbox/2026/06/2026-06-08_20-22-09_recording_a916d40e` |
| `transcribe:2026-06-08_20-26-47_recording_253210fe` | `2026/06/2026_06_08_20_26_47.mp3` | `approved_route_correction` | bus77_power_and_cabling_installation_rule | `003_iRidi_Wiki_Docs` | `00_Inbox/Raw_Collector/Archive/2026/07/20260708_transcribe_recording_2026-06-08_20-26-47_reco_93477f993d.md` | `C:/AI/transcribe/outbox/recordings/inbox/2026/06/2026-06-08_20-26-47_recording_253210fe` |

## Decision Needed

- `approve`: проектный агент создает source trace и детальный review изменений проекта.
- `revise`: уточнить route/split/privacy.
- `reject`: оставить archive trace без проектного разбора.
