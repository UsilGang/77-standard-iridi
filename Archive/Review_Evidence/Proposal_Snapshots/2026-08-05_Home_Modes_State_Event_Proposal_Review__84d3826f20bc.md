---
type: proposal_snapshot
status: frozen
created: 2026-08-05T13:39:22Z
project: "001_77_Standard_iRidi"
privacy: "internal"
original_review_ref: "01_Projects/001_77_Standard_iRidi/Reviews/2026-08-05_Home_Modes_State_Event_Proposal_Review.md"
content_sha256: "84d3826f20bc8038ad85a150120424c750ebf7ff77b8c4edb193a156af3292c1"
allowed_use: "decision_evidence+shadow_evaluation"
graph_exempt: false
---

# Proposal snapshot: 2026-08-05_Home_Modes_State_Event_Proposal_Review

Связано с [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-05_Home_Modes_State_Event_Proposal_Review]], [[03_Resources/Intelligence_Engine/Contracts/Record_Contracts_v1]] и [[03_Resources/Intelligence_Engine/Policies/Policy_Ledger]].

Immutable pre-decision copy. Do not edit; a changed proposal creates a new hash revision.

## Frozen review content

---
type: standard_proposal_review
status: review
project: 77 Standard iRidi
project_id: "001"
created: 2026-08-05
privacy: internal
blocker: needs_human_decision
source_id: "transcribe:2026-06-08_20-09-34_recording_30168e31"
proposal_ref: "[[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-08-05_home-modes-state-event/proposal]]"
---

# Review: режим как состояние и событие

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-08-05_home-modes-state-event/content]], [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-08-05_home-modes-state-event/proposal]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Quality_Gates]] и [[07_Source_Registry/Transcribe_Source]].

## Коротко

Фрагмент Transcribe подтвержден по source-owned расшифровке. Proposal предлагает убрать определение «режим — это виджет» и разделить два применения режима в правилах: смена/активация как событие и текущее значение как состояние-условие.

## R1 — направление текста

`approve` — принять черновик как направление для разделов 4.6/4.7 и передать на проверку автору раздела. Это не разрешает менять Google Doc, Wiki или remarks.

## R2 — класс изменения

`approve E2` — считать изменение дополнением существующего подраздела с PATCH-эффектом. Если текущий текст требует существенной переписки, выбрать `revise E3` до публикации.

## R3 — продуктовые границы

До проверки не утверждать взаимное исключение режимов, приоритеты, хранение после перезапуска и точные возможности Home/Studio/Project Tool.

## Варианты решения

- `approve R1-R3`: принять направление и оставить канон неизменным до авторской проверки и отдельного apply;
- `revise`: указать правки к термину, примерам, разделам или change class;
- `reject`: архивировать proposal без изменения книги.
