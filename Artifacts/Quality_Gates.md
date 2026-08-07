---
type: quality_gates
project: 77 Стандарт iRidi
status: active
updated: 2026-07-08
source_ref: "[[01_Projects/000_CORD_System/Archive/Reviews/Applied/2026-07-08_Project_77_Fit_Report]]"
---

# Quality Gates

## Перед proposal

- Есть источник: встреча, поле, релиз, тикет или документ.
- Есть тип знания: термин, требование, схема, техрешение, продажная формулировка, Wiki-факт.
- Есть целевой раздел стандарта или явно указано, что раздел не найден.
- Факт отделен от интерпретации.
- Открытые вопросы вынесены отдельно.

## Перед approve

- Указан владелец проверки: Василий или автор раздела.
- Указан change_class E0-E7.
- Понятно, меняется ли рекомендация или только формулировка.
- Указано, нужна ли Drive-книга и Wiki.
- Понятно, какие материалы нельзя публиковать внешне.

## После approve

- Обновлен canonical output: Google Doc / Wiki / remarks.
- Создан `resolution.md`.
- Задача перенесена из `inbox` в `archive`.
- Зафиксирован version bump или явно указано `no version change`.
- Если изменение влияет на P4, добавлена ссылка в [[01_Projects/002_Panel_P4_BUS77/Panel_P4_MOC]] или его артефакты.

## Перед сборкой и agent package

- Каждая публикуемая тема имеет уникальный `semantic_uid`, `legacy_uids`, `node_kind`, `coverage_status` и `change_refs`.
- `attachment` не отвечает как самостоятельное знание, `artifact` не публикуется, `gap` не превращается в выдуманную норму.
- Buffer, private baseline и drafts не включаются в agent package.
- `audit-migration` подтверждает exact source tabs, blocks, topic content, tables, asset digests, HTML/DOCX и package integrity.
- HTML и DOCX содержат автоматически собранное оглавление; каждая внутренняя ссылка обязана разрешаться в существующий semantic anchor/bookmark, что проверяет `audit-migration`.
- `audit-migration` проверяет присутствие каждой содержательной строки source в HTML и восстановление source inline formatting; `render_browser_audit.js` проверяет heading hierarchy, картинки и overflow на desktop/tablet/mobile.
- Отрицательный агентский тест обязан вернуть `gap` без citations, а не подобрать случайную тему по общему слову.
- Эта техническая проверка не заменяет независимый D8 и не дает разрешение на cutover или публикацию.
