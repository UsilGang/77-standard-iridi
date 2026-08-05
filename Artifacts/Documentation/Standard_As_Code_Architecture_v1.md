---
type: standard_as_code_architecture
status: approved_design
project: 77 Standard iRidi
project_id: "001"
version: "approved-1"
created: 2026-08-05
privacy: internal
origin: agent_synthesis
confidence: high
verification: source_audit_and_project_rules
allowed_use: implementation_contract
decision_ref: "[[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-05_Standard_As_Code_Architecture_D1_D11]]"
source_refs:
  - "[[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]]"
  - "[[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/VERSIONING]]"
  - "[[03_Resources/Standard_Book/Publishing_Pipeline_Design]]"
---

# Архитектура Standard as Code для «Стандарта автоматизации iRidi»

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/Standard_Book_Manifest_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Reconstruction_Parity_Acceptance_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Quality_Gates]], [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/VERSIONING]] и [[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-08-05_Standard_As_Code_Architecture_Review]].

## 1. Рекомендуемое решение

Стандарт следует вести как версионируемый продукт знаний, в котором локальное дерево типизированных артефактов является источником для сборки, а книга — одним из представлений. Входящие от рынка, разработки, владельца, продаж, пресейла и поддержки не должны сразу переписывать текст. Они образуют change card, проходят impact analysis и review, изменяют конкретные стабильные UID и только затем входят в выпуск.

Основная формула:

```text
source signal
  -> change card
  -> impact + coverage disposition
  -> proposal / decision
  -> source artifacts by stable UID
  -> validate + build + diff
  -> release manifest
  -> human book + agent package + change feed
```

Это дает две самостоятельные проверки, которые важны для стандарта:

- **ответа нет, потому что это пробел** — кандидат на продуктовую или документальную доработку;
- **ответа нет, потому что решение вне стандарта** — явная граница рекомендуемого подхода, а не приглашение к произвольной реализации.

## 2. Архитектурные принципы

1. **Идентичность не равна номеру.** `8.3.2` — отображаемый адрес, который может измениться; постоянная сущность — `std_topic_ventilation_control_modes`.
2. **Книга не источник истины.** PDF, DOCX, Google Doc, HTML и agent package собираются из одного release manifest.
3. **Тема — базовая единица редактирования.** Не дробить каждый абзац в отдельный файл.
4. **Правило — адресуемая единица контроля.** Отдельный rule UID нужен для обязательной/рекомендуемой нормы, проверки проекта, deprecation и точной ссылки агента.
5. **Факт отделен от нормы.** «Модуль поддерживает X» и «в стандартных проектах применять X» — разные типы утверждений и могут иметь разные источники.
6. **Источник не копируется в канон.** Раздел хранит ссылки на source refs и change refs; raw остается в своем privacy-контуре.
7. **Черновик не попадает в ответы.** MCP и внешние views по умолчанию читают только released content.
8. **Оформление — код/конфигурация.** Шрифты, размеры, отступы, таблицы, выноски, нумерация, подписи и размещение картинок задаются design tokens и renderer rules.
9. **Сборка проверяема.** Каждый выпуск имеет lock manifest, checksums, semantic diff и visual QA.
10. **Миграция не равна содержательному одобрению.** Перенос существующего текста сохраняет provenance `legacy_migration`; обнаруженные ошибки идут отдельными proposals.

## 3. Правильная гранулярность

Текущая книга не должна автоматически задавать будущую структуру только потому, что именно так ее когда-то сверстал человек. Controlled refactoring, два build profile и versioned archetype templates описаны в [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]].

Рекомендуются четыре уровня:

| Уровень | Для чего | Когда отдельный файл/ID |
| --- | --- | --- |
| Chapter | композиция книги | всегда отдельный `section.yaml` |
| Topic | самостоятельный вопрос читателя | отдельная папка или `content.md` |
| Rule / claim | норма, продуктовый факт, ограничение | отдельная запись с UID, если по ней возможен аудит или изменение |
| Asset / data | схема, изображение, таблица, расчет | отдельный UID и manifest |

