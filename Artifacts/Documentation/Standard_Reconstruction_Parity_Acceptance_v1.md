---
type: reconstruction_parity_acceptance_contract
status: active_requirement
project: 77 Standard iRidi
project_id: "001"
version: "1.0"
created: 2026-08-05
privacy: internal
origin: mixed
authority_weight: owner_requirement
verification: pending_implementation_and_independent_certification
allowed_use: project_context
source_ref: "user acceptance clarification in Codex task 2026-08-05"
---

# Контракт приемки реконструкции книги

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Current_Book_Structure_Audit_2026-08-05]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/Standard_Book_Manifest_MOC]], [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-05_Standard_As_Code_Architecture_Review]] и [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-PARITY-001_Independent_Reconstruction_Certification]].

## Критерий завершения этапа

Этап перевода книги в машиночитаемые артефакты считается завершенным не после создания структуры или успешного запуска сборщика, а только после независимого подтверждения следующей цепочки:

```text
зафиксированная исходная книга
  -> машиночитаемые артефакты
  -> чистая детерминированная сборка
  -> реконструированная книга
  -> независимое сравнение
  -> PASS по всем обязательным gates
```

Если `legacy-fidelity` не совпадает с исходником по содержанию, структуре, изображениям и существенному оформлению, результат не принимается. `Standard-normalized` может намеренно отличаться, но только по versioned template и approved transformation manifest. Любое необъясненное отличие блокирует приемку.

## Двойной объект приемки

1. `legacy-fidelity` доказывает lossless import и способность воспроизвести исходник;
2. `standard-normalized` доказывает унификацию по template contract без потери смысла и побочных правил;
3. cross-profile check доказывает, что каждый legacy element имеет normalized target или explicit approved disposition, а каждый delta — operation UID.

Так человеческая ошибка не становится обязательным шаблоном, но и не исчезает молча.

## Принцип независимости

Приемку нельзя считать обычной самопроверкой build script.

- Мигратор и renderer производят результат и технические логи.
- Отдельная задача-certifier получает immutable baseline, release candidate, generated outputs и этот контракт.
- Certifier не исправляет source tree, extractor или renderer во время проверки.
- Certifier выдает только evidence-backed `PASS` или `FAIL` с классифицированными отклонениями.
- После исправлений запускается новый certifier run на чистой сборке.
- Автор реализации не может заменить приемочный отчет утверждением «визуально похоже».

Задача владельца — согласовать архитектурный критерий один раз. Перелистывать две книги и вручную ловить расхождения владелец не должен.

## Что фиксируется как baseline

До миграции полного текста создается immutable baseline package:

1. Google Doc ID, tab IDs, revision/snapshot locator и время фиксации;
2. экспорт исходной книги в PDF и DOCX;
3. структурный inventory: вкладки, заголовки, абзацы, списки, таблицы, изображения, links, headers/footers;
4. исходные изображения и object mapping, где API это позволяет;
5. page/style profile: A4, поля, шрифты, размеры, цвета, spacing, page breaks, callouts;
6. checksums всех baseline-файлов;
7. перечень известных дефектов: они сохраняются в `legacy-fidelity`, но исправляются в `standard-normalized` только через transformation operation и нужный gate.

Baseline package после фиксации не обновляется вслед за мигратором. Если исходная книга продолжила меняться, создается новый baseline UID и проверка явно выбирает один из них.

## Обязательные gates

### G1. Composition and accountability parity

- 100% legacy-вкладок/глав учтены в fidelity/accountability mapping;
- composition `standard-normalized` соответствует approved book manifest;
- в `legacy-fidelity` порядок, заголовки, уровни, нумерация и оглавление воспроизведены;
- в `standard-normalized` структура соответствует template/manifest, а отличия имеют operation UID;
- Buffer и иные staging-данные не попали в published view;
- нет неожиданных пустых или дополнительных разделов.

### G2. Text and semantic parity

- 100% исходных опубликованных текстовых блоков сопоставлены с target UID;
- нет пропавшего или добавленного текста без approved change/refactoring operation UID;
- diff `legacy -> lossless import` равен нулю после технической нормализации;
- diff `lossless import -> normalized source` полностью покрыт transformation manifest;
- нормативный смысл, ограничения, числовые значения, единицы измерения и product facts не изменились;
- перенос текста между темами не меняет semantic digest соответствующего claim/rule.

### G3. Tables, lists and callouts parity

- 100% таблиц присутствуют и имеют те же данные, порядок строк/столбцов, merge и подписи;
- списки сохраняют порядок, вложенность и тип нумерации;
- warning, recommendation, example и иные визуальные выноски не превращены в обычный неразличимый текст;
- формулы, обозначения и специальные символы не потеряны.

### G4. Asset parity

- 100% изображений и схем сопоставлены с постоянными asset UID;
- checksum/перцептивный hash подтверждает правильный исходный asset;
- не потеряны подписи, credit/source restrictions и связи с темами;
- в `legacy-fidelity` placement, порядок, размер, crop, aspect ratio и обтекание воспроизведены в tolerance;
- в `standard-normalized` asset identity/content сохранены, а placement соответствует template и operation manifest;
- нет placeholder, broken image или случайной подмены версии изображения.

