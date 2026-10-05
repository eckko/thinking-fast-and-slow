# Quiz-Book Prompt

Paste everything below into a new Claude chat (in the "learning helper" project, so the template is available), together with the book file and title. It is the same procedure as the `/quiz-book` skill.

---

# quiz-book: a quiz website for any book

Invoked as `/quiz-book`. The user gives a book name and a book file
(PDF or EPUB). You build a complete project folder: the Recall Quiz
site (themes, spaced repetition, eight question types) with a new
`questions.json` holding a large question bank for that book, then
deliver it as a zip they can upload to GitHub Pages.

## 0. Inputs: stop until you have both

Required:
1. **Book name** (title; author if known).
2. **Book file**: an attached `.pdf` or `.epub`.

If either is missing, **stop and ask for it. Do nothing else first**:
no extraction, no template, no plan. Ask only for what is missing,
for example "Please attach the book as a PDF or EPUB file" or "What
is the book's title?". A file name alone is not a book name; confirm
it.

Then ask (one AskUserQuestion call, all optional with defaults):
- **Questions per page**: the target density. Offer 6 (recommended),
  4, 8 and Other. State what it means: "About N questions for this
  book" (pages x rate, once you know the page count, see step 3).
- **Labels** if the book is not chapter-based ("Lesson", "Sutra",
  "Section"). Default: Chapter / Topic.

If no one is there to answer (scheduled or unattended run), use
6 per page and the default labels, and say so at the top.

Copyright: the user owns the book; the bank is for their own study.
Questions and explanations paraphrase the book. Quotes are short
(a sentence at most) and exact. Never reproduce long passages. Never
include cover art or the publisher's images.

## Model: use the best one available

Question quality is the whole product, so every question is written
and reviewed by the most capable model available.
- When you hand work to subagents (Agent tool), set `model` to the
  strongest option it offers. At the time of writing that is
  `"fable"`; if that is not offered, is refused, or fails (for
  example "out of usage credits"), use `"opus"` and tell the user
  once which model wrote the bank. Never use a smaller or faster
  model to write or review questions.
- Mechanical steps (unpacking, scripts, zipping) need no subagent.

## 1. Get the template

The site template (everything except the book's questions) lives in
the user's "learning helper" project as one text bundle:
`claude/quiz-template/recall-quiz-template.txt`.

1. `project_read` it (it is large, so it comes back as a local file).
   If the user attached a quiz-site `.zip` instead, unzip that and
   skip to step 3 of this list.
2. Unpack it into `<book-id>-quiz/`:

   ```python
   import re, sys
   from pathlib import Path
   bundle = Path(sys.argv[1]).read_text()
   target = Path(sys.argv[2])
   for path, body in re.findall(
           r"^@@@ FILE (.+?) @@@\n(.*?)(?=^@@@ (?:FILE|END) )",
           bundle, re.S | re.M):
       out = target / path
       out.parent.mkdir(parents=True, exist_ok=True)
       out.write_text(body[:-1])  # drop the separator newline
   ```

3. `cd <book-id>-quiz && python3 tools/build_themes.py` (rebuilds the
   generated `css/themes.css` and `js/themes-list.js`).
4. Read `AGENTS.md` and `ai-context/data-formats.md` once.

`<book-id>`: lower-case title with hyphens, e.g. `the-gita`. It also
names the reader's saved progress, so it must differ between books.

## 2. Extract the text

```bash
python3 tools/extract_book.py BOOK_FILE work/extract
```

This writes `work/extract/parts/*.txt` (one per EPUB file or PDF
page, headings marked `## `), `book-outline.json` (TOC, headings,
words and pages per part) and `book-text.txt`.

- If it warns the PDF looks scanned, stop and tell the user: the text
  needs OCR first (offer to run it if `ocrmypdf` or `tesseract` can be
  installed).
- Keep `work/` outside the site folder; it is not published.

## 3. Map the chapters (`work/chapters.json`)

Read `book-outline.json` and the table of contents, then skim each
candidate chapter. Write `work/chapters.json` (format in the docstring
of `tools/plan_question_bank.py`):

- **Include**: every chapter, plus Introduction / Preface / Prologue
  and Conclusion / Epilogue when they carry the author's argument.
- **Exclude** by default: cover, title, copyright, dedication,
  contents, notes, index, bibliography, acknowledgements, "about the
  author", reprinted papers and other appendices that repeat earlier
  material. List what you excluded in the final message.
- `unit`: "Chapter 9", "Introduction" (consistent wording; the chapter
  picker is built from these). `unitTitle`: exact chapter title.
- `pages`: PDF: the chapter's real page range (count from where the
  chapter starts to where the next starts). EPUB: `estimatedPages`
  from the outline (words / 300). Sum several parts if a chapter is
  split across files.