Обычный объясняющий текст живет внутри `content.md` темы. Не нужно присваивать ID каждому абзацу. Если позже абзац становится проверяемой нормой, он выделяется в rule без перестройки всей главы.

## 4. Типы разделов книги

Один шаблон на 17 глав создаст ложную унификацию. Нужны семь архетипов:

| Архетип | Разделы | Основная логика |
| --- | --- | --- |
| `front_matter` | 1 | аудитория, назначение, роли, термины, как пользоваться |
| `policy / requirements_process` | 2–3 | общие правила и контракт ТЗ |
| `platform_architecture` | 4 | протокол, топология, компоненты, питание, логика, ограничения |
| `subsystem` | 5–12 | ценность → варианты → рекомендуемая реализация → монтаж → проверка |
| `room_patterns` | 13 | тип помещения → функции → состав → варианты → критерии приемки |
| `engineering_process / tool / cabinet` | 14–16 | процесс проектирования, Project Tool, щиты |
| `commissioning_qa` | 17 | подготовка → тесты → диагностика → приемка → evidence |

### Контракт типовой инженерной подсистемы

Не все пункты обязательны, но отсутствие должно быть явным:

1. назначение и ценность;
2. область действия и термины;
3. типы систем и технологий;
4. рекомендуемая архитектура;
5. оборудование и compatibility matrix;
6. правила проектирования и подбора;
7. логика управления, режимы и сценарии;
8. кабели, топология и схемы;
9. монтаж;
10. настройка и ПНР;
11. критерии приемки и проверки;
12. ограничения, анти-паттерны и явное `out_of_scope`;
13. источники и история изменения.

## 5. Предлагаемое дерево хранения

Исторические `inbox/archive/sources` сохраняются как control plane. После approve редактируемое знание, правила сборки, временный build и опубликованные пакеты физически разделяются:

```text
Workspace/77_Стандарт_iRidi/
  inbox/                         # change proposals, как сейчас
  archive/                       # resolved change packets, как сейчас
  sources/                       # source locators и legacy extracts
  standard-src/                  # только содержимое канона
    book.yaml                    # состав, порядок, профили публикации
    taxonomy/
      audiences.yaml
      normative-levels.yaml
      coverage-statuses.yaml
      tags.yaml
    sections/
      architecture/
        section.yaml
        topics/
          bus-topology/
            topic.yaml
            content.md
            rules.yaml
            data/
      ventilation/
        section.yaml
        topics/...
    entities/
      products/                  # факты о продуктах, не рекомендации
      capabilities/              # свет, вентиляция, протечки и т. п.
      protocols/
      roles/
    assets/
      ast_.../
        asset.yaml
        original.ext
        derivatives/
  tooling/                       # правила и инструменты, не содержимое книги
    theme/
      tokens.yaml
      layout.yaml
      callouts.yaml
      docx-template.docx
    schemas/
      book.schema.json
      section.schema.json
      topic.schema.json
      rule.schema.json
      change.schema.json
    renderers/
    templates/
    tests/
  build/                         # воспроизводимые временные результаты, не канон
  releases/                      # immutable published packages
    1.2.0/
      release.yaml
      manifest.lock.json
      CHANGELOG.md
      checksums.txt
      human/
      agent/
      deltas/
```

Точная структура может быть скорректирована пилотом, но разделение `control plane / standard-src / tooling / build / releases` является обязательным. Потребляющие агенты читают только `releases/<version>/agent`; подробный контракт описан в [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]].

## 6. Контракт метаданных

### Минимум для topic

```yaml
uid: std_topic_ventilation_control_modes
type: topic
title: "Управление вентиляцией"
parent_uid: std_ch_ventilation
display_order: 40
status: approved
audiences: [integrator, presales, sales, training]
jobs: [learn, explain, select, audit]
consumer_applications: [reference_agent, presales_auditor, training_agent]
normative_level: mixed
coverage_status: documented
owners: [standard_owner]
reviewers: [domain_expert]
source_refs: [source:...]
change_refs: [chg:...]
introduced_in: 1.2.0
last_changed_in: 1.2.0
```

### Минимум для rule / claim

