---
type: architecture_review
status: approved
project: 77 Standard iRidi
project_id: "001"
created: 2026-08-05
privacy: internal
origin: mixed
source_ref: "user request in Codex task 2026-08-05"
source_refs:
  - "user request in Codex task 2026-08-05"
  - "[[00_Inbox/Raw_Collector/Archive/2026/07/20260708_transcribe_recording_2026-06-30_15-04-23_reco_c98ab5251a]]"
  - "[[00_Inbox/Raw_Collector/Archive/2026/07/20260711_transcribe_recording_2026-07-10_14-01-47_reco_46f55ec34a]]"
proposal_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]]"
action_id: operate_standard_book
tool_plan: local_file_tools_plus_read_only_google_docs_inventory
tool_gap: standard_as_code_pipeline_to_be_implemented_and_registered_by_approved_do
approval_class: human_decision
blocker: null
canonical_change: false
external_write: false
approved_at: 2026-08-05
approval_ref: "user: аппрув на все; D8 сейчас не выполняем; остальное реализовать"
approved_decisions: [D1, D2, D3, D4, D5, D6, D7, D9, D10, D11]
deferred_execution: [D8]
---

# Review: архитектура Standard as Code

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Audience_And_Agent_Knowledge_Access_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/Standard_Book_Manifest_MOC]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Reconstruction_Parity_Acceptance_v1]], [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/VERSIONING]] и [[01_Projects/001_77_Standard_iRidi/Artifacts/Quality_Gates]].

## Что предлагается решить

Утвердить архитектурное направление, не меняя пока Google Doc и не мигрируя содержание.

### Рекомендуемый пакет defaults

| ID | Решение | Почему |
| --- | --- | --- |
| D1 | Будущий source of truth — локальный типизированный `standard-src`; Google Doc после cutover — generated view | дает diff, build, trace и несколько выходных форматов |
| D2 | До full parity gate Google Doc остается действующим опубликованным каноном | не ломает текущую работу и позволяет rollback |
| D3 | Стабильные semantic UID отделены от отображаемой нумерации | перенос темы не ломает ссылки и историю |
| D4 | Базовая единица — topic; отдельные UID только для правил, claims, таблиц, схем и assets | точность без файлового взрыва |
| D5 | Книга имеет release SemVer; любое опубликованное изменение поднимает минимум PATCH. Вложенные units имеют revision+digest, draft — build ID; chapter SemVer не вводится | не допускает две разные опубликованные книги с одной версией и не плодит несинхронные SemVer |
| D6 | Обязательный scope — вся книга; первый deep slice — раздел 5 «Освещение»; Buffer исключен из auto migration | крупнейший раздел проверяет архитектуру на максимальной сложности, но не подменяет full-book acceptance |
| D7 | Один CLI `standard_book.py` + один skill-оркестратор; MCP после стабильной сборки | снижает операционную сложность |

### D8 — обязательный owner requirement, не optional default

Переход на новый source of truth запрещен без отдельной независимой приемки. Она должна собрать оба profile: сравнить `legacy-fidelity` с immutable baseline, а `standard-normalized` — с template contract и approved transformation manifest, затем выдать PASS по G1–G8. При FAIL цикл повторяется без ручного перелистывания владельцем.

### D9 — рекомендуемый content refactoring default

Текущая книга сохраняется как legacy evidence, но не диктует шаблон normalized canon. Pipeline строит два profile: `legacy-fidelity` для доказательства полноты и `standard-normalized` для новой унифицированной книги. Каждый normalized delta обязан иметь transformation operation UID; typed rule — единственный способ создать нормативное правило.

### D10 — редакционное задание и version trace

Входящий сигнал после disposition превращается в EDT — исполняемый контракт с reader problem, source refs, target UIDs, планом текста/визуала, outputs, acceptance и version impact. EDT связывается с actual changeset и release. Разделы, темы, rules и assets имеют revisions; книга меняет SemVer только при release, но каждый опубликованный экземпляр с изменением получает минимум PATCH.

### Что подтверждено разговором с генеральным директором

Найдена и полностью прочитана запись от 30 июня 2026 года; запись от 10 июля подтверждает последующее развитие решения. Сырой транскрипт остается в source-контуре. В архитектуру перенесены только обезличенные выводы:

- первичные пользователи — инсталляторы/интеграторы, продажи и пресейл;
- дополнительные рабочие контуры — проектировщики, монтаж/ПНР, Академия, продукт/разработка и управленческий QA;
- стандарт нужен одновременно для первоначального обучения, оперативного ответа, проверки технической корректности и выявления рыночных пробелов;
- продажный QA и технический QA являются разными приложениями;
- схемы и Project Tool требуют строгих инженерных данных, а не только текстового поиска;
- изменения из экспертных советов и релизов должны попадать в review, а не напрямую переписывать канон.

