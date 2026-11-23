# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository. It routes; the detail lives in the files it points to.

## What this is

Kinetic Atlas: a personal exposure tracker that models alcohol (BAC %), caffeine (mg) and nicotine (mg) over time from logged intake. It is for education, not medical use, and the UI says so.

**Today** it is one self-contained file, `index.html` (~130 KB, minified-style long lines): no build step, no dependencies, no network calls, data in `localStorage`.
**Planned:** a web app with a backend, a database and user accounts. Keep the current file working until that migration starts, and don't block it (see below).

## Where to go

| Task | Read first |
|---|---|
| Find or understand code in `index.html` | `docs/architecture.md` |
| Change anything (what else must move in the same commit) | `docs/change-impact.md` |
| UI, copy, chart or export look | `brand/README.md` (tokens: `brand/tokens.json`) |
| Pick up or ship a fix | `docs/FIXES.md` (backlog), `docs/FIXES_ARCHIVE.md` (shipped) |
| Public overview | `README.md` |

## Commands

- Run: open `index.html` in a browser, or `python3 -m http.server 8000` and visit `/`.
- Tokens: after editing `brand/tokens.json`, run `python3 brand/build_tokens_css.py`.
- No build, lint or test tooling yet. When adding tests, start with the PK math: it is pure, and it is where a mistake matters.
- Lines are thousands of characters long. Find code with `grep -n` or `grep -o` plus `cut -c`, not by reading whole lines.

## Git workflow

- After a coherent chunk of work, **ask the user whether to commit it**. Never commit without their go-ahead.
- Conventional Commits: `<type>: <short imperative summary>`, e.g. `feat: add combined timeline tab`, `fix(chart): ...`. Types: `feat`, `fix`, `docs`, `refactor`, `style`, `test`, `chore`.
- One logical change per commit. Keep code (`index.html`) and docs (`CLAUDE.md`, `README.md`, `docs/`) in separate commits unless the docs describe that exact code change.

## Migration direction (backend, DB, users)

- Move the PK model out first, into a standalone module with no DOM dependencies, shared by browser and server and unit-tested.
- `exportJSON` (version 2) is the import path into a new account. Keep it readable.
- The data is health-related (special-category personal data under UK GDPR). Plan per-user authorization on every entry and profile access from the start.
