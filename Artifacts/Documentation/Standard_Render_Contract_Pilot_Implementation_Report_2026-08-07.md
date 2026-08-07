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
feedback_ref: "user browser comments 2026-08-07: heading markers, readable margins, and LED table geometry"
---

# Отчет: пилот контракта генерации книги

Связано с [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review]], [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Full_Book_Migration_And_Agent_Access_Audit]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_render_contract_candidate_v1.yaml]] и [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-PARITY-001_Independent_Reconstruction_Certification]].

## Результат

В единый CLI добавлена выборочная сборка по `section UID`. Пилот «Освещение» и полное превью используют один `standard-normalized` renderer, один `book.yaml` и одинаковые правила обработки заголовков, списков, таблиц и изображений.

## Execution trace

| Поле | Значение |
| --- | --- |
| Tool/action | `standard_book.py build`, action `operate_standard_book` |
| Код | `Workspace/77_Стандарт_iRidi/tooling/standard_book.py` |
| Новая команда | `build ... --section std_ch_lighting` |
| Контракт | `Artifacts/Machine_Readable/standard_render_contract_candidate_v1.yaml` |
| Контракт таблиц | `Workspace/77_Стандарт_iRidi/tooling/table_layout_contract.yaml` |
| Review | `Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review.md` |
| Private build root | `Workspace/77_Стандарт_iRidi/build/contract-pilot/` |

## Проверки

- source validation: PASS, 17 разделов, 276 тем, 0 approved typed rules;
- unit tests: PASS, 16 tests;
- Lighting HTML: 62 public topic anchors, 37 таблиц, 107 изображений, 0 missing image links;
- full-book HTML: 261 public topic anchors, 146 таблиц, 441 изображение, 0 missing image links;
- Lighting DOCX: 37 таблиц, 107 inline shapes, ZIP integrity PASS;
- full-book DOCX: 146 таблиц, 441 drawings, 534 bookmarks, 0 image placeholders, ZIP integrity PASS;
- landing page `START_HERE.html` проверена headless Chrome;
- exact browser regression: `5.3.2.1.2. Принцип фазового диммирования` — tag `H3`, literal `####` absent;
- HTML layout at 1280 px: centered 1040 px paper, 120 px outer margins plus 80 px inner padding;
- LED table browser regression: `table-headerless`, 0 `thead`, 5 строк по 2 `td`, колонки `60%/40%`, первая строка без заливки, горизонтального переполнения нет;
- LED table DOCX regression: fixed grid, 5 строк, 2 колонки, ширины `5443/3629` DXA;
- scoped CORD rail: project type valid, artifact coverage has no missing rows, dashboard audit has 0 findings;
- generated book, images and QA screenshots остаются под `**/build/` и не попадают в Git.

## Исправление, найденное визуальным пилотом

- Первый HTML-render дублировал заголовок темы. Совпадающий первый заголовок теперь не повторяется.
- Разрозненные legacy list paragraphs собираются в один список без потери inline images.
- По browser feedback заголовки `####`–`######` внутри темы нормализуются в `Heading 3` в HTML и DOCX; literal Markdown markers исчезли.
- По browser feedback HTML получил ограниченную читаемую колонку и адаптивные боковые поля.
- По browser feedback восстановлена семантика таблицы видов LED-лент: исходный Google baseline содержит 5 строк без заголовка, ширины `243/162 pt` и объединение второй ячейки на две source-колонки. Контракт удаляет пустую extraction-колонку, фиксирует две эффективные колонки `60/40`, не красит первую строку и ограничивает изображения размером ячейки.

Все случаи закреплены детерминированными тестами и проверены повторной сборкой раздела и всей книги. Дополнительно введены semantic UID, node kinds, fragments, domain-first query и отрицательный anti-hallucination test; полный evidence — в [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Full_Book_Migration_And_Agent_Access_Audit]].

## Оставшиеся ограничения и gates

- `std_render_contract_v1_candidate` остается proposal до ответа владельца;
- содержательный рефакторинг «Освещения» не начат и требует утвержденного RC1;
- 96 lighting rule candidates не утверждены;
- LibreOffice отсутствует, поэтому DOCX прошел структурную, но не постраничную PNG-проверку;
- D8, cutover и внешняя публикация не выполнены и не разрешены этим Do.
