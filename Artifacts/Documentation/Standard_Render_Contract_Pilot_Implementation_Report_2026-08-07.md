---
type: implementation_report
status: completed_for_review
created: 2026-08-07
project: 77 Standard iRidi
project_id: "001"
privacy: internal
action_id: operate_standard_book
source_ref: "[[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review]]"
contract_uid: std_render_contract_v1_candidate
---

# Отчет: пилот контракта генерации книги

Связано с [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_render_contract_candidate_v1.yaml]] и [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-PARITY-001_Independent_Reconstruction_Certification]].

## Результат

В единый CLI добавлена выборочная сборка по `section UID`. Пилот «Освещение» и полное превью используют один `standard-normalized` renderer, один `book.yaml` и одинаковые правила обработки заголовков, списков, таблиц и изображений.

## Execution trace

| Поле | Значение |
| --- | --- |
| Tool/action | `standard_book.py build`, action `operate_standard_book` |
| Код | `Workspace/77_Стандарт_iRidi/tooling/standard_book.py` |
| Новая команда | `build ... --section std_ch_lighting` |
| Контракт | `Artifacts/Machine_Readable/standard_render_contract_candidate_v1.yaml` |
| Review | `Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review.md` |
| Private build root | `Workspace/77_Стандарт_iRidi/build/contract-pilot/` |

## Проверки

- source validation: PASS, 17 разделов, 276 тем, 0 approved typed rules;
- unit tests: PASS, 7 tests;
- Lighting HTML: 64 topic headings, 37 таблиц, 107 изображений, 0 missing image links;
- full-book HTML: 276 topic headings, 150 таблиц, 437 изображений, 0 missing image links;
- Lighting DOCX: 37 таблиц, 107 inline shapes, ZIP integrity PASS;
- full-book DOCX: ZIP integrity PASS;
- landing page `START_HERE.html` проверена headless Chrome;
- scoped CORD rail: project type valid, artifact coverage has no missing rows, dashboard audit has 0 findings;
- generated book, images and QA screenshots остаются под `**/build/` и не попадают в Git.

## Исправление, найденное визуальным пилотом

Первый HTML-render дублировал заголовок темы: один раз из реестра и второй раз из legacy content. Генератор исправлен так, чтобы совпадающий первый заголовок не повторялся. Разрозненные legacy list paragraphs теперь собираются в один список без потери inline images. Оба случая закреплены тестами.

## Оставшиеся ограничения и gates

- `std_render_contract_v1_candidate` остается proposal до ответа владельца;
- содержательный рефакторинг «Освещения» не начат и требует утвержденного RC1;
- 96 lighting rule candidates не утверждены;
- LibreOffice отсутствует, поэтому DOCX прошел структурную, но не постраничную PNG-проверку;
- D8, cutover и внешняя публикация не выполнены и не разрешены этим Do.
