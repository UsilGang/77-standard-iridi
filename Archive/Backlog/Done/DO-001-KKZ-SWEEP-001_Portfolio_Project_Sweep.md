---
type: do_action
status: done
project: 77 Standard iRidi
project_id: "001"
id: DO-001-KKZ-SWEEP-001
action_id: portfolio_project_sweep
created: 2026-07-18
updated: 2026-07-20
completed: 2026-07-20
owner: Василий Татаринов
executor: agent
privacy: confidential
source_ref: "[[01_Projects/010_Product_Key_Tasks/Artifacts/Portfolio_Project_Sweep_2026-07-18]]"
write_guard: local_only
result_ref: "[[01_Projects/001_77_Standard_iRidi/QA/Project_Artifact_Coverage_Report]]"
---

# DO-001-KKZ-SWEEP-001: Portfolio Project Sweep

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Passport]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Dashboard]] и [[01_Projects/010_Product_Key_Tasks/Artifacts/Portfolio_Do_Register]].

## Цель

Довести локальную постановку проекта до состояния, где по связанным ККЗ понятно: какие источники уже осаждены, какие обязательные артефакты отсутствуют, какой следующий проверяемый шаг нужен и что нельзя писать наружу без отдельного approve.

## Связанные ККЗ

- `kt_e61095d3fb09`: Подготовить, согласовать и опубликовать материалы по «Книга "стандарт автоматизации" (этап 1)». см. iRidi ККЗ KR НИОКР Ключевых проектов и задачи

## Source Logs

- [[01_Projects/001_77_Standard_iRidi/Sources/Key_Task_Log_N31_kt_e61095d3fb09]]

## Проверка Sweep

| Поле | Значение |
| --- | --- |
| Project type | `C7` / `valid` |
| Passport quality | `D` |
| Project progress | `25%` |
| Missing artifacts | 3 |
| Manual checks | 1 |
| Open reviews | 1 |
| Open backlog | 0 |
| Artifact gaps | `project_creation_brief:missing; documentation_package:missing; weekly_status:manual_check; artifact_coverage:missing` |

## Следующий Шаг

1. Открыть project-local source logs и не спрашивать повторно то, что уже есть в ККЗ-логе.
2. Закрыть первый artifact gap: `project_creation_brief:missing; documentation_package:missing; weekly_status:manual_check; artifact_coverage:missing`.
3. Если нужен внешний владелец, подготовить адресный draft с `key_task_uid`, проектом, недостающим артефактом, зачем он нужен и done criteria.
4. Перед любой записью в Google Sheets/Redmine/Bitrix/Telegram выполнить отдельную проверку цели публикации и получить explicit approve.

## Done Criteria

- По каждому `key_task_uid` есть source anchor.
- Missing artifacts либо созданы локально, либо имеют вопрос/decision `not_applicable` с источником.
- Следующий статус в ККЗ можно подтвердить без номера строки как идентификатора.

## Result

Выполнено локально без внешних записей:

- создан [[01_Projects/001_77_Standard_iRidi/Artifacts/Project_Creation_Brief]];
- создан [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/README]];
- создан [[01_Projects/001_77_Standard_iRidi/QA/Project_Artifact_Coverage_Report]];
- обновлены [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/artifact_index.csv]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/project_rail_state.csv]] и [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/external_refs.csv]].

Оставшийся gate не является этим Do: содержательный review [[01_Projects/001_77_Standard_iRidi/Reviews/2026-07-15_Transcribe_Backlog_Route_Review]] требует human approve/revise/reject перед изменением стандарта.
