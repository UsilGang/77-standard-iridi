---
type: standard_content_refactoring_model
status: proposal
project: 77 Standard iRidi
project_id: "001"
version: "candidate-1"
created: 2026-08-05
privacy: internal
origin: agent_synthesis
confidence: high
verification: architecture_analysis_against_live_book_audit
allowed_use: draft
source_refs:
  - "[[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]]"
  - "user refactoring clarification in Codex task 2026-08-05"
---

# Модель содержательного рефакторинга и шаблонов стандарта

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Reconstruction_Parity_Acceptance_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/Standard_Book_Manifest_MOC]] и [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-05_Standard_As_Code_Architecture_Review]].

## 1. Главное решение

Текущая книга — ценный источник и исторический baseline, но не образец всех будущих правил хранения и оформления. Она создавалась людьми в процессе развития продукта, поэтому содержит одновременно проверенное знание, удачные паттерны, редакционные различия, дубли, случайную нумерацию и возможные ошибки или неявные побочные нормы.

Переход в Standard as Code должен быть не слепым копированием, а контролируемым рефакторингом без потери происхождения:

```text
Legacy book
  -> lossless import evidence
  -> semantic decomposition
  -> normalization/refactoring proposals
  -> approved normalized canon
  -> versioned templates
  -> deterministic publication views
```

## 2. Два разных понятия верности

### Source fidelity

Extractor обязан увидеть весь исходник: текст, таблицы, изображения, порядок, стили, связи и дефекты. Это доказывает профиль `legacy-fidelity`.

### Standard correctness

Нормализованный выпуск обязан соответствовать утвержденным смысловым и редакционным шаблонам, а не случайным различиям старой верстки. Это доказывает профиль `standard-normalized`.

Правильный критерий:

> Каждый элемент старой книги учтен; каждое отличие новой книги объяснено, классифицировано и разрешено; каждый итоговый раздел соответствует единому шаблону.

## 3. Четыре слоя, которые нельзя смешивать

| Слой | Роль | Можно менять автоматически? |
| --- | --- | --- |
| L0 `legacy-snapshot` | immutable evidence текущего Google Doc | нет |
| L1 `lossless-import` | полный импорт с legacy locators/layout hints | только исправлять extractor с новым diff |
| L2 `normalized-source` | будущий канон: темы, rules, facts, assets, templates | только через review |
| L3 `generated-views` | PDF, DOCX, Google Doc, HTML, agent package | генерируется; ручная правка запрещена |

L1 нужен для доказательства полноты, но не используется как нормативная модель. L2 не наследует случайную разметку L0/L1.

## 4. Две обязательные сборки миграции

`legacy-fidelity` использует lossless import и legacy layout manifest. Он доказывает, что extractor и asset pipeline ничего не потеряли. Он может воспроизводить исходные огрехи, потому что является контрольным образцом, а не новым каноном.

`standard-normalized` использует normalized source, versioned templates и общую тему. Он становится новой книгой стандарта без случайных различий между разделами.

После cutover `legacy-fidelity` остается архивным QA-профилем; пользователям и агентам публикуется `standard-normalized`.

## 5. Общий контракт любой темы

Все архетипы наследуют общий семантический каркас:

| Slot | Смысл | Правило |
| --- | --- | --- |
| `purpose` | зачем тема нужна читателю | required |
| `scope` | где применима | required |
| `terms` | термины и glossary refs | required when terms introduced |
| `norms` | обязательные/рекомендуемые решения | explicit, typed |
| `rationale` | почему принято решение | required for non-obvious norm |
| `implementation` | как реализовать | archetype-specific |
| `verification` | как проверить | required for engineering guidance |
| `limitations` | исключения и out-of-scope | explicit |
| `sources_and_changes` | происхождение и история | required, generated |

Slot имеет одно из состояний: `filled`, `not_applicable`, `intentionally_omitted`, `missing_review`, `blocked`. Молчаливого отсутствия не существует.

## 6. Архетипы вместо одного жесткого шаблона

- `front_matter`: аудитория, назначение, роли, терминология, использование, версия;
- `policy`: принцип, применимость, норма, rationale, исключения, контроль;
- `platform_architecture`: компоненты, протоколы, topology, ограничения, compatibility, расчеты, диагностика;
- `subsystem`: ценность, scope, технологии, рекомендуемая архитектура, оборудование, проектирование, управление, кабели/схемы, монтаж, настройка, приемка, ограничения;
- `room_pattern`: задачи помещения, минимальный/рекомендуемый/расширенный состав, сценарии, приемка;
- `engineering_process`: входы, роли, шаги, outputs, gates, tools, definition of done;
- `commissioning_qa`: предусловия, checklist, test procedure, expected result, evidence, diagnosis, handoff.

Machine-readable draft связан через [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/Standard_Book_Manifest_MOC]].

## 7. Как не дать книге создавать побочные правила

### Только typed rule является нормой

Проза, пример, описание продукта и комментарий автора не становятся нормой автоматически. Нормативное утверждение существует только как `rule` с UID, уровнем `must/should/may`, scope, rationale, exceptions и decision provenance. Линтер блокирует нормативные слова внутри informative-блока без rule UID.

### Одно правило — одно определение

Если правило нужно в нескольких главах, оно хранится один раз и включается по ссылке. Копирование запрещается.

### Определения живут в glossary

Canonical definition имеет один term UID; разделы только ссылаются и дают контекст.

### Product fact отделен от recommendation

