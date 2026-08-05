# standard-src

Связано с [[01_Projects/001_77_Standard_iRidi/Artifacts/Machine_Readable/Standard_Book_Manifest_MOC]] и [[01_Projects/001_77_Standard_iRidi/Artifacts/Documentation/Standard_As_Code_Implementation_Report_2026-08-05]].

Редактируемое ядро стандарта. Файлы этого слоя создаются и проверяются `tooling/standard_book.py`.

- `book.yaml` — состав книги и порядок разделов;
- `sections/` — section/topic/rule content;
- `entities/` — продукты, capabilities, protocols и роли;
- `assets/` — изображения, схемы и data assets с checksum;
- `taxonomy/` — аудитории, jobs, coverage statuses и normative levels;
- `staging/` — Buffer и другие непубликуемые материалы.

Полный импорт действующей книги является внутренним source package. До отдельного publication approve он не отправляется в открытый GitHub remote.
