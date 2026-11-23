# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Kinetic Atlas: a personal exposure tracker that models alcohol (BAC %), caffeine (mg) and nicotine (mg) over time from logged intake. It is for education, not medical use, and the UI says so.

**Today** it is one self-contained file, `kinetic_atlas.html` (~100 KB, minified-style long lines). It has no build step, no dependencies and no network calls, and it stores data in `localStorage`.
**Planned:** a proper web app with a backend, a database and user accounts. Keep the current file working until that migration actually starts. Code added now should not block the split described under "Migration direction".

## Commands

- Run: open `kinetic_atlas.html` in a browser, or serve it with `python3 -m http.server 8000` and visit `/kinetic_atlas.html`.
- There is no build, lint or test tooling yet. When you add tests, start with the pharmacokinetic (PK) math (see below). It is pure, and it is the part where a mistake actually matters.
- Lines are thousands of characters long. Find code with `grep -n` or `grep -o` plus `cut -c`, not by reading whole lines.

## Git workflow

- After finishing a coherent chunk of work, **ask the user whether to commit it** instead of leaving it uncommitted. Never commit without their go-ahead.
- Use Conventional Commits: `<type>: <short imperative summary>`, e.g. `feat: add combined timeline tab`, `fix: open Log intake on the viewed compound`, `docs: add icon and time-format items to FIXES.md`. Types: `feat`, `fix`, `docs`, `refactor`, `style`, `test`, `chore`. Add a scope when it helps (`fix(chart): ...`).
- One logical change per commit. Keep code (`kinetic_atlas.html`) and docs (`CLAUDE.md`, `FIXES.md`) in separate commits unless the docs describe that exact code change and must stay in sync.

## Architecture (single file)

Layout: `<head><style>` → markup (`<main id="top">`, plus `<dialog id="profileDialog">` and `<dialog id="scienceDialog">`) → one `<script>` holding a strict-mode IIFE. No globals leak out.

Inside the script, in order:

1. **Constants and presets.** `KEY='kinetic-atlas-offline-v2'` (storage key), `defaults` (profile), and `P`, the drink/product presets. Presets are **positional arrays**, not objects, and the layout differs by type: alcohol and caffeine use `[id, label, volume, abv|mg, group]`, while nicotine adds duration and absorption fields and keeps its group at index 6. `setEntryType` / `assignPreset` / `getFormDose` read them by index, so keep them in sync when you edit presets.
2. **State.** `state = {profile, profileSet, entries[]}`, plus UI vars (`entryType`, `chartType`, `plotScale`, `horizon`, `series`, `historyStack`). `chartType` is a compound or `'all'` (the Combined tab, drawn by `drawCombined` on a relative 0–1 or log-mg axis per `plotScale`), so don't assume it indexes a series. Every mutation goes through `transaction(fn)`, which pushes an undo snapshot (max 10), calls `persist()`, then `renderAll()`.
3. **Trust boundaries.** `validateEntry` and `normalizeProfile` clamp and validate everything loaded from storage or JSON import. Import is capped at 2 MB. These define the de facto data schema, so they become the server-side validation later. Don't loosen them.
4. **PK model** (pure functions):
   - `instantAmount` / `amountFor`: one-compartment model with first-order absorption (`ka`) and elimination (`ke = ln2/half-life`). Intake is spread evenly over `durationMin`.
   - `alcoholScenario`: the absorbed ethanol fraction (`absorbedFrac`) is converted to BAC with Widmark `r`, then reduced at a constant `beta` %/h down to 0.
   - `buildSeries(now)`: a 5-minute grid from −96 h to +72 h. Each point holds a central `v` plus `low` and `high` uncertainty bands. Alcohol bands come from r ±0.06 and the clearance range; caffeine and nicotine bands from half-life ×0.7 and ×1.5.
   - `at`, `peakNext` and `settledTime` interpolate and query `series`.
5. **Rendering.** `renderAll` recomputes `series` and redraws everything: summary, `renderChart` (hand-drawn `<canvas>`, DPR-aware, no chart library), `renderHistory`, `renderLedger`, `renderInterpretation` and `renderProfileSummary`. HTML is built from template strings, so interpolated user text must go through `esc()`. `renderInterpretation` hides `#guideSec` unless a card applies to the current data. A `setInterval` runs `renderAll` every 60 s while the tab is visible.
6. **Wiring.** `addEventListener` calls near the bottom, using delegated clicks (`data-action`, `data-close`). Export/import is `exportJSON` (`{app, version:2, profile, entries}`) and `exportCSV`. `exportPNG` saves the chart as shown; it labels the image from the DOM (`.legend` spans, `#plotUnit`, `#plotNote`), so keep those in sync with what the canvas draws.

Entry shape (also the future DB row): `{id, type: 'alcohol'|'caffeine'|'nicotine', preset, label, time: ISO string, note, qty, durationMin, dose, ka, ...}`, plus type-specific fields: alcohol `units, volume, abv, food`; caffeine `mg, volume`; nicotine `mg, fraction`. IDs are generated on the client.

## Domain constraints

- The model parameters, guidance thresholds (EFSA caffeine limits, UK units) and cited sources are listed in `#scienceDialog`. If you change a formula or default, update that dialog in the same change. The app's stance is that showing the method is part of the feature.
- Locale is UK (`en-GB` formatting, UK units, NHS/999 wording).
- The "Data handling" block in `#scienceDialog` promises "no outbound requests" and local-only storage. Rewrite it as soon as any network or backend behaviour lands.

## Migration direction (backend, DB, users)

- Move the PK model (section 4) out first, into a standalone module with no DOM dependencies, so the browser and the server can share it and it can be unit-tested.
- The existing `exportJSON` format (version 2) is the natural path for importing local data into a new account. Keep it readable by the new system.
- The data is health-related (substance use, pregnancy, medications, liver condition), which counts as special-category personal data under UK GDPR. Plan for per-user authorization on every entry and profile access from the start.