```yaml
- uid: std_rule_ventilation_speed_control_001
  claim_type: recommendation
  normative_level: should
  statement: "..."
  rationale: "..."
  applies_when: ["..."]
  exceptions: []
  evidence_refs: [source:...]
  decision_ref: decision:...
  status: approved
  introduced_in: 1.2.0
  last_changed_in: 1.2.0
```

Обязательные общие поля: `uid`, `type`, `status`, `parent_uid`, `source_refs`, `change_refs`, `introduced_in`, `last_changed_in`, `privacy`, `allowed_outputs`. Номер и порядок — отдельные presentation fields.

## 7. Типизированные содержательные блоки

Для сборки и ответов агентов полезны следующие типы:

- `normative_rule`: обязательное или рекомендуемое решение;
- `product_fact`: проверяемая возможность/ограничение продукта;
- `rationale`: почему правило принято;
- `warning` и `anti_pattern`;
- `example` и `scenario`;
- `selection_rule` и `calculation`;
- `compatibility_matrix`;
- `procedure`, `checklist`, `acceptance_test`;
- `glossary_term`;
- `image`, `schematic`, `table`, `diagram`, `ui_capture`.

Не следует превращать всю прозу в YAML. Текст остается удобным Markdown, а YAML содержит композицию, адресуемые нормы и данные, которые должны проверяться машиной.

## 8. Assets и оформление

Каждая картинка, схема и таблица получает постоянный UID. Для image asset нужны:

- оригинальный локальный файл;
- SHA-256;
- тип и MIME;
- размеры оригинала и параметры отображения;
- alt, caption, credit, source_ref и license/use restriction;
- список производных файлов;
- список topic/rule, где asset используется.

Временный Google `contentUri` не считается источником. В миграции файл скачивается один раз, фиксируется локально и связывается с исходным object ID.

Оформление текущей книги нужно формализовать в design tokens:

- A4 и поля;
- типографика заголовков, основного текста, подписей и таблиц;
- интервалы и правила page break;
- стили callout, warning, example и recommendation;
- ширина/обтекание картинок;
- заголовки таблиц и рисунков;
- колонтитулы, версия и дата выпуска;
- автоматическое оглавление и нумерация.

Семантический heading level задает структура source tree, а не случайный стиль, импортированный из Google Docs.

## 9. Change card и трассировка

Исполняемый слой между source signal и changeset — редакционное задание EDT. Его полный контракт, content/visual brief и связь с версиями описаны в [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]]. Change card отвечает «почему рассматриваем изменение», EDT — «что именно и как должно быть сделано», changeset — «что фактически изменилось».

Каждый новый сигнал формирует одну change card или явно объединенную серию. Минимальный контракт:

```yaml
change_uid: chg_20260805_example
initiator: owner | integrator | development | sales | presales | support | market
source_refs: [...]
problem_or_question: "..."
audience_impact: [...]
candidate_uids: [...]
route_confidence: high | medium | low
coverage_disposition: documented | gap | out_of_scope | conflict | needs_review
change_class: E0 | E1 | E2 | E3 | E4 | E5 | E6 | E7
normative_impact: none | clarification | compatible_addition | changed_recommendation
compatibility_impact: none | additive | breaking | deprecation
decision: pending | approve | revise | reject
decision_ref: null
planned_release: null
```

После применения change card должна содержать exact `changed_uids`, semantic diff, build evidence и release UID. Обратные ссылки из topic/rule на `change_refs` дают ответ «кто, когда и почему изменил этот стандарт».

## 10. Coverage и поведение при отсутствии ответа

Поиск не должен отвечать только «найдено / не найдено». Для вопроса или capability фиксируется один из статусов:

| Статус | Смысл | Действие |
| --- | --- | --- |
| `documented` | стандарт содержит ответ | вернуть released UID и цитату |
| `partial` | описана только часть | ответить известное и открыть gap proposal |
| `gap` | ожидаемая тема не описана | route в продукт/документацию |
| `out_of_scope` | стандарт сознательно не рекомендует/не рассматривает | вернуть границу и rationale |
| `conflict` | источники или нормы расходятся | блокировать уверенный ответ, открыть review |
| `unknown` | еще не классифицировано | owner/domain review |
| `deprecated` | решение ранее было допустимо, теперь нет | вернуть замену и версию изменения |

