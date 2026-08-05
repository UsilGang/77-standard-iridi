---
type: integration_map
project: 77 Стандарт iRidi
status: active
updated: 2026-07-09
source_ref: "[[01_Projects/000_CORD_System/Archive/Reviews/Applied/2026-07-08_Project_77_Fit_Report]]"
---

# Карта интеграции проекта 77 в CORD

## Роль в vault

| Слой CORD | Как работает для 77 |
| --- | --- |
| Collect | Сырье попадает в `00_Inbox/Raw_Collector` или во внешние источники: транскрипты, Drive, Sheets, Wiki, Bitrix |
| Organize | Обработанная выжимка создается в `01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/YYYY-MM-DD_slug` |
| Review | Автор раздела / Василий проверяет `proposal.md`, класс изменения, риски и целевые разделы |
| Do | После approve обновляются Google Doc, Wiki, remarks, changelog, archive |

## Где находится workspace

Рабочая структура стандарта находится здесь: `01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi`.

MOC проекта остается основной точкой входа:

- [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]]
- [[03_Resources/Standard_Book/Standard_Book_MOC]]
- [[07_Source_Registry/Source_Registry]]

## Основные маршруты

| Источник | Первый слой | Проектный слой | Выход |
| --- | --- | --- | --- |
| экспертный совет | Raw Collector | `01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox` | proposal в стандарт |
| релиз продукта | Raw Collector | `01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox` | правки стандарта/Wiki |
| фидбек продаж | Raw Collector | `01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox` или sales organizer | уточнение формулировок |
| Panel P4 | проект P4 | `01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox` | обновление разделов 4/12/13/15/17 |
