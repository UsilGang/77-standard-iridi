---
type: standard_content_contract_review
status: review
created: 2026-08-07
project: 77 Standard iRidi
project_id: "001"
privacy: internal
review_uid: std_review_content_template_lighting_edt_20260807
template_contract_uid: standard_templates_1_candidate
editorial_job_uid: EDT-2026-0001
source_ref: "user: давай, давай after RC1 approval"
proposal_ref: "[[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-08-07_lighting-content-template-pilot/proposal]]"
decision_required: approve_or_revise
action_id: operate_standard_book
blocker: needs_human_decision
canonical_change: false
external_write: false
---

# Согласование CT1 и первого редакционного задания

Связано с [[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-07_Standard_Render_Contract_RC1_Approval]], [candidate-контрактом CT1](../Artifacts/Machine_Readable/standard_template_contract_candidate_v1.yaml), [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-08-07_lighting-content-template-pilot/brief]] и [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-LIGHTING-REF-001_Refactor_Lighting_Content]].

## Решение в двух строках

1. `CT1`: раздел и отдельная тема получают разные шаблоны; отсутствующий обязательный блок показывается как gap и блокирует release.
2. `EDT1`: по этому контракту локально рефакторится весь раздел «Освещение» — 64 темы и группы 5.1–5.14, а не один удобный подраздел.

## Почему candidate изменен

Предыдущая версия смешивала уровень раздела и темы. В результате каждую отдельную тему можно было ошибочно заставить содержать архитектуру, оборудование, монтаж, ПНР и приемку всей подсистемы. В CT1:

| Уровень | За что отвечает |
| --- | --- |
| `tpl_subsystem_section_v1` | порядок смысловых модулей всего раздела |
| topic archetype | контракт одного адресуемого ответа: понятие, технология, оборудование, инструкция, сравнение, room pattern или кейс |

## Карта раздела, которую утверждает CT1

| Исходные группы | Целевой смысловой модуль |
| --- | --- |
| 5.1 | ценность |
| 5.2, 5.6 | scope, термины и классификация |
| 5.3–5.4 | технологии, источники и выбор |
| 5.5 | рекомендуемая архитектура |
| 5.7 | сценарии |
| 5.8–5.9 | оборудование, датчики и применение |
| 5.10–5.11 | кабели, схемы и монтаж |
| 5.12 | best practices и ограничения |
| 5.13–5.14 | room patterns и пример реализации |

Настройка/ПНР и приемочные испытания сейчас не имеют достаточных самостоятельных блоков. CT1 не придумывает их, а делает gaps видимыми.

## Что показал повторный аудит пустых документов

- девять коротких файлов — это контейнеры оглавления, а не потерянный текст;
- один файл — source attachment и не должен публиковаться как самостоятельный ответ;
- тема 5.3 содержит только вводную фразу и требует merge/disposition;
- тема 5.14 содержит черновой placeholder «тут накидываем проектов на Bus77» и блокируется для release до появления утвержденного примера.

CT1 закрепляет это системно: container/attachment получают отдельные archetypes и не попадают в agent answers, а настоящий недостающий content становится видимым gap.

## Что разрешает EDT1

- учитывать весь раздел 5 и всех его descendants;
- нормализовать оформление и нумерацию;
- перемещать, разделять, объединять, дедуплицировать и уточнять материал без смены смысла;
- отделять fact, rule candidate, rationale, example, procedure и warning;
- пересобрать «Освещение» и всю книгу и показать explained delta.

## Что остается отдельным решением

- любой из 96 lexical rule candidates;
- новый или измененный product fact;
- конфликт, удаление, deprecation или новая норма;
- заполнение gaps по ПНР и приемке;
- D8, cutover, Google Doc, Wiki и публикация.

## Критерий возврата результата

Результат придет не просьбой перечитать всю книгу, а сравнительным пакетом:

- 64/64 темы имеют archetype, target slot и disposition;
- 100% текста, таблиц и изображений имеют source trace и target/disposition;
- все изменения перечислены по operation UID;
- неутвержденные нормы и отсутствующие знания вынесены отдельно;
- раздел и полная книга собраны одним renderer;
- агентские вопросы проверены на documented/gap behavior.

## Как ответить

- `Утверждаю CT1 и EDT1` — активировать шаблон и начать локальный рефакторинг «Освещения»;
- `Нужно поправить: ...` — изменить контракт/задание и вернуть обновленный пакет.

Это решение не разрешает внешнюю публикацию.