Это превращает отсутствие текста из случайности в управляемое знание.

## 11. Версионность

### Рекомендация

1. Внешняя версия книги — обычный `MAJOR.MINOR.PATCH`.
2. `schema_version` source layer и `build_tool_version` живут отдельно и не меняют версию технического стандарта сами по себе.
3. Chapter/topic/rule/asset не получают собственный SemVer. У них есть монотонная `revision`, content digest, `introduced_in`, `last_changed_in` и `last_editorial_job`.
4. Независимый module SemVer вводится только для реально отдельно публикуемой книги, а не автоматически для каждой главы.
5. Edition (`2026.2`, квартальный срез) — удобный alias для обучения/печати, но не вторая истина.
6. Любой новый опубликованный экземпляр с измененным содержанием обязан увеличить book SemVer минимум на PATCH; до публикации используется draft build ID.

### Как выбирать bump

Change class E0–E7 недостаточно использовать без смыслового воздействия. Bump определяется по `normative_impact` и `compatibility_impact`:

| Выпуск | Когда |
| --- | --- |
| PATCH | редактура/уточнение, не меняющее рекомендацию; добавление примера без новой нормы |
| MINOR | новое совместимое правило, технология, раздел или существенное расширение применимости |
| MAJOR | изменение обязательной/рекомендуемой модели, ломающее прежний проектный подход; deprecation без совместимого продолжения |

Таким образом, E2 может быть PATCH для примера и MINOR для нового рекомендуемого решения. E3 может быть PATCH при чистой редакционной перестройке и MAJOR при смене самой рекомендации.

### С какой версии начинать

Миграция формы хранения не должна автоматически объявлять технический стандарт `2.0.0`. Рекомендуется:

- зафиксировать текущий опубликованный смысл как baseline `1.2.0`;
- указать `source_schema_version: 1`;
- после паритетной миграции выпустить следующий номер только по реальным содержательным изменениям;
- использовать `2.0.0` лишь когда меняется нормативная модель стандарта или сознательно объявляется несовместимое новое поколение.

Каждый release хранит immutable manifest со всеми UID/digest и генерируемый changelog со ссылками на decisions и source refs.

## 12. Детерминированная сборка

### Конвейер

```text
load manifests
  -> schema validation
  -> graph/link/source validation
  -> resolve publication profile
  -> canonical document AST
  -> render adapters
  -> semantic diff + visual QA
  -> signed/locked release manifest
```

Canonical document AST нужен, чтобы Markdown, YAML и assets одинаково собирались в несколько представлений, а правила нумерации и дизайна не дублировались в каждом renderer.

### Представления

| Profile | Получатель | Содержимое |
| --- | --- | --- |
| `integrator_full` | интеграторы | полная книга стандарта |
| `presales_audit` | пресейл | нормы, подбор, ограничения, checklists |
| `sales_quick` | продажи | ценность, возможности, границы, быстрые ссылки |
| `training_delta` | обучение | только изменения выпуска + связанные темы |
| `agent_knowledge` | агенты/MCP | released structured content, UID, связи, фасетные индексы; embeddings optional |
| `internal_review` | авторы | draft + source/change provenance + findings |

На этапе миграции обязательны два технических profile:

- `legacy-fidelity` — доказать полноту импорта и воспроизвести исходный экземпляр с legacy layout hints;
- `standard-normalized` — собрать унифицированную книгу по versioned templates и approved transformations.

### Выходы

- HTML/CSS как диагностируемое промежуточное human view;
- PDF как фиксированный выпуск;
- DOCX как редактируемый обменный формат;
- Google Doc как сгенерированный publication target после approve;
- JSON/JSONL knowledge package и search index для агентов.

Google Doc может собираться через renderer/API или импорт управляемого DOCX. Он не должен быть единственным build target или источником обратной миграции.

### Проверки готовности сборки

