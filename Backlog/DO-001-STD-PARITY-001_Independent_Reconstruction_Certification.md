---
type: verification_do
status: waiting_for_source
id: DO-001-STD-PARITY-001
project: 77 Standard iRidi
project_id: "001"
created: 2026-08-05
privacy: internal
source_ref: "user acceptance clarification in Codex task 2026-08-05"
action_id: TBD
baseline_uid: baseline_19K5o8mg_288e8eead70d07c1
release_candidate_uid: std_release_010_fe753b2355
requirement_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Reconstruction_Parity_Acceptance_v1]]"
refactoring_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]]"
blocked_by:
  - approved_full_transformation_manifest
  - independent_visual_certifier_environment
trigger: "Activate after exact baseline_uid and full_book_release_candidate_uid are both fixed and every blocked_by item is resolved."
tool_gap: "LibreOffice/page raster and independent full-book comparison route are not available; do not self-certify with the implementation CLI"
approval: owner_has_approved_the_acceptance_principle_but_not_cutover_or_external_publish
---

# DO-001-STD-PARITY-001: независимая сертификация реконструкции книги

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Reconstruction_Parity_Acceptance_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_Content_Refactoring_And_Template_Model_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Architecture_v1]], [[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-08-05_Standard_As_Code_Architecture_Review]], [[03_Resources/CORD_Methodology/Do_Execution_And_Tools]], [[03_Resources/Tool_Registry/Tool_Registry_MOC]] и [[03_Resources/Action_Registry/Action_Registry_MOC]].

## Goal

Независимо подтвердить, что `legacy-fidelity` соответствует зафиксированной исходной книге, а `standard-normalized` соответствует normalized source, template contract и approved transformation manifest без необъясненной потери смысла, таблиц, изображений, трассировки или воспроизводимости.

## Почему это отдельная задача

Extractor/renderer не должен сам сертифицировать собственный результат. Эта задача запускается в отдельном чистом контексте после появления полного release candidate и не получает права исправлять проверяемый source/build во время аудита.

## Inputs

- immutable baseline package;
- approved source schema и acceptance contract;
- migrated full content tree;
- build command и environment lock;
- generated PDF, DOCX, Google Doc draft/export и agent package;
- `legacy-fidelity` и `standard-normalized` profiles;
- approved transformation manifest и template version;
- release candidate manifest.

## Outputs

- evidence folder `QA/Reconstruction_Parity/<run_uid>/`;
- PASS/FAIL по gates G1–G8;
- visual overlays и machine-readable diffs;
- классифицированные defects;
- final certificate;
- при FAIL — отдельные defect Do без молчаливого изменения acceptance threshold.

## Tool plan

Требуется зарегистрированный certifier route поверх будущего `standard_book.py`, PDF/DOCX/Google Docs inventory, text/table/asset comparators и page raster visual diff. Существующие общие CORD audits проверяют lifecycle/trace, но не обеспечивают book reconstruction parity.

До реализации общего инструмента нельзя заменять его ручным одноразовым просмотром книги.

## Activation gate

Перевести `waiting_for_source -> approved/in_progress` только когда выполнены все `blocked_by` и зафиксированы exact baseline UID и release candidate UID.

## Completion

`done` допускается только при final certificate `ACCEPTED` и PASS по G1–G8. `FAIL_IMPLEMENTATION` или `FAIL_ARCHITECTURE` не закрывает задачу: создается следующий certification run после исправлений.
