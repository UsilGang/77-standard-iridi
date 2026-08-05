# Device API для Bus77: выжимка для стандарта

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/008_Bus77_Protocol_Knowledge/Bus77_Protocol_Knowledge_MOC]], [[01_Projects/008_Bus77_Protocol_Knowledge/Sources/Device_API_Source]] и [[01_Projects/008_Bus77_Protocol_Knowledge/QA/Protocol_Collision_Log]].

## Суть

Device API описывает прикладной слой Bus77: какие типы устройств существуют, какие у них Device ID, какие каналы управления и обратной связи доступны, какие FID, типы значений, флаги, обязательность и версия API у каждого канала.

Для стандарта 77 это нужно объяснять как правило применения и проектирования, а не переносить сырые таблицы Device API в книгу.

## Факты / формулировки для стандарта

- Device API отделен от wire-level Bus77 protocol: wire protocol отвечает за обмен сообщениями, Device API описывает модель устройств и каналов.
- Основные сущности объяснения: Device Type / Device ID, подустройство, КУ, КОС, FID, Required, Flags, API version.
- FID нельзя проверять только как число: один и тот же FID может встречаться в разных направлениях или классах каналов. Ключ проверки должен учитывать `device_id + direction/class + fid + function`.
- Для книги стандартов допустимы только approved summaries; source tables, SDK zip and reference implementations остаются в проекте 008.

## Цитаты или отсылки к источнику

- `C:/AI/VS/bus77-pwa/references/Device API iRidium (1).xlsx` - Cursor/PWA xlsx export Device API.
- `C:/AI/ESP/ESP_B77/Doc/DeviceAPITable.md` - локальный markdown Device API.
- `C:/AI/mcp-bus77-py/iridium_device_api_simple.json` - Cursor-derived structured Device API model.
- [[01_Projects/008_Bus77_Protocol_Knowledge/QA/Protocol_Collision_Log]] - журнал расхождений.

## Открытые вопросы

- Resolved 2026-07-09: canonical name for `Device ID=2` is `Button`; локальный `DeviceAPITable.md` with `DryContact` is not canonical for this naming.
- Нужно определить, упоминать ли конкретные Device Type examples в тексте стандарта или оставить только общую модель Device API.

## Не включать в стандарт

- Полные таблицы Device API.
- Raw SDK, zip, firmware/reference implementations.
- Полные списки типов устройств and FID without collision review.
