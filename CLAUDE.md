# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. It routes; the detail lives in the files it points to.

## What this is

Kinetic Atlas: a personal substance tracker that models alcohol (BAC %), caffeine (mg) and nicotine (mg) over time from logged intake. It is for education, not medical use, and the UI says so.

**Today** it is one self-contained file, `index.html` (~130 KB, minified-style long lines): no build step, no dependencies, no network calls, data in `localStorage`.
**Planned:** a web app with a backend, a database and user accounts. Keep the current file working until that migration starts, and don't block it (see below).

## Where to go

| Task | Read first |
|---|---|
| Find or understand code in `index.html` | `docs/architecture.md` |
| Change anything (what else must move in the same commit) | `docs/change-impact.md` |
| UI, copy, chart or export look (branding and style core) | `docs/brand/README.md` (tokens: `docs/brand/tokens.json`) |
| Add or restyle any visible element | `docs/brand/README.md`, "Composition": the alignment and polish rules every element must meet |
| Pick up or ship a fix | `docs/FIXES.md` (backlog), `docs/FIXES_ARCHIVE.md` (shipped) |
| Public overview | `README.md` |

## Commands

- Run: open `index.html` in a browser, or `python3 -m http.server 8000` and visit `/`.
- Tokens: after editing `docs/brand/tokens.json`, run `python3 docs/brand/build_tokens_css.py`.
- Check a UI change by eye before committing it: screenshot at each width, then read the images. Every edge should land on the page grid and no text should wrap beside empty space ("Composition" in `docs/brand/README.md`).
  `for w in 1600 1280 1000 500; do "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=$w,900 --screenshot=/tmp/ka-$w.png "file://$PWD/index.html"; done`
- Test: `node tests/pk.test.js` checks the nicotine blood curve against a step-by-step simulation. It is the only test; there is no build or lint tooling. When adding tests, stay with the PK math first: it is pure, and it is where a mistake matters.
- Lines are thousands of characters long. Find code with `grep -n` or `grep -o` plus `cut -c`, not by reading whole lines.

## Git workflow

- After a coherent chunk of work, **commit it without asking**, then tell the user what was committed. Pushing still needs their go-ahead.
- Conventional Commits: `<type>: <short imperative summary>`, e.g. `feat: add combined timeline tab`, `fix(chart): ...`. Types: `feat`, `fix`, `docs`, `refactor`, `style`, `test`, `chore`.
- One logical change per commit. Keep code (`index.html`) and docs (`CLAUDE.md`, `README.md`, `docs/`) in separate commits unless the docs describe that exact code change.

## Migration direction (backend, DB, users)

- Move the PK model out first, into a standalone module with no DOM dependencies, shared by browser and server and unit-tested.
- `exportJSON` (version 2) is the import path into a new account. Keep it readable.
- The data is health-related (special-category personal data under UK GDPR). Plan per-user authorization on every entry and profile access from the start.
