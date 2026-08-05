# archive — согласованные материалы из inbox

Здесь хранятся папки задач, по которым вы **приняли решение**: изменения применены, отклонены или применены частично.

Inbox — только активная очередь. Archive — журнал и аудит.

## Структура папки в archive

```
archive/
  YYYY-MM-DD_краткий-slug/
    meta.yaml        # финальный status, даты, ссылки на правки
    content.md       # исходный обработанный материал (копия из inbox)
    proposal.md      # предложение агента
    resolution.md    # ваше решение + что сделано
```

## Поля resolution в meta.yaml

```yaml
resolution: applied | rejected | partial
resolved_at: 2026-07-03T14:00:00+05:00
resolved_by: Василий Татаринов
book_changes:
  - target: book-main
    section: "4.9.2"
    url: https://docs.google.com/document/d/19K5o8mg.../edit
    note: добавлен абзац про UPS LiFePO4
wiki_changes: []   # или список URL/разделов Wiki
```

## Правила

- **Не удалять** папки из archive — только добавлять.
- Имена папок **сохранять** как в inbox (тот же slug).
- При `partial` в `resolution.md` перечислить, что не вошло в книгу и нужно ли новое inbox-задание.

