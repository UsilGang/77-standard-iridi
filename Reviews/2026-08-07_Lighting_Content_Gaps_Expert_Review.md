---
type: expert_review
status: review
date: 2026-08-07
project_id: "001"
section_uid: std_ch_lighting
editorial_job_uid: EDT-2026-0001
source_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Reports/2026-08-07_Lighting_CT1_EDT1_Implementation_Report]]"
privacy: internal
blocker: needs_human_decision
needed_decision: "Утвердить маршруты заполнения четырех gaps или оставить их явными пробелами стандарта."
---

# Нерешенные содержательные вопросы раздела «Освещение»

## Что не было додумано автоматически

| Gap UID | Что отсутствует | Что нужно для заполнения | Решение |
|---|---|---|---|
| `std_topic_lighting_setup_and_commissioning_gap` | Подтвержденная процедура настройки и ПНР | Проверенный порядок, роли, входы, контрольные точки и источник | отдельное EDT + эксперт |
| `std_topic_lighting_acceptance_tests_gap` | Приемочные критерии и измеримые проверки | Чек-лист, ожидаемые результаты, допуски и authority source | отдельное EDT + эксперт |
| `std_topic_lighting_limitations_and_anti_patterns_gap` | Подтвержденный набор ограничений и анти-паттернов | Разбор 96 lexical candidates и/или новые authoritative sources | отдельный rule/fact review |
| `std_topic_lighting_primer_realizatsii` | Утвержденный пример реализации | Реальный проверенный проект, ограничения, схема, результат и review | отдельное EDT + кейс |

## Предлагаемое решение

Оставить gaps опубликованными только во внутреннем normalized view и агентском пакете как маршрутизаторы редакционной недоработки. Не превращать их в технические утверждения до отдельных решений.

## Не входит в этот review

- утверждение любой из 96 lexical rule candidates;
- удаление исходного placeholder;
- публикация книги;
- независимая D8-проверка.
