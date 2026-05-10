# sasha

Marketplace плагинов Claude Code от [@agh0](https://github.com/agh0).

## Плагины

### svoislova

Анализирует текст через API [svoislova.ru](https://svoislova.ru), находит иностранные слова с риском medium и выше, придумывает русские альтернативы и выдаёт таблицу замен с переписанным текстом.

## Установка

В Claude Code:

```
/plugin marketplace add agh0/sasha
/plugin install svoislova@sasha
```

После установки скилл активируется автоматически, когда вы просите Claude проверить текст на заимствования, найти замены или «обрусить» текст.

## Использование

```
проверь этот текст на иностранные слова: ...
```

Claude вызовет скилл и вернёт таблицу замен:

```
| Слово в тексте | Риск | Рекомендуемые замены |
|---|---|---|
| дедлайн | 🔴 high | срок, крайний срок, контрольная дата |
| митинг | 🟡 medium | совещание, собрание |

Переписанный текст:
...
```

## Структура

```
sasha/
├── .claude-plugin/
│   ├── marketplace.json   # манифест marketplace
│   └── plugin.json        # манифест плагина svoislova
└── skills/
    └── svoislova/
        ├── SKILL.md       # инструкции для Claude
        └── scripts/
            └── analyze.py # обёртка над svoislova.ru/analyze
```

## Лицензия

[MIT](LICENSE)
