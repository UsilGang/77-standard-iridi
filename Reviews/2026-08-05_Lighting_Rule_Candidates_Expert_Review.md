---
type: standard_review
status: review
project: 77 Standard iRidi
project_id: "001"
created: 2026-08-05
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Implementation_Report_2026-08-05]]"
action_id: operate_standard_book
blocker: needs_human_decision
decision_scope: lighting_rule_candidate_batch
candidate_count: 96
---

# Экспертный review кандидатов норм раздела «Освещение»

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Implementation_Report_2026-08-05]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]] и [[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-05_Standard_As_Code_Architecture_D1_D11]].

## Что подготовлено

CLI нашел 96 фрагментов с нормативной лексикой в 64 темах раздела «Освещение». Private candidate package хранит statement, topic UID, line locator, lexical trigger и предварительную классификацию. Ни один кандидат не включен в действующие `rules.yaml` или agent package.

## Что должен решить эксперт

Для каждого кандидата требуется один disposition:

- `approve_as_rule`: подтвердить statement, claim type, normative level, scope, applicability, rationale, exceptions и authority;
- `merge_with_rule`: связать с одной общей нормой вместо дублирования;
- `keep_informative`: оставить объяснением, не превращать в норму;
- `revise`: переписать без изменения смысла и повторно проверить;
- `reject`: ложная эвристика, контекстный текст или устаревшее утверждение;
- `product_gap`: для подтверждения нужна разработка или продуктовое решение.

## Приемка batch

- у каждого принятого правила есть source_ref и decision_ref;
- дубли не создают несколько UID одной нормы;
- конфликт или недостаток данных не скрывается формулировкой;
- changeset перечисляет exact changed UIDs и version impact;
- опубликование не выполняется в рамках этого review.

## Решение нужно

Утвердить отдельный экспертный batch review 96 кандидатов. До решения раздел остается структурно мигрированным, но пресейл-аудит корректно возвращает `needs_input` для нормативной проверки.