- `sections`: the chapter's sub-headings, exact words, in order (title
  case if the book prints them in capitals).
- `weight` (0.7 to 1.3) from your skim: 1.3 for dense chapters
  (definitions, models, multi-step arguments, many studies), 1.0 for
  typical ones, 0.7 for light ones (mostly stories, recaps, quotes,
  pictures). Weights move questions between chapters; the total
  stays pages x rate.
- `typeWeights` where content suits a type: `{"order": 1.5}` for
  processes, sequences or history; `{"match": 1.5}` for many terms or
  people; `{"sort": 1.5}` for chapters built on a two-way contrast;
  `0.5` where a type would be forced.
- Add `"sourceParts": ["0017.txt", ...]` so writers know which text
  files to read (or `"pages": [first, last]` notes for PDFs).

## 4. Plan

```bash
python3 tools/plan_question_bank.py work/chapters.json --per-page RATE
```

It writes `work/question-plan.json`: questions per chapter (pages x
weight, at least 8 each) and per type (default mix: mcq 25%, recall
17%, fill 15%, multi 10%, tf 10%, order 8%, match 8%, sort 7%,
adjusted by `typeWeights`). Tell the user the total and a one-line
summary (largest and smallest chapters), then continue.

Also tell them what it costs: each chapter writer takes about 4
minutes and about 100k tokens (measured on a 55-question chapter), so
a 40-chapter book is roughly 40 to 60 minutes with 5 writers at a
time, and uses a large share of their plan's usage. For a very large
bank on a limited plan, offer to do it in rounds (one Part at a time).

## 5. Write the questions, chapter by chapter

One writer per chapter, in parallel batches (about 5 at a time), each
a subagent on the best model (see "Model"). Give each writer:
- the brief below, pasted in full;
- its plan entry (unit, unitTitle, idPrefix, sections, questionCount,
  types) and the plan file path;
- the paths of its chapter text files, `work/extract/book-text.txt`,
  and its output path `work/questions/<idPrefix>.json`;
- the book's table of contents (for "place in the argument" questions).

A chapter needing more than about 120 questions can be split between
two writers by sections; give the second writer ids starting at the
next hundred (`c05-101` on) so ids never collide.

When a writer returns, its file must pass
`python3 tools/merge_question_bank.py work/question-plan.json --only
<idPrefix> --book-text work/extract/book-text.txt` with no errors.

### Chapter writer brief (paste in full)

You are writing quiz questions for one chapter of a book, for a
reader who wants to understand and remember the author's argument.
Read the whole chapter text first. Then write exactly the planned
number of questions of each type, save them as a JSON list to the
output path, and run the `--only` check until it shows no errors and
no avoidable warnings.

Coverage
- Cover every section in proportion to its length: each key idea,
  defined term, study or example, and the author's conclusion.
- About 1 in 12 questions is about structure, with `section` set to
  "Place in the argument": why this chapter is where it is, what its
  title signals, the order of its sections, how it links to earlier
  and later chapters (use the table of contents you were given).
