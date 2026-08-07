# Предложение: CT1 + EDT-2026-0001

Связано с [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Content_Template_And_Lighting_EDT_Review]], [candidate-контрактом CT1](../../../../Artifacts/Machine_Readable/standard_template_contract_candidate_v1.yaml) и [[01_Projects/001_77_Standard_iRidi/Workspace/77_Стандарт_iRidi/inbox/2026-08-07_lighting-content-template-pilot/brief]].

## Целевой контур

| Куда | Scope | Действие |
| --- | --- | --- |
| normalized source | `std_ch_lighting` и 64 descendant topics | controlled refactor после approve |
| generated views | «Освещение» + вся книга | rebuild и explained-delta audit |
| agent package | lighting fragments/indexes | regenerate и query smoke tests |
| Google Doc / Wiki | — | не менять |

## Решения

- `CT1`: утвердить двухуровневую модель section template + topic archetypes и missing-slot policy.
- `EDT1`: разрешить локальный трассируемый рефакторинг всего раздела «Освещение» в границах `editorial.yaml`.

## Не входит

- утверждение норм и продуктовых фактов;
- добавление отсутствующего знания по ПНР/приемке;
- удаление или deprecation;
- публикация и D8.

## После approve

Candidate-контракт превращается в `standard_templates_1`, EDT переходит `approved -> in_progress`, а результат возвращается одним сравнительным review-пакетом: исходник, normalized view, объясненные изменения, gaps и отдельные semantic decisions.
