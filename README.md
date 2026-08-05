# 77 Standard iRidi

Самостоятельный репозиторий проекта по переводу «Стандарта автоматизации iRidi» в управляемую модель Standard as Code.

Цель проекта — хранить стандарт как версионируемое ядро знаний, из которого детерминированно собираются:

- человекочитаемая книга;
- представления для инсталляторов, продаж, пресейла и обучения;
- машиночитаемый пакет знаний для агентов;
- история изменений, редакционные задания и release delta.

## С чего начать

1. [`Artifacts/Documentation/Standard_As_Code_Implementation_Report_2026-08-05.md`](Artifacts/Documentation/Standard_As_Code_Implementation_Report_2026-08-05.md) — что реализовано, проверено и что остается на D8.
2. [`Archive/Reviews/Applied/2026-08-05_Standard_As_Code_Architecture_Review.md`](Archive/Reviews/Applied/2026-08-05_Standard_As_Code_Architecture_Review.md) — утвержденная архитектура и исходный лист согласования.
3. [`Artifacts/Documentation/Package_Index.md`](Artifacts/Documentation/Package_Index.md) — состав документационного пакета.
4. [`Workspace/77_Стандарт_iRidi/README.md`](Workspace/77_Стандарт_iRidi/README.md) — рабочий контур стандарта.

## Статус

Архитектура D1–D7 и D9–D11 утверждена и реализована: есть schemas, CLI, dual-profile build, agent package, editorial trace, release candidate и `$standard-book-operator`. Текущий Google Doc остается действующим каноном до независимого D8 PASS и отдельного cutover/publication approve.

## Что включено

- проектные правила и рабочая очередь предложений;
- архитектура Standard as Code;
- модели редакционного задания, версионности и доступа агентов;
- кандидаты машинных контрактов YAML/CSV;
- критерии качества и независимой приемки;
- schemas, theme tokens, subsystem template, deterministic CLI, tests and operator skill;
- безопасные editorial/transformation manifests без полного текста книги;
- локальные обработанные summaries и source locators, необходимые для трассировки решений.

## Что не включено

- исходные аудиозаписи и полные транскрипты;
- содержимое внешних систем и других проектов CORD;
- секреты, учетные данные и локальные runtime-артефакты;
- полный текст действующей книги, baseline, images, builds, agent package и release candidate: они существуют локально, но не публикуются без отдельного approve.

Часть Obsidian-ссылок указывает на материалы полного CORD vault и в автономном репозитории служит трассировочным идентификатором.

## Скачать

- Репозиторий: <https://github.com/UsilGang/77-standard-iridi>
- ZIP-архив последней версии: <https://github.com/UsilGang/77-standard-iridi/archive/refs/heads/main.zip>
