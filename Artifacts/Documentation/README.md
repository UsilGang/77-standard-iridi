---
type: documentation_package
status: active
project: 77 Standard iRidi
project_id: "001"
project_type_id: "C7"
created: 2026-07-20
updated: 2026-08-07
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/README]]"
---

# Documentation Package: 77 Standard iRidi

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Creation_Brief]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Package_Index]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Quality_Gates]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Integration_Map]] и [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/README]].

## Назначение

Этот пакет показывает, где лежат рабочие и публикационные материалы стандарта. Он не является текстом стандарта и не заменяет Google Doc. Его задача - дать агенту и человеку быстрый маршрут: где источник, где proposal, где versioning, где approve gate.

## Состав пакета

| Артефакт | Где | Статус | Как использовать |
| --- | --- | --- | --- |
| Project brief | [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Creation_Brief]] | active | объясняет, зачем проект существует и какие gates обязательны |
| Package index | [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Package_Index]] | active | дает scannable состав documentation package |
| Integration map | [[01_Projects/001_77_Standard_iRidi/Artifacts/Integration_Map]] | active | показывает, как CORD связан с workspace стандарта |
| Quality gates | [[01_Projects/001_77_Standard_iRidi/Artifacts/Quality_Gates]] | active | проверяет proposal до approve/apply |
| Review rhythm | [[01_Projects/001_77_Standard_iRidi/Artifacts/Review_Rhythm]] | active | задает ритм ревью стандарта |
| Versioning | [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/VERSIONING]] | active | правила версионирования книги |
| Workspace inbox | [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/README]] | active | source-owned proposal queue |
| Workspace archive | [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/archive/README]] | active | resolved proposals |
| Current book audit | [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]] | draft_for_review | фактическая структура вкладок, таблиц, изображений и проблем миграции |
| Standard as Code architecture | [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]] | approved_design | модель артефактов, UID, versioning, build, MCP и migration plan |
| Machine-readable book manifest candidate | [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/Standard_Book_Manifest_MOC]] | proposal | draft bridge к текущей структуре Google Doc; не канон и не build input |
| Reconstruction parity acceptance | [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Reconstruction_Parity_Acceptance_v1]] | active_requirement | независимые G1–G8, evidence package и строгий PASS/FAIL цикл |
| Content refactoring and templates | [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]] | approved_design | lossless import, normalized canon, archetypes и защита от побочных правил |
| Editorial assignment and versioning | [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]] | approved_design | EDT contract, text/visual brief, unit revisions, draft builds и release SemVer |
| Audiences and agent knowledge access | [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]] | approved_design | человеческие аудитории, machine applications, физическое разделение слоев, generated agent package и query/audit contract |
| Full migration and agent access audit | [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Full_Book_Migration_And_Agent_Access_Audit]] | completed_for_review | exact сверка baseline/source/build, semantic UID, node kinds, agent queries и известные manual gates |

## Текущие открытые предложения

| Proposal | Что меняет | Gate |
| --- | --- | --- |
| [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-07-08_standard-book-publishing-pipeline/proposal]] | publishing workflow and source-of-truth модель книги | требует решения по переходному процессу |
| [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-07-18_track-lighting-classification/proposal]] | классификация трековых систем освещения | требует проверки автором раздела освещения |
| [[01_Projects/001_77_Standard_iRidi/Reviews/2026-07-15_Transcribe_Backlog_Route_Review]] | кандидаты по питанию/монтажу Bus77 из Transcribe | требует approve/revise/reject |

## Утвержденная реализация

- Решение: [[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-05_Standard_As_Code_Architecture_D1_D11]].
- Исполненный Do: [[01_Projects/001_77_Standard_iRidi/Archive/Backlog/Done/DO-001-STD-AS-CODE-001_Implement_Approved_Architecture]].
- Принято D1-D7,D9-D11; D8 остается отдельной независимой приемкой после готовности полной сборки.

Отдельная задача полного подтверждения после сборки: [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-PARITY-001_Independent_Reconstruction_Certification]]. Она ожидает полный baseline/source/build candidate и не заменяется самопроверкой renderer.

## Правило публикации

Утвержденная архитектура разрешает локальную реализацию и read-only миграцию источника. Google Doc, Wiki, внешние системы и публикация полного текста книги в публичный Git не меняются автоматически.
