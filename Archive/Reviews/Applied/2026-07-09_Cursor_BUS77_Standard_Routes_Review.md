---
type: review_packet
status: applied
created: 2026-07-09
project: 77_Standard_iRidi
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Archive/Inbox/Routed/2026-07-09_Cursor_BUS77_Standard_Routes]]"
decision_ref: "[[01_Projects/001_77_Standard_iRidi/Decisions/2026-07-09_Cursor_BUS77_Standard_Routes_R1_R4]]"
---

# Cursor BUS77/Standard Routes Review

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Quality_Gates]], [[01_Projects/008_Bus77_Protocol_Knowledge/Bus77_Protocol_Knowledge_MOC]], [[03_Resources/Bus77_Device_API/Device_API_MOC]] и [[01_Projects/000_CORD_System/Archive/Reviews/Applied/2026-07-09_Cursor_Source_Full_Intake_Review]].

## Коротко

Cursor source layer показывает сигналы по Bus77 tool routes, Device API and standard flow. Для проекта 77 это не прямое изменение канона: протокольные сырьевые источники должны оставаться в [[01_Projects/008_Bus77_Protocol_Knowledge/Bus77_Protocol_Knowledge_MOC]], а в стандарт попадает только approved explanation/proposal.

## Organize proposal

| Project / Candidate | Что положить | Почему сюда | Куда положить | Source ref | Action after approve |
| --- | --- | --- | --- | --- | --- |
| [[01_Projects/008_Bus77_Protocol_Knowledge/Bus77_Protocol_Knowledge_MOC]] | Raw/source knowledge по Bus77 protocol, Device API, SDK, reference implementations, collision checks. | Это протокольная база, а не текст стандарта для инсталляторов. | Sources / Artifacts / QA protocol log | [[01_Projects/000_CORD_System/Archive/Reviews/Applied/2026-07-09_Cursor_Source_Full_Intake_Review]] | Держать как source-owned protocol project. |
| [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]] | Candidate proposal: какие проверенные protocol explanations нужны для раздела 4 и связанных разделов стандарта. | Стандарту нужны только применимые правила и объяснения, прошедшие review. | `Workspace/77_Стандарт_iRidi/inbox` после отдельного approve | этот review | Создать standard proposal candidate, если пользователь approve R2. |
| [[03_Resources/Bus77_Device_API/Device_API_MOC]] | Ссылку на Device API как черновой/проверяемый источник, не public canon. | Device API сейчас требует product/firmware approve перед публикацией. | Resource MOC already exists | [[07_Source_Registry/Source_Registry]] | Не менять, только ссылаться как source. |
| [[01_Projects/002_Panel_P4_BUS77/Panel_P4_MOC]] | P4 feedback только как processed item, если standard proposal влияет на panel/device behavior. | P4 потребляет канон 77 и возвращает feedback через proposal. | P4 Inbox/Artifacts after approve | future proposal | Пока не создавать P4 task. |

## Decisions

R1 approve? Принять маршрутизацию: raw Bus77 protocol and Device API остаются в проекте 008, а не в 77 Standard.

R2 approve? Подготовить отдельный proposal candidate для `Workspace/77_Стандарт_iRidi/inbox` только по проверенным объяснениям для раздела 4 стандарта.

R3 approve? Не публиковать и не менять Google Doc/Wiki/канон 77 на этом шаге.

R4 approve? Device API считать source/reference with `needs_review`, пока нет product/firmware approve and collision checks.

## Blockers

- Нет approved explanation, который можно безопасно перенести в текст стандарта.
- Для approved explanation создан и затем локально применен proposal [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/archive/2026-07-09_bus77-device-api-explanation/proposal]].
- Google Sheet Device API найден как Cursor/PWA xlsx export `C:/AI/VS/bus77-pwa/references/Device API iRidium (1).xlsx`.
- R1-R4 approved by user 2026-07-09.