- Mix depth: about 40% remember (terms, findings, who/what), 40%
  understand (why, how, what follows), 20% apply (a short new
  everyday scenario the author's idea explains).
- Everything must be answerable from this book. No outside facts,
  later research or criticism.

Every question
- Tests one idea, stands alone (never "as above" or "in this
  section"), and names its subject ("In the Linda problem, ...").
- One unambiguous right answer according to the book. No trick
  wording, no double negatives, no "all/none of the above".
- Plain text only: no HTML, no markdown.
- Common fields: `id` (`<idPrefix>-1`, `-2`, ... in order), `unit`
  and `unitTitle` exactly as in the plan, `section` (one of the
  plan's sections, "Opening" for text before the first sub-heading,
  or "Place in the argument"), `kind`, `q`, `explain`.
- `explain` (all types except recall): 1 to 3 sentences saying why
  the answer is right and, where useful, why the tempting wrong
  answer is wrong. At most one short exact quote (under 25 words) in
  curly quotes “...”, copied character for character from the text
  file, never from memory. Paraphrase everything else. Refer to a
  wrong answer by its idea ("the idea that experts are immune"), never
  by position ("the first option").

Types (exact fields)
- `mcq`: `options` 4 strings, `answer` index from 0. Wrong options
  are plausible: common misreadings, nearby ideas from the same book.
  All options similar in length and grammar. Spread the right
  answer's position evenly across 0 to 3.
- `tf`: `q` starts "True or false: "; `answer` true or false. About
  half false; a false statement changes one meaningful detail of a
  real claim (the direction of an effect, who did what, a condition).
- `multi`: `q` starts "Which of these ..."; `options` 4 to 6;
  `answers` 2 or 3 indexes; at least one wrong option.
- `fill`: `q` contains one blank written `____`; `accept` lists the
  answer (1 to 3 words, the author's key term) first, then other
  wordings the author uses or obvious variants (singular/plural,
  hyphenated). Case, punctuation, "a/an/the" and small typos are
  already forgiven.
- `order`: `items` 3 to 6 short distinct strings in the correct order
  (steps of an experiment, the argument's sequence, chronology, the
  chapter's sections). `q` says what the order is.
- `match`: `pairs` 3 to 5 `[left, right]`, both sides distinct;
  right sides under about 100 characters (term to meaning, person to
  finding, example to idea).
- `sort`: `groups` exactly 2 names; `items` 4 to 8 `{"t": text,
  "g": 0 or 1}`, both groups used (for example System 1 vs System 2,
  gains vs losses).
- `recall`: an open question needing an explanation; `a` is the model
  answer in 2 to 4 sentences, in the author's terms, with at most one
  short exact quote. No `explain`.

Example (shape only):
`{"id": "c09-3", "unit": "Chapter 9", "unitTitle": "Answering an
Easier Question", "section": "The Mood Heuristic for Happiness",
"kind": "tf", "q": "True or false: ...", "answer": false, "explain":
"..."}`

Before saving, reread each question as a careful reader: is the right
answer clearly right in the book, and every wrong option clearly
wrong? Reply with the count per type and any section you could not
cover well.

## 6. Merge and check

```bash
python3 tools/merge_question_bank.py work/question-plan.json \
    --book-text work/extract/book-text.txt --output questions.json
```

Run from inside the site folder (paths adjusted). It stops on errors
and lists warnings in `work/question-bank-report.md`. Fix every error
and every "quote not found" warning (correct the quote from the text
or turn it into paraphrase). Resolve near-duplicates and lopsided
answer positions. Counts within the tolerance shown are fine.

## 7. Independent review

A separate subagent on the best model, which did not write the
questions, checks a random sample (about 3% of the bank, at least 40
questions, every chapter and type represented) against the chapter
text: right answer correct per the book, wrong options really wrong,
not ambiguous, explanation accurate, quote exact. If it finds
problems, fix them and look for the same pattern in the rest of that
chapter (send the chapter back to a writer with the findings if
needed), then merge again.

## 8. Finish the site

1. `questions.json` has `id` (= book-id), `book` (the title) and
   `labels` if set. The page title comes from `book`.
2. Run `python3 tests/run_tests.py`. All checks must pass (the browser
   part samples a few questions of each type; every question is
   checked for fields).
3. Open the page once (Playwright screenshot of the home screen, a
   question, the chapter picker) and look at it.
4. Delete `work/` from inside the site if it got there, and any
   `__pycache__`.

## 9. Deliver

Zip the folder as `<book-id>-quiz.zip` and send it with SendUserFile.
Reply briefly:
- total questions, the mix by type, chapters covered, and what was
  excluded (notes, index, ...);
- how to publish: create a GitHub repository, upload the folder's
  contents (not the folder itself), Settings → Pages → deploy from the
  main branch; or open `index.html` from the folder;
- that progress is saved per book, so several book quizzes can live
  on the same site domain without mixing.
Also attach `question-bank-report.md` only if there were warnings
worth reading. Do not recap the steps.

## Later changes

- **More questions or a new chapter**: plan with the new rate or
  chapters, write only the missing questions with new ids continuing
  each chapter's numbering, merge again. Never renumber existing ids
  (saved progress is keyed by them).
- **Fix a question**: edit it in `questions.json` keeping its id.
- **Updating the template**: when the quiz site itself changes, run
  `python3 tools/pack_template.py pack recall-quiz-template.txt` in
  the latest site folder (it leaves out the book and generated files)
  and `project_write` the result (with `local_path`) to
  `claude/quiz-template/recall-quiz-template.txt`.
