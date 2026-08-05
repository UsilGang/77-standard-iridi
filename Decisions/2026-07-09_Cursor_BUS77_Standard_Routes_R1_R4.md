---
type: decision
status: applied
created: 2026-07-09
project: 77_Standard_iRidi
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-07-09_Cursor_BUS77_Standard_Routes_Review]]"
---

# Cursor BUS77 Standard Routes R1-R4

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/008_Bus77_Protocol_Knowledge/Bus77_Protocol_Knowledge_MOC]], [[03_Resources/Bus77_Device_API/Device_API_MOC]] и [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/archive/2026-07-09_bus77-device-api-explanation/proposal]].

## Решение

Пользователь принял R1-R4:

- R1: raw Bus77 protocol and Device API остаются в проекте 008, не в 77 Standard.
- R2: для 77 Standard создается отдельный proposal candidate по проверенному объяснению Device API.
- R3: Google Doc, Wiki and canonical standard не меняются на этом шаге.
- R4: Device API остается source/reference with `needs_review`, пока не закрыты product/firmware approve and collision checks.

## Applied Trace

- Создан proposal candidate, затем применен локально: [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/archive/2026-07-09_bus77-device-api-explanation/proposal]].
- Review packet перенесен в applied archive.
- Для проекта 008 зафиксирован Cursor/PWA xlsx source and collision note.

## Что нужно, чтобы появился approved explanation

1. Закрыть коллизии источников Device API в [[01_Projects/008_Bus77_Protocol_Knowledge/QA/Protocol_Collision_Log]].
2. Согласовать черновик текста в proposal candidate.
3. После явного `применяем` перенести approved explanation в standard output and archive proposal.
