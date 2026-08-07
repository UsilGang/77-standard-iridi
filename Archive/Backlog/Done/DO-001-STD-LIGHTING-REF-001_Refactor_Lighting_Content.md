---
type: content_refactoring_do
status: done
id: DO-001-STD-LIGHTING-REF-001
project: 77 Standard iRidi
project_id: "001"
created: 2026-08-07
privacy: internal
source_ref: "[[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-07_Standard_Render_Contract_RC1_Approval]]"
approval_ref: "[[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-07_Content_Template_CT1_And_Lighting_EDT1_Approval]]"
render_contract_uid: std_render_contract_v1
section_uid: std_ch_lighting
blocked_by: []
approval: ct1_and_edt1_approved
completed_at: 2026-08-07
result_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Reports/2026-08-07_Lighting_CT1_EDT1_Implementation_Report]]"
---

# DO-001-STD-LIGHTING-REF-001: содержательный рефакторинг «Освещения»

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_render_contract_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_template_contract_candidate_v1]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Editorial_Assignment_And_Versioning_Model_v1]] и [[01_Projects/001_77_Standard_iRidi/Decisions/2026-08-07_Standard_Render_Contract_RC1_Approval]].

## Цель

После отдельного утверждения содержательного шаблона и редакционного задания привести раздел `std_ch_lighting` к единой структуре без скрытых смысловых изменений и с полной трассировкой каждого преобразования.

## Обязательные входы

- утвержденный content template contract;
- редакционное задание с целями, границами, source refs, затрагиваемыми UID и критериями приемки;
- перечень transformation operations для перемещения, объединения, разделения, дедупликации и уточнения текста;
- отдельные human decisions для изменения норм, удаления содержания и разрешения противоречий.

## Выходы

- обновленный normalized source раздела «Освещение»;
- changeset и transformation manifest;
- повторная сборка раздела и всей книги одним renderer;
- сравнительный отчет по разрешенным изменениям;
- пакет нерешенных смысловых вопросов без их молчаливого применения.

## Граница

RC1 разрешил renderer и визуальный контракт, но не разрешил автоматически переписывать содержание. CT1 и EDT1 утверждены отдельным решением; локальный трассируемый рефакторинг завершен. Нормы, публикация и независимый D8 остаются отдельными gates.

## Результат

- 64/64 темы получили template slot, topic archetype и explicit disposition;
- раздел и полная книга пересобраны одним renderer;
- source/browser/package audits прошли без findings;
- нерешенные смысловые gaps вынесены в [[01_Projects/001_77_Standard_iRidi/Reviews/2026-08-07_Lighting_Content_Gaps_Expert_Review]].