- все UID уникальны, ссылки разрешены;
- все published claims имеют decision/migration provenance;
- все assets существуют и совпадают с checksum;
- нет draft/private content в выбранном output profile;
- число тем, таблиц и изображений совпадает с ожидаемым manifest;
- одинаковый source lock дает одинаковый semantic digest;
- semantic diff объясняет каждое изменение;
- visual diff проверяет заголовки, таблицы, выноски, картинки, переносы и оглавление;
- в release package присутствуют версия, дата, changelog и checksums.

## 13. MCP и доступ других агентов

Агент — не самостоятельная человеческая аудитория, а приложение, работающее от имени роли и задачи. Метаданные должны отдельно хранить `audiences`, `jobs` и `consumer_applications`. Справочный агент, sales technical QA, пресейл-аудитор и учебный агент используют один release, но разные query/audit profiles.

До MCP обязательным интерфейсом является generated agent package: `START_HERE.md`, package manifest, topic/rule/entity registries, relations, aliases, release delta и производные фасетные индексы. Детерминированный поиск по UID, aliases и facets выполняется раньше необязательного semantic recall. Полный контракт — в [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]].

MCP следует строить поверх released manifest и индекса, а не поверх живой папки черновиков. Минимальные read-only методы:

- `search_standard(query, audience, release)`;
- `get_topic(uid, release)`;
- `get_rule(uid, release)`;
- `get_capability_status(capability_uid)`;
- `diff_releases(from, to, audience)`;
- `list_changes_since(release)`;
- `audit_project(requirements_or_bom, release)`;
- `report_gap(question, context)` — создает только локальный кандидат, внешняя запись отдельно;
- `get_release_manifest(release)`.

Ответ MCP обязан включать: release, UID, title, normative level, coverage status, source/decision refs, применимость и direct citation. Draft, Buffer и unresolved conflict не должны выдаваться как действующий стандарт.

После публикации выпуск может создавать внутреннее событие `standard.release.published` с release UID, changed UIDs, audience impact и changelog ref. Отдел обучения получает не весь документ, а `training_delta` и список тем для обновления программы.

## 14. Инструменты и skills

Сейчас зарегистрированного конвейера Standard as Code нет. Это tool gap; одноразовыми несвязанными скриптами его закрывать не следует.

Для управляемости рекомендуется один CLI `standard_book.py` с подкомандами:

- `inventory` — read-only аудит Google Doc/source tree;
- `extract` — контролируемая миграция текста/assets;
- `validate` — schema, links, source, assets, privacy, coverage;
- `build` — выбранный profile/output;
- `diff` — semantic и visual diff;
- `release` — release manifest/changelog/checksums после approve;
- `index` — agent knowledge package;
- `serve-mcp` или отдельный MCP service — только после стабильного контракта.

Внутри CLI могут быть модули, но пользователь и агент получают один интерфейс. После утверждения он должен быть зарегистрирован в [[03_Resources/Tool_Registry/CORD_Script_Index]], [[03_Resources/Tool_Registry/Tool_Registry_MOC]] и [[03_Resources/Action_Registry/Action_Registry_MOC]].

На первом этапе достаточно одного skill-оркестратора `$standard-book-operator`, который выбирает подкоманду, восстанавливает проектный контекст и соблюдает approve gates. Отдельные skills для intake/editor/release имеет смысл выделять только после повторяющихся устойчивых сценариев.

## 15. План миграции

| Фаза | Что делаем | Gate результата |
| --- | --- | --- |
| 0. Inventory | фиксируем структуру, вкладки, styles, tables, images, revisions | аудит и manifest-кандидат; выполнено в proposal |
| 1. Architecture | утверждаем модель UID, layout, versioning, lifecycle | решение по этому пакету |
| 2. Full-book lossless import | импортируем всю книгу, все вкладки, таблицы, assets, legacy layout hints и provenance | 100% full-book source inventory, без редактуры |
| 3. Lighting deep slice | на крупнейшем разделе 5 собираем `legacy-fidelity`, выполняем refactoring и `standard-normalized` | проверены extractor, templates, tables, 107 images и dual-profile diff |
| 4. Full-book normalization | применяем утвержденные archetypes и transformation manifests ко всей книге | пораздельные reports + full-book coverage |
| 5. Special chapters | отдельно 1, 4, 5 и planned 2–3, 13–17 | содержательные findings не исправляются без review |
| 6. Dual run | Google Doc остается каноном, source tree собирает release candidate | один полный выпуск без потерь |
| 7. Cutover | утверждаем source tree как источник истины | signed release, rollback snapshot, publication approve |
| 8. Agent access | строим read-only MCP и change feed | ответы с UID/release/citations и privacy tests |

