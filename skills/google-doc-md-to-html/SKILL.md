---
name: google-doc-md-to-html
description: Конвертирует Markdown-файл (в том числе экспорт из Google Docs) в минималистичный HTML5 — только базовый whitelist тегов, без CSS, без классов, без скриптов. Используй этот скилл, когда пользователь просит «сделать html из markdown», «конвертировать md в html», «переделать .md в .html», «преобразуй markdown в html», «html из google docs markdown», «экспорт из google docs в html», когда пользователь передаёт .md файл с просьбой получить .html, или упоминает google-doc-md-to-html.
---

# google-doc-md-to-html — Markdown → минималистичный HTML

## Что делает

Детерминированно преобразует `.md` в `.html` через bundled Python-скрипт. На выходе — валидный HTML5 со строгим whitelist'ом тегов, без `class`, `id`, `style`, без `<div>`/`<span>`, без `<script>`/`<style>`/`<link>`.

## Как вызывать

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/google-doc-md-to-html/scripts/convert.py" <input.md> [output.html]
```

Также допустим stdin:

```bash
cat input.md | python3 "${CLAUDE_PLUGIN_ROOT}/skills/google-doc-md-to-html/scripts/convert.py" --stdin > output.html
```

Скрипт печатает в stdout абсолютный путь к созданному файлу (или сам HTML при `--stdin`). Ошибки — в stderr, exit code ≠ 0.

## Алгоритм работы

1. Определи путь к входному `.md` из сообщения пользователя или приложенного файла.
2. Если пользователь не указал выходной путь — используй то же имя с расширением `.html` в той же директории.
3. Вызови скрипт.
4. Сообщи пользователю путь к созданному файлу одной строкой. Не вставляй сырой HTML в чат.
5. Если скрипт завершился с ошибкой — покажи stderr пользователю.

## Зависимости

Скрипт использует `markdown` и `bleach`. Если их нет — скрипт сам подскажет команду установки в stderr (`pip install markdown bleach`).

## Что НЕ делать

- Не редактируй HTML после генерации — он уже соответствует требованиям.
- Не добавляй CSS, классы, скрипты «для красоты».
- Не показывай содержимое HTML в чат, если пользователь явно не попросил.