`Модуль поддерживает X` и `Для стандартного проекта применять X` — разные сущности с разными источниками и lifecycle.

### Override объявляется явно

Локальная рекомендация не может молча отменить общее правило. Нужны `overrides_uid`, scope, rationale и decision ref.

### Нумерация не является identity

Ссылки строятся по UID; номера и подписи генерирует build.

### Данные не дублируются в прозе

Compatibility matrix, product parameters и selection tables хранятся как typed data и рендерятся во все views.

## 8. Каталог операций рефакторинга

| Operation | Что делает | Gate |
| --- | --- | --- |
| `format_normalize` | стили, spacing, callout, heading level | batch review, no semantic impact |
| `term_normalize` | единое название термина/продукта | glossary evidence + review |
| `renumber` | новая генерируемая нумерация | mechanical, diff recorded |
| `move` | перенос в правильную тему | semantic digest unchanged |
| `split` | разделение смешанного блока | source coverage 100% |
| `merge` | объединение дублей | все locators сохранены |
| `deduplicate` | один canonical rule вместо копий | equivalence evidence |
| `type_separate` | fact/rule/rationale/example в разные сущности | classification review |
| `clarify` | переписывание без смены рекомендации | E1 review |
| `resolve_conflict` | выбор между утверждениями | human/domain decision |
| `deprecate` | отмена решения | E7 + release impact |
| `add_content` | новое знание | отдельный source proposal, не refactoring |
| `remove_content` | исключение материала | explicit reason + decision |

Механические transformations можно утверждать пакетом. Split/merge/dedupe/clarify требуют редакционного review. Конфликт, новая норма, изменение применимости, deprecation и удаление требуют human/domain decision.

## 9. Transformation manifest

Каждый refactoring batch создает immutable manifest:

```yaml
batch_uid: refactor_legacy_to_normalized_001
legacy_snapshot_uid: legacy_20260805
template_version: standard_templates_1
operations:
  - operation_uid: op_0001
    type: move
    source_locators: [legacy:tab-17:block-001]
    target_uids: [std_topic_bus_diagnostics]
    semantic_impact: none
    reason: "Материал 4.11 находился во вкладке ПНР."
    reviewer: pending
    decision_ref: null
```

Manifest — единственный allowlist отличий между `legacy-fidelity` и `standard-normalized`. Необъясненный text/visual diff завершает приемку FAIL.

## 10. Template contract для сборщика

Build script не угадывает структуру по тексту. Он получает `template_uid` и version, ordered slots, required conditions, allowed content types, missing policy, heading/numbering behavior, renderer component и publication profile visibility.

```yaml
template_uid: tpl_subsystem_v1
inherits: tpl_topic_core_v1
slots:
  - id: purpose
    required: true
    accepts: [prose, value_statement]
  - id: recommended_architecture
    required: true
    accepts: [prose, rule, schematic]
  - id: verification
    required: true
    accepts: [checklist, acceptance_test]
missing_policy:
  release: block
  internal_review: render_gap_marker
```

Новый раздел нельзя выпустить без required slot; optional slot не создает пустой заголовок.

## 11. Автоматические проверки целостности

`standard_book.py validate` должен искать:

- duplicate/similar rules без общего UID;
- конфликтующие значения product fact;
- undefined или повторно определенные terms;
- normative language вне typed rule;
- rule без scope/rationale/source/decision;
- override без `overrides_uid`;
- required slot со статусом `missing_review`;
- ручные номера в cross-reference;
- asset/table без UID или provenance;
- data value, скопированный в несколько тем;
- fragment без legacy locator или approved source;
- source block без target или explicit disposition.

Semantic similarity только предлагает deduplication; автоматически правила не объединяются.

## 12. Двухконтурная приемка

1. `legacy-fidelity` сравнивается с immutable исходной книгой и доказывает lossless import.
2. `standard-normalized` сравнивается с normalized source/template contract и transformation manifest.
3. Cross-check доказывает, что каждый legacy element сохранен, преобразован approved operation или исключен explicit decision.

Pixel parity требуется для `legacy-fidelity`. Для `standard-normalized` требуется template conformance и отсутствие необъясненных semantic/content deltas; намеренно унифицированная верстка не является дефектом.

## 13. Порядок пилота и миграции

1. Зафиксировать immutable legacy snapshot.
2. Выполнить lossless import без редактуры.
3. Собрать `legacy-fidelity` и доказать полноту extractor/assets.
4. Применить core template и архетип раздела.
5. Сформировать findings и transformation manifest.
6. Пакетно утвердить mechanical operations.
7. Отдельно решить semantic conflicts и изменения стандарта.
8. Собрать `standard-normalized`.
9. Выполнить independent dual-profile certification.
10. Только после PASS предложить cutover.

Вся книга входит в обязательный scope с самого начала через full-book lossless import. Раздел 5 «Освещение» проходит первым глубокий dual-profile цикл и проверяет достаточность slots, типизацию rules/facts, сложные таблицы, 107 изображений и transformation manifest. Его PASS не заменяет full-book certification.

## 14. Рекомендуемое решение D9

Утвердить:

- текущая книга — immutable legacy baseline, а не шаблон будущего канона;
- pipeline строит `legacy-fidelity` и `standard-normalized`;
- новый канон формируется по versioned archetype templates;
- любое отличие normalized output имеет transformation operation UID;
- человеческие ошибки не исправляются молча и не наследуются автоматически;
- отсутствие необъясненных отличий важнее буквального сохранения случайной редакционной формы.