Обязательный scope — вся книга. Раздел 5 «Освещение» используется только как первый глубокий вертикальный проход, потому что это крупнейшая заполненная глава: около 144 тыс. знаков, 37 таблиц и 107 изображений. Успех по освещению доказывает зрелость сложного шаблона и renderer, но не заменяет full-book migration и certification.

«Буфер» в batch migration не входит. Каждый его фрагмент проходит source/proposal route отдельно.

## 16. Acceptance criteria для всей инициативы

Полный исполняемый контракт приемки зафиксирован в [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Reconstruction_Parity_Acceptance_v1]]. Проверка выполняется отдельной задачей [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-PARITY-001_Independent_Reconstruction_Certification]], а не самим мигратором/сборщиком.

1. По любому опубликованному утверждению можно установить UID, версию, источник/миграционное происхождение и решение.
2. По change card/refactoring operation можно установить инициатора, причину, legacy locator, затронутые UID, diff и выпуск.
3. Из clean checkout одной командой собираются human book и agent package без ручной правки содержания.
4. Картинки, таблицы, подписи, нумерация, оглавление и ключевое оформление воспроизводятся автоматически.
5. Система отличает `gap`, `out_of_scope`, `conflict`, `deprecated` и обычное отсутствие результата поиска.
6. Пресейл-аудит возвращает не общую справку, а проверяемые нормы и несоответствия с release citations.
7. Новый выпуск автоматически дает краткий human changelog и machine-readable delta для обучения и агентов.
8. Черновики, Buffer, private sources и unresolved proposals не попадают в published views.
9. Миграцию можно остановить и откатить, не потеряв действующий Google Doc.
10. Смена renderer/theme не меняет нормативную версию стандарта без содержательного change.

К этим критериям применяется строгий результат: `PASS`, `FAIL_IMPLEMENTATION` или `FAIL_ARCHITECTURE`. Полная инициатива не принимается как «в целом похожая». До PASS выполняются исправление, clean rebuild и новый независимый certification run.

## 17. Решения, которые действительно нужны сейчас

Вместо выбора десятков деталей предлагается утвердить семь базовых defaults, refactoring default D9, EDT/version trace D10 и access model D11:

1. локальный `standard-src` становится будущим source of truth только после dual-profile parity gate;
2. Google Doc остается действующим каноном до cutover, затем становится generated view;
3. постоянные semantic UID отделяются от номера главы/подраздела;
4. базовая гранулярность — topic, а отдельные rule/asset/data UID создаются по необходимости;
5. версия книги — SemVer; schema/build version отдельно; chapter SemVer не вводится на старте;
6. обязательный scope — вся книга; первый deep slice — раздел 5 «Освещение»; Buffer не мигрируется автоматически;
7. сначала реализуется один зарегистрированный CLI и один skill-оркестратор, MCP — после стабильной паритетной сборки.

Обязательное owner requirement поверх defaults: full-book cutover запрещен без независимого PASS по контракту реконструкционной приемки G1–G8.

Рекомендуемый default D9: legacy book сохраняется как evidence, но normalized canon строится по versioned templates; pipeline выпускает `legacy-fidelity` и `standard-normalized`, а каждое отличие второго объясняется transformation operation UID.

D10: редакционное задание связывает reader problem, source refs, target UID, text/visual plan, changeset и release.

D11: применяется `knowledge kernel + generated projections`; control plane, `standard-src`, `tooling`, `build` и `releases` физически разделены, человеческие аудитории отделены от machine applications, а агенты получают только released package через единый query contract.

Детали renderer/templates можно уточнить по результату lighting deep slice, но этап завершается только после полной миграции и независимой приемки всей книги.