### D11 — knowledge kernel и доступ агентов

Физически разделить пять слоев: control plane, `standard-src`, `tooling`, временный `build` и immutable `releases`. Человеческая аудитория, выполняемая задача и тип агента становятся разными полями. Потребляющий агент получает только generated release package с `START_HERE`, topic/rule/entity registries, relations, aliases, фасетными индексами и citations. Векторный поиск допускается позднее как помощник поиска, но не как источник истины. CLI и будущий MCP используют один query/audit contract.

| Группа потребителей | Основные задачи |
| --- | --- |
| Инсталляторы и интеграторы | обучение, выбор решения, единый стандарт команды, монтаж и проверка |
| Проектировщики, монтаж, ПНР и сервис | расчет, совместимость, схемы, подключения, диагностика и приемка |
| Продажи | ценность, ограничения, вопросы клиенту, техническая корректность разговора |
| Пресейл | решение запроса, проверка состава, аудит проекта по rule UID |
| Академия | курсы, тесты, персональное дообучение и release delta |
| Продукт и разработка | gaps рынка, неподдержанные сценарии, связь релиза со стандартом |
| Руководитель и QA | нарушения, пробелы знаний, качество применения стандарта |
| ИИ-приложения | справка, sales technical QA, presales audit, обучение, редакция, gaps и release monitoring |

| Физический слой | Содержимое | Кто читает |
| --- | --- | --- |
| Control plane | источники, EDT, review, решения, история | редакция и владелец |
| `standard-src` | редактируемые темы, rules, entities, assets | авторы и сборщик |
| `tooling` | schemas, templates, theme, renderers, tests | сборщик и QA |
| `build` | временные результаты | сборка и диагностика |
| `releases/<version>` | immutable human book, agent package и deltas | люди и потребляющие агенты |

Быстрый поиск не требует чтения сотен Markdown-файлов: агент фиксирует release, определяет роль/задачу/домен/стадию, проходит UID/aliases/фасетные индексы, читает только найденные topic/rule и возвращает `documented | gap | out_of_scope | conflict | deprecated | needs_input` с точными citations.

## Что не входит в это решение

- исправление найденных опечаток, нумерации и доменных противоречий;
- перенос раздела 17;
- автоматическая публикация в Google Docs, Wiki или другие внешние системы;
- признание draft manifest действующим каноном;
- создание MCP-сервера до стабильного full-book source/build contract;
- миграция содержимого «Буфера».
- ослабление acceptance thresholds самим extractor/renderer без отдельного owner decision.
- выдача агентам raw sources, control plane, drafts или unresolved proposals.
- автоматическая генерация схем/Project Tool только по свободному тексту без typed engineering contract.

## Tool check

Готового зарегистрированного инструмента для полного цикла Standard as Code нет. Google Drive/Docs использован только для read-only аудита. Локальные Markdown/YAML artifacts созданы штатными file tools. После approve требуется отдельный Do на разработку и регистрацию общего CLI, schema и build route; новые `C:/AI/CORD/scripts/*.py` до этого решения не создаются.

## Предлагаемый ответ

- `approve D1-D7,D9-D11` — перейти к full-book lossless import, внедрению EDT/access contracts и первому deep slice раздела 5 «Освещение» без внешней публикации; D8 уже действует как owner requirement;
- `revise D...` — изменить конкретный default, остальные сохранить;
- `reject` — оставить Google Doc источником истины и закрыть инициативу.

## Следующий Do после approve

Подготовить исполняемый технический пакет фазы 2:

1. JSON Schemas и design-token contract;
2. schema/template редакционного задания EDT и зарегистрированный action/tool route;
3. topic/rule/entity/relation schemas и query/audit answer contract;
4. read-only extractor/inventory для всей книги;
5. full-book lossless source tree и assets manifest;
6. generated agent package и фасетные индексы для раздела 5 «Освещение»;
7. dual-profile source/build для раздела 5 «Освещение»;
8. lighting parity/refactoring/access report и full-book migration plan, без изменения Google Doc.

## Resolution

Пользователь утвердил D1–D7 и D9–D11 и поручил перейти к реализации. D8 не входит в текущий Do: независимая приемка остается обязательным последующим gate и запускается только после появления полного baseline и deterministic build candidate.

Решение: [[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-05_Standard_As_Code_Architecture_D1_D11]].

Исполнение: [[01_Projects/001_77_Standard_iRidi/Archive/Backlog/Done/DO-001-STD-AS-CODE-001_Implement_Approved_Architecture]].
