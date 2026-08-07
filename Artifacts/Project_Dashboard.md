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
review_ids: ["2026-07-15_Transcribe_Backlog_Route_Review", "2026-08-07_Lighting_Render_Contract_Pilot_Review", "2026-08-07_Full_Book_Migration_And_Agent_Access_Audit", "2026-08-07_Full_Render_Parity_Self_Audit", "2026-08-05_Lighting_Rule_Candidates_Expert_Review", "2026-08-07_Content_Template_And_Lighting_EDT_Review"]
decision_ids: ["2026-08-05_Standard_As_Code_Architecture_D1_D11", "2026-08-07_Standard_Render_Contract_RC1_Approval", "2026-08-07_Content_Template_CT1_And_Lighting_EDT1_Approval"]
open_question_ids: ["2026-08-07_Lighting_Content_Gaps_Expert_Review", "D8-independent-certification"]
backlog_ids: ["DO-001-KKZ-SWEEP-001", "DO-001-STD-PARITY-001"]
downstream_project_ids: []
upstream_project_ids: []
property_profile: generic_project
last_sync_at: 2026-08-07
last_sync_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Reports/2026-08-07_Lighting_CT1_EDT1_Implementation_Report]]"
privacy: internal
---

# Project Dashboard: 77 Standard iRidi

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Passport]] и [[05_Templates/Project_Dashboard]].

## Current Understanding

- Проект поддерживает «Стандарт автоматизации iRidi» как продуктовый knowledge-cycle: систематизирует уже выпущенные продукты, оформляет их в книге/стандарте и регулярно обновляется при новых релизах и правках.
- Full-book baseline уже переведен в адресуемый source layer. Контракт генерации RC1 утвержден на крупном разделе «Освещение» и применяется тем же renderer к полной книге.
- Вся книга получила стабильные semantic UID и agent package с фрагментами, связями, aliases и доменной маршрутизацией. Lossless source и Buffer физически отделены от generated package.

## Confirmed

- Project folder: `01_Projects/001_77_Standard_iRidi`.
- Owner: Василий.
- Reviewer: Василий.
- Пилот RC1 собран: 1 раздел, 64 темы, 37 таблиц и 107 изображений; полное превью включает 17 разделов и 276 тем.
- Browser feedback RC1 применен: deep Markdown headings нормализованы в `Heading 3`, HTML получил читаемую колонку и адаптивные боковые поля.
- Table feedback RC1 применен: таблица видов LED-лент восстановлена как пять строк данных без ложной шапки, с двумя фиксированными колонками `60/40`; правило заголовков и геометрии теперь машиночитаемо и одинаково для HTML/DOCX.
- Повторная full-book сверка PASS: 18 вкладок, 6 758 блоков, 276 topic content, 146 таблиц и 471 source asset совпадают с baseline.
- Agent package: 261 самостоятельный узел, 4 947 фрагментов, 267 связей, 441 изображение; Buffer не включен.
- Полный render parity self-audit применяет три класса finding. После автоматических исправлений: 5 924/5 924 content lines, 146/146 tables, 441/441 published images, 0 broken links/anchors, 0 browser overflow на 1600/1024/640 px.
- Нормализованные HTML/DOCX получили оглавление, переходы между темами и восстановление source inline formatting; ложная шапка таблицы ONOKOM устранена системным правилом.
- Владелец утвердил RC1; канонический машинный контракт теперь `std_render_contract_v1`. Содержательный template contract, нормы, D8 и публикация этим решением не утверждены.
- CT1 candidate исправлен после проверки на реальных 64 темах: шаблон целого раздела физически отделен от topic archetypes; подготовлено EDT-2026-0001 на весь раздел «Освещение».
- CT1 и EDT-2026-0001 утверждены и применены: 64/64 темы имеют slot/archetype/disposition/operation trace, lossless content не переписан.
- Lighting normalized view: 14 модулей, 52 самостоятельные темы, 37 таблиц, 107 изображений и три явных knowledge gaps; все 107 image refs сопоставлены со слотами.
- Обновленный agent package: 231 topic/gap node, 4 918 fragments и slot index. Smoke-проверка 9/9; ПНР, приемка и ограничения возвращают gap, а не выдуманную норму.
- Повторные migration и browser audits прошли с 0 critical/material/cosmetic findings. D8 по-прежнему не self-certified.

## Assumptions

- Dashboard создан как backfill обязательного CORD property layer; содержательное наполнение уточняется при следующем project-run.
- `passport_uid` пока `needs_passport_review:77_standard_iridi`, потому что паспортная сущность книги не подтверждена отдельным источником.

## Open Questions

- Решить review [[01_Projects/001_77_Standard_iRidi/Reviews/2026-07-15_Transcribe_Backlog_Route_Review]] по двум Transcribe-сигналам.
- Решить [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Content_Gaps_Expert_Review]] по ПНР, приемке, ограничениям и примеру реализации.

## Next Do

- Выполнить независимый [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-PARITY-001_Independent_Reconstruction_Certification]]. D8 не закрывать по self-audit.

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
