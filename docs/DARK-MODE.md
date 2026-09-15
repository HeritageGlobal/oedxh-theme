# Dark mode

## What's build-verified vs. documented-only

**Build-verified** (compiled and inspected in this repository's own CI-style
build, same rigor as the light theme): the CSS layer described below in
"Automatic (no setup required)". It ships inside `dist/core.min.css` --
nothing extra to install or configure.

**Documented, not build-verified**: the optional manual toggle script in
"Manual toggle (optional, advanced)" below. There is no live edx-platform or
MFE image build available in this repository's build environment to test
script injection and DOM behavior against, the way the CSS layer was tested.
Test it on a staging instance before shipping to production.

## Why this isn't a second Paragon-built theme

Paragon 23.23.0 ships only a "light" reference theme. Attempting to build a
real second theme variant (`paragon build-tokens --themes light,dark`) was
tried in the course of developing this package and fails outright --
Paragon's own component token files (`Badge.json`, `Alert.json`, etc.)
reference alias/action tokens that only exist under its bundled `light`
theme, so a `dark` theme folder containing just color overrides doesn't have
enough of Paragon's own internal wiring to resolve, and the build crashes.
Fully replicating that wiring for a second theme would mean re-authoring
dozens of Paragon's own internal token files with no official dark reference
to check the result against.

Instead, dark mode here overrides the same compiled `--pgn-color-*` custom
properties at a higher-specificity CSS scope, at runtime, in the browser.
This works because (verified against this package's own compiled output)
most of Paragon's component-level color tokens are themselves `var()`
references chasing down to about twenty base tokens (`--pgn-color-primary-*`,
`--pgn-color-secondary-*`, `--pgn-color-brand-*`, `--pgn-color-accent-*`,
`--pgn-color-gray-*`, `--pgn-color-white`, `--pgn-color-black`) -- override
those twenty and buttons, badges, nav, alerts, etc. all follow automatically.
A handful of derived tokens are baked to literal hex values at build time
instead (the `--pgn-color-action-default-{primary,secondary,brand,gray}-base`
hover-state tokens); those are overridden explicitly since the cascade can't
reach them. Paragon's own status colors (success/info/warning/danger) and
"light"/"dark" **button variant** tokens (`Button/light.json`,
`Button/dark.json` -- variant names, unrelated to page theme) are
deliberately left untouched in both light and dark mode, matching the rest of
this brand package's approach of deferring to Paragon's stock values for
anything the light theme itself doesn't override.

## Automatic (no setup required)

`paragon/styles/heritage.scss` includes a `@media (prefers-color-scheme:
dark)` block that activates whenever the visitor's OS/browser is set to dark
mode, with no plugin configuration, no script, and no image rebuild --
already live wherever `PARAGON_THEME_URLS` is configured (see
`docs/INSTALL-TUTOR.md`).

## Manual toggle (optional, advanced)

To let visitors override the OS preference with an explicit light/dark
switch, set `data-heritage-theme="dark"` or `="light"` on the `<html>`
element; the CSS in `heritage.scss` already responds to it (an explicit
`"light"` value also suppresses the automatic OS-preference block, so a
visitor who explicitly chooses light isn't overridden by a dark OS setting).

Getting a toggle **button** in front of visitors on every page requires
injecting a small script, since this is DOM/JS behavior, not something CSS
alone can add. The mechanism differs by surface:

### On Paragon MFEs (Verawood: also frontend-base apps)

tutor-mfe (v22+) ships a real, documented hook for this exact purpose:
`tutormfe.hooks.EXTERNAL_SCRIPTS`. It requires **an MFE image rebuild**
(`tutor images build mfe`), unlike the CSS layer above. Example plugin
snippet (adapt and test on staging first):

```python
from tutor import hooks
from tutormfe.hooks import EXTERNAL_SCRIPTS

NPM_INSTALL = """
RUN npm install @heritage-institute/theme-toggle-loader
"""
hooks.Filters.ENV_PATCHES.add_item(("mfe-dockerfile-post-npm-install", NPM_INSTALL))

EXTERNAL_SCRIPTS.add_item(("all", "HeritageThemeToggleLoader"))
```

This requires publishing an actual `@heritage-institute/theme-toggle-loader`
npm package implementing the loader class shape tutor-mfe expects
(`constructor({ config })` + `loadScript()`) -- not included in this
repository. See `overhangio/tutor-contrib-google-analytics` for a complete
reference implementation of the same loader pattern before building one for
this toggle.

### On classic Django-rendered LMS/CMS pages

These don't run MFE JavaScript at all, so `EXTERNAL_SCRIPTS` doesn't reach
them. Use a Tutor `ENV_PATCHES` entry targeting the LMS/CMS base template
patch location for your edx-platform version to inject a `<script>` tag
pointing at a small toggle script you host yourself (alongside this
package's `dist/` files, for example). This part follows the same
best-effort, not-build-verified status as `legacy-theme/` -- confirm the
exact patch location name against your edx-platform tag before relying on
it.
