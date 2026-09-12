# Heritage → Paragon Token Map

This document separates **Paragon-native overrides** from the Heritage-specific extension layer.

| Heritage decision | Implementation | Notes |
|---|---|---|
| Crimson primary | `color.primary.*` | Base 500 is exact corporate crimson; support ramp is derived for the Paragon scale |
| Crimson brand | `color.brand.*` | Brand mirrors the primary brand color |
| Teal secondary | `color.secondary.*` | Base 500 is exact corporate teal |
| Gold accent | `color.accent.a` | Exact corporate gold |
| White / black | `color.white` / `color.black` | Exact corporate values |
| Stone / Mist | `color.gray.100` / `color.gray.200` | Exact corporate values |
| Jost UI | `typography.font.family.sans.serif` | Paragon-native typography token |
| Cormorant Garamond editorial | `typography.font.family.serif` | Paragon-native typography token |
| Cinzel display | `--heritage-font-display` | Used by heading selectors because Paragon's global schema has no separate display family |
| Content width 1160px | `--heritage-content-max` | Heritage extension token |
| Body max 66ch | `--heritage-body-max` | Heritage extension token |
| 1/2/4/6.5rem spacing | `--heritage-sp-*` | Heritage extension tokens |
| Focus ring | CSS layer | Non-tokenizable selector/interaction requirement |
| Hero fadeUp | CSS layer | Non-tokenizable page-behavior requirement |
| Header blur / sticky | CSS layer | Component-specific behavior not safely represented as a global Paragon token |

## Derived color ramps

The source specification supplies base corporate colors, not complete 100–900 ramps. This implementation derives the supporting shades by blending the exact base color toward white for 100–400 and toward black for 600–900.

That makes the theme operational for Paragon's scale-based color tokens without modifying the supplied corporate base colors. For strict brand governance, replace the generated ramps with approved accessibility-tested brand ramps when a formal palette is available.

## Array token overrides -- read before editing `typography.json`

Paragon's own `typography.font.family.sans.serif` default (and `.monospace`)
are **arrays** of font names, e.g. `["-apple-system", "BlinkMacSystemFont",
"Segoe UI", ..., "Noto Color Emoji"]` (12 items). This matters for two
reasons that were both real, build-verified bugs in this package prior to
v1.0.0's rebuild:

1. **The value must be a JSON array, not a pre-joined string.** An earlier
   version of this file wrote the sans-serif override as a single string
   with embedded escaped quotes (`"Jost, ... \"Segoe UI\", ..."`). Style
   Dictionary's font-family CSS transform expects an array and quotes each
   multi-word item itself; feeding it an already-quoted string produced
   `'"Segoe UI"'` in the compiled CSS -- a font name that matches nothing,
   silently falling back to the next item in the stack.

2. **Style Dictionary/lodash merges array tokens by index, not by full
   replacement.** If your override array is shorter than Paragon's default
   array, the *tail* of Paragon's default array survives at the indices
   your override didn't cover. Concretely: overriding `sans.serif` with a
   6-item array on top of Paragon's 12-item default does NOT produce a
   6-item result -- it produces your first 6 items followed by items 6-11
   of Paragon's *default* array (`Noto Sans, sans-serif, Apple Color Emoji,
   Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji` at the time of
   writing, current values may differ across Paragon versions).

**The fix applied in `paragon/tokens/core/global/typography.json`:** the
`sans.serif` override array is padded to be at least as long as Paragon's
own default array (verified against `@openedx/paragon@23.23.0`), so every
index is explicitly overridden and nothing from the default leaks through.
`monospace` was already long enough by coincidence; `serif` is unaffected
because Paragon's own default for that token is a plain string, not an
array, so a full replacement happens automatically.

**If you ever change these fonts:** rebuild (`npm run build`) and inspect
`dist/core.css` for the compiled `--pgn-typography-font-family-*` values
before shipping -- `make validate` (wired into `npm run build`) also runs a
cheap automated check for this specific regression, but only for the exact
"Apple Color Emoji without Jost" signature described in `Makefile`; it is
not a substitute for reading the actual compiled output after a real change.
