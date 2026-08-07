---
type: decision
status: applied
created: 2026-08-07
project: 77 Standard iRidi
project_id: "001"
privacy: internal
origin: human
source_ref: "[[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-08-07_Lighting_Render_Contract_Pilot_Review]]"
approval_ref: "user: в целом мне нравится апрув"
contract_uid: std_render_contract_v1
canonical_contract_ref: "[[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_render_contract_v1.yaml]]"
---

# Решение: утвердить контракт генерации RC1

Связано с [[01_Projects/001_77_Standard_iRidi/Standard_iRidi_MOC]], [[01_Projects/001_77_Standard_iRidi/Archive/Reviews/Applied/2026-08-07_Lighting_Render_Contract_Pilot_Review]], [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/standard_render_contract_v1.yaml]] и [[01_Projects/001_77_Standard_iRidi/Backlog/DO-001-STD-LIGHTING-REF-001_Refactor_Lighting_Content]].

## Принято

- source-to-view архитектура `book -> section -> topic -> content`;
- один renderer для крупного раздела и полной книги;
- единая иерархия заголовков и автоматически формируемая навигация;
- читаемая ширина листа и адаптивные боковые поля;
- детерминированные правила таблиц, колонок и изображений для HTML и DOCX;
- «Освещение» как первый глубокий раздел при обязательном масштабе всей книги;
- обязательные machine UID, source refs и transformation trace.

## Граница решения

Этим approve не утверждены:

- смысловая правильность старого текста и 96 кандидатов норм «Освещения»;
- candidate-контракт содержательных шаблонов;
- D8, cutover, публикация, изменение Google Doc или Wiki;
- пиксельное равенство старого и нового документа.

## Применение

- канонический машинный контракт: `std_render_contract_v1`;
- исходный candidate сохранен как утвержденный snapshot предложения;
- review RC1 закрыт и перенесен в applied archive;
- следующий контур — отдельное согласование содержательного шаблона и редакционного задания на рефакторинг «Освещения».
