# Kinetic Atlas brand

Kinetic Atlas is a personal exposure lab. It models alcohol, caffeine and nicotine in the body over time and draws them on one live timeline. It is for education, not medical use.

The look is a night instrument panel. Ink-navy grounds, three luminous signal colours, heavy tight numerals, soft big corners. It is modern and slightly aggressive in its type and contrast, and warm underneath: peach and mint hues, plain human sentences, and safety guidance that never scolds.

## Using this folder

This folder is the branding and style core of the Kinetic Atlas web app: how it looks, sounds and draws its charts. It holds stable reference, not app code. Today `index.html` copies its values; the planned web app should use them directly. Read it before you change any UI, add a screen, make an export, or build the planned web app.

To check a change, regenerate `tokens.css` if tokens moved, then open `gallery.html` and look at every component.

| File | What it is | Who it's for |
| --- | --- | --- |
| `README.md` | This brand book: personality, voice, colour, type, layout, motion, icons, accessibility | Everyone, first |
| `tokens.json` | Source of truth for every colour, text style, spacing step, radius, shadow and breakpoint, each with a usage note | Agents and tools |
| `tokens.css` | The same tokens as CSS custom properties. Generated: run `python3 docs/brand/build_tokens_css.py` after editing `tokens.json` | Code |
| `components.css` | Component styles using the app's class names, built only on `tokens.css` variables | Code |
| `components.md` | When and how to use each component | Everyone |
| `charts.md` | Canvas drawing rules for the timeline | Anyone touching `renderChart` or exports |
| `gallery.html` | Every component rendered live. Open it in a browser | Humans |
| `logos/` | The brandmark as SVG | Everyone |

**Rules for changes**

