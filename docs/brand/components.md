# Components

Usage rules for each component. Styles are in `components.css` (load `tokens.css` first). Live examples: open `gallery.html`.

## Brand

The lockup: the pulse-trace brandmark on a mint tile, followed by the name in `brandname`.

- Consumer provides: nothing; use it as-is in the top-left of the top bar, linking to the top of the page.
- The tile is 43px, `radius-brand`, `brand-tile` fill, `shadow-brand` halo. The trace is 26px, 2.4px stroke, round caps, in `brand-ink`.
- Gap between mark and name is `space-4` (13px). The name is "Kinetic Atlas", two words, title case, weight 850.
- The mark may stand alone (favicon, app icon, tight spaces). The name never appears without the mark in the app chrome.
- Don't recolour the tile with a compound hue, outline it, or put the trace on a dark ground without the tile.

## Intro

The page's opening statement, above the Now section: a `micro` kicker, one `intro-title` headline and, always directly below it, one `small` paragraph.

- Layout: one stacked block at every width. Kicker, headline, then the paragraph 10px below, each running from the shell's left edge to its right edge. The paragraph never sits beside the headline. No `max-width` of its own.

- Consumer provides: kicker, headline, paragraph. One per page.
- In the headline, wrap each compound name in `<span class="c-alc">` (or `c-caf`, `c-nic`). Inside `.intro h1` a span becomes `accent-word`: the curly serif italic, weight 400, 1.18em, in the compound's hue.
- Only compound names get the accent, and only here. The word is its own label, so the hue is never the only signal.
- The paragraph tells what the app is for, not how to use it: what happens in the body after intake, what the timeline shows, and that every curve is an estimate. Step-by-step guidance belongs in empty states and dialogs.
- Write it as a neutral statement of fact, like an instrument's caption: name the thing and what it does ("plots the rise, peak and clearance"). No storytelling, metaphor or drama ("isn't over when you finish it", "that hidden part", "the long tail").
- Links in the paragraph are quiet `linkbtn`s: the paragraph's own colour, size and weight, a `muted` underline, `primary` on hover. They open the matching dialog and read as part of the sentence ("everything you log", "your profile"), not as calls to action. The primary button already does that job.
- Don't add a second headline, glow, or a gradient across the three names.

## Button

Buttons are 39px tall (`control-h`), 12px bold labels, `radius-control` corners, a verb first and an icon before the verb when one exists.

- **Primary** (`btn btn-primary`): mint fill, `on-primary` text. The one action the view is for: "Log intake", "Add to timeline", "Save profile". One per view.
- **Default** (`btn`): `control` fill, `border2` outline. Secondary actions: "Cancel", "Export CSV".
- **Ghost** (`btn btn-ghost`): no fill. Toolbar actions next to the primary.
- **Outline** (`btn btn-outline`): mint outline and text. A repeat of the primary action further down the page, e.g. in an empty history.
- **Danger** (`btn btn-danger`): destructive and irreversible only ("Clear all"). Always confirm in the page itself.
- **Small** (`btn-small`): 28px, 11px text, `radius-sm`. Inside panels and dialog headers.
- **Link button** (`linkbtn`): an inline action styled as a link ("How this is calculated").
- Consumer provides: a `<button type="button">` with label text; an `aria-label` when the button shows only an icon (close). Icons are `<svg class="ic" aria-hidden="true">` from the sprite (see Iconography in `README.md`).

## Tag

Tags are pills (`radius-pill`) for a passive fact; status badges are small rounded labels (`radius-xs`) for a judged state.

- `tag`: neutral fact. `tag green`: a positive, completed fact ("Profile set").
- `badge-status`: neutral state. `badge-status warn`: caution. `badge-status urgent`: urgent.
- Each badge uses its full ink / bg / border token triplet. The word always states the state; colour only reinforces it.
- Consumer provides: a short noun phrase in sentence case, two or three words.

## Tabs

Two segmented controls on a `track`: compound tabs switch what the chart shows; pill buttons switch a setting of the view.

- **Compound tabs** (`tabs`): 12px at 780. The selected tab gets `tab-active` and a 2px underline in its compound hue. The Combined tab's underline is the `alc → caf → nic` gradient.
- **Pills** (`pill-btns`): 11px at 750 for range (24 h / 48 h / 72 h) and scale (Relative / Log mg). The selected pill gets `pill-active` and `shadow-pill`.
- Consumer provides: buttons with `active` on the current one, plus `aria-pressed` or a tablist role.
- Below 680px the compound tabs become a 4-column grid.

## Panel

The main container: a lit gradient card with `radius` corners, a `border` hairline and `space-6` padding.

- Background is always `linear-gradient(155deg, surface-raised, surface)`; never a flat fill, never a compound hue.
- Header (`panel-title`): `panel-title` heading with a `caption` subtitle on the left, small actions on the right.
- Panels sit `space-5` apart in the dashboard grid. Don't nest panels; use `statbox`, `insight` or `info-card` inside.

## MetricCard

The live reading for one compound: name with a glowing dot, a big tabular value, its unit, the next peak and a meter.