### G5. Visual fidelity and template conformance

- `legacy-fidelity` совпадает с baseline по формату, сетке и legacy styles;
- `standard-normalized` соответствует versioned theme/template, а не случайным различиям legacy sections;
- проверены шрифты, размеры, цвета, интервалы и выравнивание;
- headers/footers, номера страниц, page breaks и оглавление работают;
- rasterized comparison `legacy-fidelity -> baseline` не содержит критических зон расхождения;
- visual QA `standard-normalized` проверяет единообразие, missing/overflow/collision и approved layout changes;
- страницы `legacy-fidelity` ниже visual threshold блокируют приемку.

Первоначальные технические thresholds для пилота:

- средняя page similarity не ниже `0.985`;
- ни одна страница не ниже `0.970` без approved exception;
- геометрическое отклонение ключевого объекта не более `2 pt` или согласованного renderer tolerance;
- aspect ratio изображений — точное совпадение;
- approved exceptions перечислены по UID, странице, причине и decision ref.

Threshold применяется к `legacy-fidelity` и не заменяет содержательные gates. Pixel difference normalized view с legacy ожидаем при утвержденной унификации; необъясненное отличие остается дефектом.

### G6. Traceability parity

- каждый migrated topic/rule/asset имеет locator в baseline;
- каждый intentional delta имеет editorial job UID, changeset UID и decision ref;
- по generated fragment можно пройти назад до source artifact и baseline object;
- по change card можно получить список изменившихся страниц и UID.

### G7. Build determinism

- сборка запускается одной документированной командой из clean source state;
- две независимые сборки с одним lock manifest дают одинаковый semantic manifest и content checksums;
- timestamps и иные допустимые nondeterministic metadata нормализованы или исключены из сравнения;
- ручная правка generated book после build запрещена;
- версия renderer, fonts, templates и dependencies зафиксирована.

### G8. Output usability

- оглавление, внутренние ссылки и bookmarks работают;
- текст доступен для поиска и копирования;
- agent knowledge package возвращает те же released UID и не читает draft/Buffer;
- PDF/DOCX/Google Doc profile не теряет обязательное содержание;
- generated release содержит version, date, changelog и manifest ref.

## Evidence package приемочной задачи

Certifier обязан создать отдельный immutable run folder:

```text
QA/Reconstruction_Parity/<run_uid>/
  certification.yaml
  baseline-manifest.json
  generated-manifest.json
  semantic-diff.json
  transformation-coverage.json
  template-conformance.json
  structure-diff.json
  table-diff.json
  asset-diff.csv
  visual-diff/
    page-metrics.csv
    overlays/
  traceability-report.json
  reproducibility-report.json
  findings.md
  final-certificate.md
```

`final-certificate.md` должен содержать:

- baseline UID и release candidate UID;
- версии extractor, schema, renderer, templates и environment lock;
- PASS/FAIL по G1–G8;
- число проверенных глав, тем, таблиц, изображений и страниц;
- список всех approved exceptions;
- residual risks;
- итог `ACCEPTED` только при полном PASS обязательных gates.

## Модель результата

Допустимы только три технических статуса:

| Статус | Смысл | Следующий переход |
| --- | --- | --- |
| `PASS` | G1–G8 выполнены, необъясненных отклонений нет | можно выносить cutover/release на approve |
| `FAIL_IMPLEMENTATION` | архитектура достаточна, дефект в extractor/data/renderer/environment | создать defect Do, исправить и повторить clean certification |
| `FAIL_ARCHITECTURE` | текущая модель артефактов не может воспроизвести важную часть книги | вернуть architecture review с конкретным missing contract |

Условного «в целом похоже» или частичной приемки полного этапа нет. Отдельный раздел-пилот может иметь pilot certificate, но он не подтверждает готовность всей книги.

## Итерационный цикл без нагрузки на владельца

```text
certify
  -> PASS -> короткий сертификат владельцу
  -> FAIL_IMPLEMENTATION -> defect backlog -> fix -> clean rebuild -> certify
  -> FAIL_ARCHITECTURE -> architecture revision -> rebuild -> certify
```

Владелец подключается повторно только если обнаружен настоящий trade-off: требуемая визуальная точность конфликтует с выбранным output format, нужен новый канонический формат либо proposed exception меняет пользовательское качество. Обычные технические дефекты команда устраняет внутри согласованного контура.

## Definition of Done инициативы

Инициатива Standard as Code не считается завершенной, пока одновременно не существуют:

1. approved source schema и artifact architecture;
2. полностью мигрированные lossless import и normalized released content tree;
3. детерминированный build tool;
4. reconstructed `legacy-fidelity` и `standard-normalized` full books;
5. independent certification package с `PASS` по G1–G8;
6. проверенный rollback к baseline;
7. отдельное решение о cutover Google Doc из source of truth в generated view.
