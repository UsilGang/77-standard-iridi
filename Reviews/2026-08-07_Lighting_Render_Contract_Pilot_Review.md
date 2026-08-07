---
type: standard_contract_review
status: review
created: 2026-08-07
project: 77 Standard iRidi
project_id: "001"
privacy: internal
review_uid: std_review_render_contract_pilot_20260807
contract_uid: std_render_contract_v1_candidate
pilot_section_uid: std_ch_lighting
source_ref: "user: pilot on one large section, full-book preview in parallel, approve contract before scaling"
machine_contract_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_render_contract_candidate_v1.yaml]]"
template_contract_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_template_contract_candidate_v1.yaml]]"
decision_required: approve_or_revise
action_id: operate_standard_book
blocker: needs_human_decision
feedback_refs:
  - "user browser comment 2026-08-07: deep Markdown headings rendered literally"
  - "user browser comment 2026-08-07: content column had no readable side margins"
---

# Согласование контракта книги: пилот «Освещение»

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_render_contract_candidate_v1.yaml]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Render_Contract_Pilot_Implementation_Report_2026-08-07]] и [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-PARITY-001_Independent_Reconstruction_Certification]].

## Что открыть и в каком порядке

1. Сначала открыть нормализованное превью раздела «Освещение» в HTML. Это основная поверхность согласования структуры, таблиц и изображений.
2. Если принцип на разделе понятен, открыть полное HTML-превью книги. Оно собрано тем же кодом, тем же профилем и из того же `book.yaml`.
3. DOCX обеих сборок лежит рядом с HTML и предназначен для проверки формата будущего распространяемого документа.

Локальные сборки не коммитятся и не публикуются, потому что содержат полный текст и изображения книги:

- `Workspace/77_Стандарт_iRidi/build/contract-pilot/lighting-normalized/standard-standard-normalized.html`;
- `Workspace/77_Стандарт_iRidi/build/contract-pilot/full-normalized/standard-standard-normalized.html`.

## Что именно предлагается утвердить

Одно решение утверждает контракт `std_render_contract_v1_candidate`:

- источником книги является адресуемая цепочка `book -> section -> topic -> content`, а не вручную редактируемый итоговый DOCX;
- «Освещение» является первым глубоким разделом для согласования, но обязательный масштаб — вся книга;
- раздел и вся книга собираются одним генератором, а не двумя расходящимися шаблонами;
- порядок разделов и тем берется из реестров, заголовки строятся по единой иерархии;
- таблицы и изображения входят в контракт, сохраняют порядок, а потерянный или неподдерживаемый объект обязан дать видимый маркер ошибки;
- любая глубина legacy-заголовка внутри темы нормализуется в единый подзаголовок без видимых `####`;
- HTML имеет читаемую колонку до 1040 px с адаптивными боковыми полями;
- HTML является быстрой поверхностью проверки, DOCX — кандидатом распространяемой книги;
- каждое будущее смысловое изменение проходит через редакционное задание, UID изменения и changeset.

## Что этим решением не утверждается

- правильность всех старых формулировок и норм;
- 96 кандидатов норм раздела «Освещение»;
- отсутствие человеческих ошибок в исходной книге;
- пиксельное равенство исходной и новой книги;
- независимая приемка D8, cutover и внешняя публикация.

После утверждения контракта содержимое «Освещения» можно рефакторить по утвержденному шаблону. Все исправления старой книги должны быть объяснены отдельными transformation operations, а не спрятаны в генераторе.

## Что уже доказано пилотом

| Проверка | «Освещение» | Вся книга |
| --- | ---: | ---: |
| Разделы | 1 | 17 |
| Адресуемые темы | 64 | 276 |
| HTML-таблицы | 37 | 150 |
| HTML-изображения | 107 | 437 |
| Потерянные ссылки на изображения | 0 | 0 |
| DOCX-таблицы | 37 | структурно проверено |
| DOCX inline images | 107 | структурно проверено |
| Целостность DOCX ZIP | PASS | PASS |

Текущие SHA-256 после обратной связи: для «Освещения» DOCX `dd20e8e3...36bcd`, HTML `255bd270...dfaa2`; для всей книги DOCX `d526fb64...38e2f`, HTML `57166b87...6786d`. Изменения объяснимы: deep headings нормализованы, HTML-колонка получила читаемые поля; текст, 37/150 таблиц и 107/437 изображений сохранены.

Ограничение текущей проверки: на машине отсутствует LibreOffice, поэтому DOCX не прошел обязательный постраничный PNG-render. Выполнена структурная проверка DOCX; основной визуальной поверхностью этого review является HTML. Постраничная визуальная приемка DOCX остается обязательной частью D8.

## Как ответить

Достаточно одной фразы:

- `Утверждаю контракт RC1` — фиксируем контракт и начинаем содержательный рефакторинг «Освещения»;
- `Нужно поправить: ...` — меняем контракт и обе сборки, затем повторяем review.

Утверждение RC1 не является утверждением содержания всей книги или разрешением на публикацию.