- Consumer provides: compound (`alcohol`, `caffeine` or `nicotine` class, which sets `--tone`), current value, unit, peak text and the meter percentage.
- Always three cards in a row, in the order alcohol, caffeine, nicotine, `space-4` apart.
- The halo is the compound hue at 9% opacity, blurred 35px, in the top-right corner. It disappears below 680px, along with the footer and meter.
- Values use `metric-value`: 35px, 800, -0.055em, tabular-nums. Alcohol shows 3 decimals, caffeine and nicotine 0 or 1.

## StatBox

Three compact readings under the chart: now, at bedtime and the next peak.

- Consumer provides: a 10px `muted` label, a 17px tabular value and a unit in `small`.
- Always three in a `stats-row`, 9px apart, on `surface-inset` with `radius-control`.
- In the Combined view each box lists one line per compound, each prefixed by a 7px dot in its hue.

## Insight

A tile in the At bedtime panel: a `micro` kicker, one big value in `insight-value`, a line of context and a status badge.

- Consumer provides: kicker text (uppercase via CSS), value, context sentence, badge state.
- Four tiles in a row on desktop, two below 1120px. `radius-brand` corners on `surface-inset`.
- The badge says the judgement in words; the value stays `text` white whatever the state.

## InfoCard

A guidance card: severity word, a one-line headline and one or two sentences of fact.

- Severity sets the stripe and label colour: none (`border2`), `caution` (`warn`), `urgent` (`danger` on `urgent-surface`).
- Consumer provides: severity, headline (12px bold) and body (11px `soft`).
- Show a card only when it applies to the current data; the Guidance section is hidden when none do.
- Write facts and thresholds with their source (EFSA, UK CMO). Never moralise. Urgent cards always name the action (call 999).
- The coloured left stripe is a source pattern; keep it for guidance cards only.

## LogItem

One logged intake in the History list: compound icon tile, label and time, dose, and edit / duplicate / delete actions.

- Consumer provides: compound class, preset label, time and note, dose and secondary dose.
- The icon tile is 35px, `radius-control`, icon in the compound hue on its `*-tint`: glass for alcohol, steaming cup for caffeine, leaf for nicotine.
- Actions are 15px icon buttons in `muted`: edit (pencil), duplicate (copy), delete (bin). Each has an `aria-label` naming the action and the entry.
- Rows are separated by `border` hairlines, not boxed. Long labels truncate with an ellipsis and keep a `title`. The dose wraps within 96px.
- Dates are `en-GB`, day first; times follow the Profile clock (24-hour or 12-hour). User text always goes through `esc()`.

## Field

Label, control and hint, laid out in a two-column `formgrid` with `space-3` gaps, fields aligned to the bottom so controls line up; `full` spans both columns.

- Labels use `field-label` (11px, 760, `soft`) above the control. Every control has a `<label for>`.
- Inputs and selects share one height, 44px, with `well` fill, `input-border` outline, `radius-input`. Focus adds a mint border and a soft 3px halo.
- Date and time are plain text fields, not native pickers: date as dd/mm/yyyy, time on the Profile clock (`21:40` or `9:40 pm`).
- Hints use 10px `muted` under the control. Say what the value means, not how to type it.
- `live-preview` shows the derived result while the person types, in the translucent green `live-*` triplet.
- `feedback` confirms the action in `feedback` green, in the past tense ("Added to timeline.").

## ChartLegend

The legend under the timeline and the tooltip that follows the cursor. Drawing rules for the canvas itself are in the Charts section.

- Legend swatches: an 18×3px line in the compound hue, an 8px band swatch, 2×12px marker lines for now and bedtime, and an 8×7px "Dose" triangle (`i.dose`). The unit sits on the right in `muted`.
- Tooltip: `tooltip-bg`, `tooltip-border`, `shadow`. The time line is bold `text`; each value line starts with a 7px dot in its hue. Near a dose marker it adds a dose list (`tip-doses`) under a `tooltip-border` hairline, one row per dose with a 7px dot in its hue.
- Keep the legend text in step with the canvas: PNG export reads it.

## EmptyState

What a list shows before it has data: a 28px spark icon, a short bold line and one sentence saying what to do next.

- Dashed `#405168` outline on `well`, `radius-card`. Text centred.
- Consumer provides: headline ("Nothing logged yet") and the next step, naming the exact control.

## Notice

One inline message. `notice` reports a problem with the app or data. Emergency guidance (999, then NHS 111) is a sentence in the footer disclaimer, not a component.

- `notice`: `notice-*` triplet, `radius-input`, `role="alert"`. Say what went wrong and what to do ("Export your data before closing this page.").
- Not dismissible.

## Toast

A brief confirmation at the bottom centre of the screen after an action that has no visible result in place.

- `control` fill, `border2`, `radius-card`, `shadow`. 12px text. Slides up 16px and fades in over 0.2s.
- Consumer provides: one past-tense sentence with the count where there is one ("Imported 14 entries.").
- Use `role="status"`. Don't use a toast for errors; use a `notice`.

## Dialog

A native `<dialog>` for Log intake, Profile and the science notes: head, scrolling body, footer.

- 760px wide (560px for narrow dialogs), `radius` corners, `dialog-border`, `surface-inset`, `shadow-dialog`, over `backdrop` with a 7px blur.
- Head: `dialog-title` plus one `soft` sentence, small close button (close icon, `aria-label`) on the right.
- Footer: secondary info or actions on the left, the primary on the right.
- Consumer provides: title, intro sentence, body content, actions. Close with `data-close`.
