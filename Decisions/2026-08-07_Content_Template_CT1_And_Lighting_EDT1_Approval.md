---
type: decision
status: applied_to_do
created: 2026-08-07
project: 77 Standard iRidi
project_id: "001"
privacy: internal
origin: human
source_ref: "[[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-08-07_Content_Template_And_Lighting_EDT_Review]]"
approval_ref: "user: Давай"
approved_decisions: [CT1, EDT1]
template_contract_uid: standard_templates_1
editorial_job_uid: EDT-2026-0001
external_write: false
publication_allowed: false
---

# Решение: утвердить CT1 и EDT1

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-08-07_Content_Template_And_Lighting_EDT_Review]], [[01_Projects/001_77_Standard_iRidi/Archive/Backlog/Done/DO-001-STD-LIGHTING-REF-001_Refactor_Lighting_Content]] и [[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-07_Standard_Render_Contract_RC1_Approval]].

## Утверждено

- CT1: разные шаблоны для сборки раздела и для одной адресуемой темы;
- `tpl_subsystem_section_v1`, каталог topic archetypes и explicit missing-slot policy;
- initial slot map групп 5.1–5.14;
- EDT-2026-0001 на локальный трассируемый рефакторинг всех 64 тем раздела «Освещение»;
- операции `format_normalize`, `renumber`, `move`, `split`, `merge`, `deduplicate`, `type_separate`, `clarify` без смены смысла.

## Не утверждено

- 96 lexical rule candidates и любые новые/измененные нормы;
- новые product facts, удаление, deprecation и разрешение конфликтов;
- заполнение отсутствующих знаний догадкой;
- D8, cutover, Google Doc, Wiki и публикация.

## Исполнение

Do `DO-001-STD-LIGHTING-REF-001` активирован. Результат должен вернуться сравнительным review-пакетом с transformation manifest, builds, agent-query checks и отдельными semantic decisions.
