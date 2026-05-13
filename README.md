# sasha

Плагин Claude Code от [@agh0](https://github.com/agh0). Содержит два скилла.

## Скиллы

### svoislova

Анализирует текст через API [svoislova.ru](https://svoislova.ru), находит иностранные слова с риском medium и выше, придумывает русские альтернативы и выдаёт таблицу замен с переписанным текстом.

### google-doc-md-to-html

Конвертирует Markdown-файл (в том числе экспорт из Google Docs) в минималистичный HTML5 — только базовый whitelist тегов, без CSS, без классов, без скриптов. Детерминированный Python-скрипт, не LLM. Требует `markdown` и `bleach` (`pip install markdown bleach`).

## Установка

В Claude Code:

```
/plugin marketplace add agh0/sasha
/plugin install sasha@sasha
```

После установки оба скилла активируются автоматически, когда вы просите Claude выполнить соответствующую задачу.

## Использование

**svoislova:**

```
проверь этот текст на иностранные слова: ...
```

Claude вернёт таблицу замен:

```
| Слово в тексте | Риск | Рекомендуемые замены |
|---|---|---|
| дедлайн | 🔴 high | срок, крайний срок, контрольная дата |
| митинг | 🟡 medium | совещание, собрание |

Переписанный текст:
...
```

**google-doc-md-to-html:**

```
конвертируй doc.md в html
```

Claude вызовет скрипт и сообщит путь к `doc.html`.

## Структура

```
sasha/
├── .claude-plugin/
│   ├── marketplace.json       # манифест marketplace
│   └── plugin.json            # манифест плагина sasha
└── skills/
    ├── svoislova/
    │   ├── SKILL.md
    │   └── scripts/analyze.py
    └── google-doc-md-to-html/
        ├── SKILL.md
        └── scripts/convert.py
```

## Лицензия

[MIT](LICENSE)