- Change a value in `tokens.json` first, regenerate `tokens.css`, then update the app. Never add a new raw colour to the app without adding it here.
- `index.html` does not load these files yet; it carries its own copy of the values in its `:root` block and canvas code. When you change a token the app uses, change it in both places in the same commit. Token names match the app's CSS variables where one exists (`--bg`, `--primary`, `--alc`, ...).
- The planned web app should load `tokens.css` and `components.css` directly instead of copying values.
- A hosted, browsable copy lives in the Kinetic Atlas Design System artifact (https://claude.ai/artifact/H2osk36of2RTuzyq5ivKAP, private to its owner). This folder is the version-controlled source; if the two differ, this folder wins.

## Personality

| Trait | How it shows |
| --- | --- |
| Futuristic, near-neon | Pastel signal hues (`alc`, `caf`, `nic`, `primary`) at high luminance on `bg`. Each glows: the compound dot carries `box-shadow: 0 0 13px <hue>`, metric cards have a blurred halo of their hue at 9% opacity. |
| Dark and captivating | One theme, Night. Two ambient glows (`glow-teal`, `glow-violet`) bleed in from the top corners of the page. Cards are lit from the top-left with a gradient from `surface-raised` to `surface`. |
| Slightly aggressive | Display weights 800 to 850 with tracking down to -0.055em. Numbers are big, tabular and white. Contrast between `text` and `bg` is 17:1. |
| Warm at heart | The alcohol hue is peach, the brand hue is mint, corners are 21px. Copy is plain UK English that explains rather than warns. |

## Voice and content

- Write in UK English with `en-GB` day-first dates (`23 Nov`, `23/11/2026`). Times follow the clock set in Profile: 24-hour by default (`21:40`), or 12-hour (`9:40 pm`). Use UK units and services: units of alcohol, mg, % BAC, NHS 111, 999.
- Speak to the person as "you"; the app does not say "I" or "we" in the interface.
- Sentence case everywhere: "Log intake", "Add to timeline", "Model, evidence & limitations". Never title case, never all caps except `micro` labels.
- Lead buttons with a verb: "Log intake", "Export CSV", "Clear all". Icon first when there is one: plus before "Log intake", download before "Export JSON", undo before "Undo".
- Say what the model is and is not, plainly: "Each preset is an editable starting point, not a laboratory value." "The alcohol distribution coefficient r is a coarse proxy for body water, not a biological sex test."
- Name uncertainty, never hide it. Every estimate has a band; copy refers to it ("Band: r ±0.06 and clearance range").
- Safety copy is direct and calm: "In an emergency, call 999. If someone is unconscious, breathing abnormally, having a seizure, or you suspect alcohol poisoning, call 999 immediately."
- No exclamation marks, no emoji as decoration, no moralising ("you should cut down"). Guidance states the fact and the threshold.
- Empty states say what to do next: "Nothing logged yet. Use the Log button above to add a drink, coffee or nicotine product and see it on the timeline."

## Colour

**Grounds, darkest to lightest:** `bg` (page) → `track` / `well` (recessed) → `surface` / `surface-inset` (cards) → `surface-raised` (lit edge) → `control` → `tab-active` → `pill-active`. Panels and metric cards are always `linear-gradient(155deg, surface-raised, surface)`, never a flat fill. The page is always `bg` with `glow-teal` and `glow-violet` radial ellipses on top.

**Text:** `text` for values and headings, `soft` for paragraphs and labels, `muted` for metadata and units. All three pass AA on every ground; `muted` is not used on `tab-active` or `pill-active`.

**Brand:** `primary` (mint) is the only brand hue. Use it for the primary action, links, focus and positive emphasis. Text on it is `on-primary`, never white or black. One primary button per view.

**Compounds:** each substance owns one hue, everywhere it appears (curve, dot, tab underline, metric halo, history tile):

- `alc` peach for alcohol, glass icon
- `caf` lavender for caffeine, steaming cup icon
- `nic` aqua for nicotine, leaf icon

Never swap them, never use them for anything else, and never use them for state. Compound hues differ in hue and lightness, but always pair them with a label or icon as well. The Combined view marks itself with a three-stop gradient bar `alc → caf → nic`; that is the only gradient made from them.

**State:** `warn` (caution) and `danger` (urgent) are for severity only. Status surfaces come in ink / bg / border triplets: `success-*`, `badge-*`, `warn-*`, `urgent-*`, `danger-*`, `notice-*`, `alert-*`, `live-*`. Always use the full triplet; never put `warn` text on `urgent-bg`. Severity is always also written as a word (`micro` label: CAUTION, URGENT).

## Typography

- One working family: Inter, falling back to the system UI stack (`--font-sans`). The offline single-file app makes no network requests, so it shows the system face unless Inter is installed. The web app should self-host Inter as a variable font (weights 400 to 900).
- Display styles (`intro-title`, `metric-value`, `dialog-title`, `insight-value`, `panel-title`, `brandname`, `section-title`, `stat-value`) are 700 to 850 with negative tracking. They carry the edge of the brand; body text stays 400.
- Body is `body` at 14px / 1.55. Most interface copy is `small` (12px) or `caption` (11px). Nothing in running text is set larger than 14px.
- Every number that updates or lines up uses `font-variant-numeric: tabular-nums`.
- One accent: `accent-word`, a curly serif italic (`--font-accent`: Hoefler Text, then Palatino Linotype, Palatino, Georgia). It sets the three compound names in the intro headline, each in its own hue, at weight 400 against the heavy sans around it. That contrast is the warmth showing through the instrument panel, and it only works if it stays rare: one headline per page, compound names only, never body text, labels, numbers or buttons. The stack is system faces, so the offline app still loads nothing; never use the generic `cursive` (it is Comic Sans on Windows).
- `micro` is the only uppercase style: 10px, weight 800, tracking 0.11em, used for severity and kicker labels.
- Formulas use `code` in `--font-mono`, `code-ink` on `track`.

## Space, radius and layout

- Spacing steps are hand-tuned: `space-3` 11px between cards, `space-4` 13px between metric cards, `space-5` 17px between panels, `space-6` 22px inside panels, `space-8` 36px page gutter. Do not snap them to an 8px grid.
- Radii nest: `radius` 21px on panels and dialogs, `radius-brand` 14px and `radius-card` 12px for cards inside, `radius-control` 11px for buttons, `radius-input` 10px for fields, `radius-xs` 7px for pills inside tracks. An inner element always has a smaller radius than its container.
- Desktop layout: a 1.84 : 1 two-column dashboard inside a 1510px shell (`shell-max`), the timeline across the top, history on the right. Below `bp-md` (900px) it becomes one column with history directly under the chart. Below `bp-sm` (680px) metric cards compact to value only and lose their glow.

## Composition

The page should look drawn on one grid, not assembled from parts. Hold every new or changed element to these:

- **Every edge lands on a line that already exists.** The lines are the shell's two edges, the three equal metric columns (`space-4` gap) and the dashboard's two columns (1.84 : 1, `space-5` gap). A block starts and ends on one of them. Never give a block a free-standing `max-width` that stops it in open space.
- **Text wraps because it reached a shared edge.** If a line breaks while there is empty page beside it, the layout is wrong. Either the block fills its container, or a sibling fills the rest of the row.
- **Side-by-side blocks share a line.** Align their tops or their bottoms, on purpose. Metric cards and panels in a row share a top.
- **Headlines wrap balanced** (`text-wrap: balance`). No single word left on a last line.
- **The page is left-aligned.** Don't centre a block to deal with leftover space; put the space to work or remove it.
- **Empty space is a decision.** Gaps between elements are spacing tokens. Any larger void needs a reason you can state.
- **One of each.** One headline, one primary button per view, one accent face, one hue per compound. Before adding a new pattern, reuse a component from `components.md`; if nothing fits, add the new one there, in `components.css` and in `gallery.html` in the same commit.
- **Look before you commit.** Screenshot the page at 1600, 1280, 1000 and 500px wide (command in `CLAUDE.md`) and check each against this list. A layout that only works at one width is not finished.

## Depth, glow and motion

- Depth comes from the lit gradient, the ambient glows and soft halos, not from hard shadows. `shadow-panel` is almost invisible on purpose. Only floating things (`shadow`, `shadow-dialog`) cast a real shadow.
- Glow is reserved for signals: the compound dot (`0 0 13px` of its hue), the metric halo (210px disc, 35px blur, 9% opacity) and the brandmark (`shadow-brand`). Never put glow on text or on buttons.
- Motion is short and functional: 0.15s ease on controls, 0.2s on the toast, 0.3s on meter widths, 0.32s rise-in on the guidance section. No looping animation. Under `prefers-reduced-motion`, transitions and animations are off.
- Dialogs sit on `backdrop` with a 7px backdrop blur.

## Interaction states

- Focus: `outline: 2px solid var(--primary); outline-offset: 3px` on every focusable element. Primary on `control` is 10:1.
- Hover: default buttons go to `control-hover` with `border-hover`; primary goes to `primary-hover`; outline buttons fill with `primary-tint`.
- Disabled: 45% opacity, `not-allowed` cursor.
- Selected tab: `tab-active` fill plus a 2px inset underline in the compound's hue. Selected pill: `pill-active` with `shadow-pill`.

## Iconography and the mark

- The brandmark is a pulse trace (a flat line, a sharp rise, a deep fall, a recovery) drawn in `brand-ink` on a 43px `brand-tile` square with `radius-brand` corners and the `shadow-brand` halo. Pair it with "Kinetic Atlas" in `brandname`, `space-4` apart. Files are in [`logos/`](logos/): `ka-mark.svg` is the tile exactly as the app ships it; `ka-trace.svg` is the trace alone recoloured to `primary` for dark grounds (a derived variant, not used in the app).
- Interface icons are line drawings in one inline, hidden SVG sprite at the top of the page: `<symbol id="i-…" viewBox="0 0 24 24">`, used as `<svg class="ic" aria-hidden="true"><use href="#i-name"/></svg>` (in the app's JS, `ic(name)`). No icon font, no external file, no network. The set: plus (add, Log intake), download (export), upload (import), undo, close (dialogs only), user (profile), edit, copy (duplicate), delete (a bin), check (done), spark (empty state), up, refresh. Compound icons: glass (alcohol), steaming cup (caffeine), leaf (nicotine), each in its hue on its `*-tint` tile.
- `.ic` sets them at 1.25em in `currentColor`, no fill, stroke-width 2.2 on the 24 grid with round caps and joins: the same proportional weight as the trace's 2.4 on its 26 grid.
- Any new icon is a `<symbol>` in that sprite, drawn on the 24 grid in strokes only, so `.ic` styles it like the rest. Icon-only buttons keep an `aria-label`; the SVG itself is always `aria-hidden`.

## Charts

The timeline is the product. Drawing rules are in [`charts.md`](charts.md).

## Accessibility

- Text pairs meet WCAG AA on the grounds named in each token's usage note.
- Known gaps kept from the source: `border`, `border2` and `input-border` are under 3:1 against their grounds. Fields remain identifiable by their `well` fill and label, but the web-app rebuild should lift `input-border` to at least `#5d7085` (`border-hover`).
- Never rely on colour alone: compounds have names and icons, severities have words.
- The app includes `.sr-only` text and `aria-live` regions; keep them when restyling.
