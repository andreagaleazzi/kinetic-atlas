# Charts

The timeline chart is drawn by hand on `<canvas>`. It scales for high-density screens and uses no chart library. These rules come from `renderChart` and keep every plot, export and future chart in the same language.

## Canvas

- The canvas is transparent, so the panel gradient shows through.
- Horizontal gridlines: `chart-grid` (#283747), 1px, five steps from 0 to the max.
- Vertical gridlines: #29394b each tick, #3b5068 at midnight, so day boundaries read a step brighter.
- Y-axis labels: 11px system UI in `muted`. Time labels #889ab0, date labels #b3c1d3 beneath them.
- Cursor: crosshair over the plot.

## A compound series

Three layers, drawn in this order, all in the compound's hue (`alc`, `caf` or `nic`):

1. **Uncertainty band:** filled from `low` to `high` at hex alpha `25` (about 15%). Alcohol's band comes from r ±0.06 and the clearance range. Caffeine and nicotine use half-life ×0.7 and ×1.5. Always draw the band. Never show a line without its range.
2. **Area glow:** filled under the central line with a vertical gradient from alpha `33` at the top to `04` at the baseline. This is the neon wash.
3. **Central estimate:** a 2.8px line with round joins.

Doses are not drawn inside the plot; they are marked under the x-axis (see below).

## Secondary curve

A second quantity for the same compound, on its own axis. Today it is only the Nicotine tab's optional blood level (ng/mL); it is off by default.

- Drawn after the compound series, in the same hue, so it reads as the same compound in another unit.
- **Band:** `low` to `high` at hex alpha `12`, half the main band, so both bands stay readable where they overlap.
- **Line:** dotted `[2,4]`, 2px. No area glow: the glow belongs to the main series.
- **Axis:** right-hand labels in the compound hue at alpha `b3`, 11px, on the same five gridlines (three labels, 0, half and max, below 500px). The right padding grows from 12 to 44px only while the curve is shown.
- No reference lines on a secondary axis: they would read as targets.
- Legend: an 18×2px dotted swatch (`i.dotted`), shown only while the curve is. The unit label names both units. The tooltip adds one line, "Blood ≈ N ng/mL".

## Markers and reference lines

- Now: a dashed `[5,5]` vertical line, 1.2px, `chart-now`, labelled `NOW` at the top in bold 10px.
- Bedtime: the same line in `chart-bedtime`, labelled `BED`.
- Caffeine personal guide: a dashed `[5,5]` horizontal line in #d5b87799, labelled "personal guide" in #dcc68d.
- Alcohol references at 0.05, 0.08 and 0.15 % BAC: dashed `[3,6]` in #e590795e, labelled ".08 reference" in #c39c95.
- Marker labels spread apart so they never overlap.
- Doses: a 7×6px upward triangle in the gutter just under the x-axis baseline, in the compound hue. Doses closer than about 5px share one marker; on the Combined view it has one triangle per compound, abutting. When a marker stands for more doses than it has triangles, a bold 9px count follows in #b3c1d3, the date-label colour.

## Hover

- Crosshair: a dashed `[2,3]` 1px vertical line in #e5eefb88.
- Point: a dot in the compound hue with a 2px #0b1420 ring, so it lifts off the line.
- Tooltip: `tooltip-bg`, `tooltip-border`, `radius-input`, `shadow`. Time in `text` bold, values in `soft`, each prefixed by a 7px dot of its hue.
- Near a dose marker the tooltip adds a dose list under a 1px `tooltip-border` hairline: up to four rows of time, dose and label, each with a 7px dot in its hue, then "+n more".

## Combined view

All three compounds on one plot, on a relative 0–1 or a log-mg axis. Its tab carries the `alc → caf → nic` gradient underline, the only gradient made from compound hues.

## Legend and export

- The legend sits under the plot behind a `border` hairline. It has 18×3px line swatches, an 8px band swatch in `chart-band` / `chart-band-edge`, 2×12px marker swatches in `chart-now` and `chart-bedtime`, and an 8×7px "Dose" triangle in the compound hue (#b3c1d3 on the Combined view). The unit label sits on the right in `muted`.
- The PNG export takes its labels from the legend, unit and plot note in the page, and draws the Dose swatch as the same triangle and the dotted swatch as the same dots. Change them in the same edit as anything the canvas draws.
