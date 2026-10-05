# Recall Quiz

A static, no-build quiz page for any book. Open `index.html` (or host the folder on GitHub Pages).
Progress is saved in the browser (localStorage); there is a Download/Load backup for moving between devices.

## Files

| File | What it does | Edit by hand? |
|---|---|---|
| `index.html` | Page structure only | rarely |
| `quiz.css` | Layout and the default look; **phone rules are the last block** | yes |
| `app.js` | Quiz logic (sessions, spaced repetition, question types, results) | yes |
| `theme.js` | Light/dark/system and the theme picker | rarely |
| `themes.css`, `themes-list.js` | **Generated** from `tools/`. Colours, art, fonts, theme list | no, run the generator |
| `questions.json` | The questions for one book | yes (per book) |
| `tools/gen_themes.py`, `tools/gen_more.py` | Theme generator | to add themes |

## Use it for another book

Only `questions.json` changes. Keep one folder (or repo) per book, or swap the file.

```json
{
  "id": "my-book",                  // used for the progress save key, keep it unique per book
  "book": "My Book Title",
  "labels": { "unit": "Chapter", "units": "chapters", "topic": "Topic", "whole": "Whole book" },
  "questions": [ { "id": "c01-1", "unit": "Chapter 1", "unitTitle": "...", "section": "...", "kind": "mcq", "q": "...", "explain": "..." } ]
}
```

`labels` is optional. Use `"unit": "Lesson"`, `"units": "lessons"` for a course, `"topic": "Section"`, and so on.

Fields by `kind` (all kinds also take `id unit unitTitle section q explain`):

| kind | extra fields |
|---|---|
| `mcq` | `options[]`, `answer` (index) |
| `tf` | `answer` true/false |
| `multi` | `options[]`, `answers[]` (indexes) |
| `fill` | `accept[]` (accepted answers; small typos tolerated) |
| `order` | `items[]` in the correct order (shown shuffled) |
| `match` | `pairs[[left, right], ...]` |
| `sort` | `groups[]`, `items[{t, g}]` (g = group index) |
| `recall` | `a` (model answer; the learner self-grades) |

## Add a question type

1. Write `function myType(q, area, keys)` in `app.js` next to the others. Draw into `area`; when the learner has answered call `settle(q, area, keys, "got" | "part" | "miss")`.
2. Register it in the `TYPES = {...}` line at the end of `app.js`.
3. Add its label to `KIND` near the top. Done.

## Add a theme

Themes are generated so each one stays small. In `tools/gen_more.py` add one `add(...)` call (copy any existing one):

```python
add('key', 'Display name',
    'paper card ink mut line acc acc2 hl c1 c2 c3 c4',   # light colours (12 hex values)
    'paper card ink mut line acc acc2 hl c1 c2 c3 c4',   # dark colours, same order
    (sans_font, heading_font), (corner_radius, small_radius),
    background_function, mascot_svg_body, start_icon_svg_body)
```

Then run `python3 tools/gen_themes.py`. It rewrites `themes.css` and `themes-list.js`, adds the tile to the picker and loads the fonts. Nothing else to touch.
For fine-tuning one theme, put extra CSS in the `h1=` argument (see the existing themes).
Colour roles: `paper` page, `card` panels, `ink` text, `mut` secondary text, `line` borders, `acc/acc2` buttons, `hl` highlighter, `c1..c4` accents.
Keep text/background contrast readable in both light and dark.

## Memory model

Levels 0 to 4 with review gaps of 0, 1, 3, 7 and 21 days (`STEPS` in `app.js`). Right answers move a question up a level, wrong ones send it back.

## Known limits

- Art is original and generic; Google Fonts need a network connection (fallback fonts are used offline).
- Opened from `file://` the browser blocks reading `questions.json`; the page then shows a file picker.
