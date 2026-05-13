# sasha

Marketplace плагинов Claude Code от [@agh0](https://github.com/agh0).

## Плагины

### svoislova

Анализирует текст через API [svoislova.ru](https://svoislova.ru), находит иностранные слова с риском medium и выше, придумывает русские альтернативы и выдаёт таблицу замен с переписанным текстом.

### google-doc-md-to-html

Конвертирует Markdown-файл (в том числе экспорт из Google Docs) в минималистичный HTML5 — только базовый whitelist тегов, без CSS, без классов, без скриптов. Детерминированный Python-скрипт, не LLM. Требует `markdown` и `bleach` (`pip install markdown bleach`).

## Установка

В Claude Code:

```
/plugin marketplace add agh0/sasha
/plugin install svoislova@sasha
/plugin install google-doc-md-to-html@sasha
```

После установки скилл активируется автоматически, когда вы просите Claude выполнить соответствующую задачу.

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
│   └── plugin.json            # манифест плагина svoislova
├── skills/
│   └── svoislova/
│       ├── SKILL.md
│       └── scripts/analyze.py
└── plugins/
    └── google-doc-md-to-html/
        ├── .claude-plugin/plugin.json
        └── skills/google-doc-md-to-html/
            ├── SKILL.md
            └── scripts/convert.py
```

## Лицензия

[MIT](LICENSE)
