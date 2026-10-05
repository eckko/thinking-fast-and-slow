# Testing

## Automated checks

```bash
pip install playwright && playwright install chromium   # once
python3 tests/run_tests.py
```

`tests/run_tests.py` starts `python3 -m http.server` on port 8765, opens
headless Chromium, and checks:

| Test function | What it proves |
|---|---|
| `test_every_question_type` | every question in `questions.json`, answered right gives "Marks: 1 out of 1", answered wrong gives "0 out of 1", with no page errors |
| `test_confidence_check` | the answer area is locked until a confidence level is picked; a "Certain" miss is flagged on the results |
| `test_timed_session` | the pill shows "Time left" and the card shows the session clock |
| `test_question_timer_runs_out` | with a fake clock, an unanswered question shows "Time's up." |
| `test_old_progress_is_upgraded` | a version-1 save shows in recent results and stats, and is re-saved as version 2 |
| `test_backup_without_version_keeps_progress` | loading a v2 backup that lacks `version` keeps the progress instead of wiping it |
| `test_book_labels` | `labels` in questions.json change the words on the page |
| `test_themes` | one tile per theme folder; choosing a theme and dark mode sets `data-theme`/`data-scheme`, and survives reload |
| `test_phone_width` | no sideways scrolling at 375px |

Tests use `page.route` to serve a made-up `questions.json` when they need
a single question or custom labels, and block Google Fonts so they run
offline.

To add a check: write a `test_...(browser)` function that uses
`open_page`, `start_session`, `answer_question` and `check`, and call it
from `main()`.

## Visual checks

The tests do not look at pixels. For styling or theme changes, take
screenshots with Playwright (or open the page) and compare:

- every changed theme, in light and dark
- the home screen, a question before and after answering (right and
  wrong), the results screen, and a timed session
- a 375px wide phone view

Useful tricks for repeatable screenshots:

- `reduced_motion="reduce"` on the page stops animations and confetti.
- `page.clock.set_fixed_time(...)` freezes dates and timers.
- Replace `Math.random` with a seeded generator in an init script so the
  shuffles are the same every run.
- Set the theme before load with an init script:
  `localStorage.setItem('recall-quiz:theme',
  JSON.stringify({t: 'lego', m: 'dark'}))`.

## Line length

```bash
find . -name "*.js" -o -name "*.css" -o -name "*.py" -o -name "*.html" \
  | grep -v -e themes.css -e themes-list.js \
  | xargs awk 'length > 79 {print FILENAME":"FNR}'
```

should print nothing.
