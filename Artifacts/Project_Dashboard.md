---
type: project_dashboard
status: active
created: 2026-07-12
project: 77 Standard iRidi
project_id: "001"
project_type_id: "C7"
project_slug: "001_77_Standard_iRidi"
source_ref: "[[01_Projects/010_Product_Key_Tasks/Archive/Reviews/Applied/2026-07-13_Full_Key_Task_Project_Type_Approval_Review]]"
stage: active
owner: Василий
reviewer: Василий
understanding_status: draft
responsible: ["Татаринов"]
executors: ["Татаринов"]
key_task_uids: ["kt_e61095d3fb09"]
passport_uid: "needs_passport_review:77_standard_iridi"
roadmap_ids: []
source_ids: ["CORD backfill 2026-07-10", "key_task:kt_e61095d3fb09"]
source_count: 2
source_types: ["key_task_log"]
source_date_min: ""
source_date_max: ""
review_ids: ["2026-07-15_Transcribe_Backlog_Route_Review", "2026-08-07_Lighting_Render_Contract_Pilot_Review", "2026-08-05_Lighting_Rule_Candidates_Expert_Review"]
decision_ids: ["2026-08-05_Standard_As_Code_Architecture_D1_D11"]
open_question_ids: ["std_render_contract_v1_candidate"]
backlog_ids: ["DO-001-KKZ-SWEEP-001", "DO-001-STD-PARITY-001"]
downstream_project_ids: []
upstream_project_ids: []
property_profile: generic_project
last_sync_at: 2026-08-07
last_sync_ref: "[[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review]]"
privacy: internal
---

# Project Dashboard: 77 Standard iRidi

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Passport]] и [[05_Templates/Project_Dashboard]].

## Current Understanding

- Проект поддерживает «Стандарт автоматизации iRidi» как продуктовый knowledge-cycle: систематизирует уже выпущенные продукты, оформляет их в книге/стандарте и регулярно обновляется при новых релизах и правках.
- Full-book baseline уже переведен в адресуемый source layer. Контракт генерации согласуется на крупном разделе «Освещение», а полная книга одновременно собирается тем же renderer.

## Confirmed

- Project folder: `01_Projects/001_77_Standard_iRidi`.
- Owner: Василий.
- Reviewer: Василий.
- Пилот RC1 собран: 1 раздел, 64 темы, 37 таблиц и 107 изображений; полное превью включает 17 разделов и 276 тем.
- Browser feedback RC1 применен: deep Markdown headings нормализованы в `Heading 3`, HTML получил читаемую колонку и адаптивные боковые поля.

## Assumptions

- Dashboard создан как backfill обязательного CORD property layer; содержательное наполнение уточняется при следующем project-run.
- `passport_uid` пока `needs_passport_review:77_standard_iridi`, потому что паспортная сущность книги не подтверждена отдельным источником.

## Open Questions

- Решить review [[01_Projects/001_77_Standard_iRidi/Reviews/2026-07-15_Transcribe_Backlog_Route_Review]] по двум Transcribe-сигналам.
- Утвердить или скорректировать `std_render_contract_v1_candidate` по [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review]].

## Next Do

- Владельцу пройти одну точку решения: [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Render_Contract_Pilot_Review]]. После approve — рефакторинг «Освещения» по утвержденному шаблону с объяснимыми delta.

## Review Queue

- Проверять через scoped queue проекта.

## Downstream Routes

- TBD.

## Source Anchors

- CORD backfill 2026-07-10
- [[01_Projects/001_77_Standard_iRidi/Sources/Key_Task_Log_N31_kt_e61095d3fb09]]

## Machine-Readable Properties

- Canonical properties are in frontmatter.
- Linked registers: TBD.
