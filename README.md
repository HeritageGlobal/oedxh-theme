# Heritage Institute — Open edX Brand Package

A reusable Open edX brand/theme package for **Heritage Institute — Purpose driven education**, implemented around the Open edX / Paragon Design Tokens architecture.

## Design source

The implementation follows `Heritage-Institute-design-specs-brief.md` (v1.0, 2025) supplied with this project.

## Scope and release posture

This repository targets the **Open edX Ulmo release**, on the Paragon Design
Tokens theming model (Paragon 23.x). It is intentionally a token-native
brand package, not a legacy Indigo SCSS fork. It is built for a **Tutor**
deployment and is intended to work across the LMS, every current
Paragon-based MFE (learner dashboard, profile, discussions, gradebook, the
Studio/course-authoring MFE) and the learner-facing public frontend.
Coverage of a handful of remaining legacy Django-rendered pages and the
Django admin site is provided separately as an optional, best-effort add-on
-- see `legacy-theme/README.md`.

`dist/` in this release was produced by actually running
`@openedx/paragon@23.23.0`'s own `build-tokens` and `build-scss` CLI against
the token sources here, end to end -- not hand-written. See
`docs/RELEASE-CHECKLIST.md` and `docs/TOKEN-MAP.md` for what that caught and
fixed (a font-family token bug that produced invalid CSS, and a token
array-merge bug that let default Paragon fonts silently override part of the
brand font stack).

## What is included

- Paragon token overrides under `paragon/tokens/`
- Non-tokenizable brand CSS under `paragon/styles/heritage.scss`
- Real, CLI-built runtime CSS under `dist/`
- Open edX brand assets (`logo.svg`, `logo-white.svg`, `logo-trademark.svg`, `favicon.ico`)
- A preview page
- `tutor-contrib-heritage/`: a proper, pip-installable Tutor plugin (with a
  real `tutor.plugin.v1` entry point) that wires this package's
  `PARAGON_THEME_URLS`/logo/favicon settings into the instance, with the
  brand CDN URL exposed as a normal, overridable Tutor configuration setting
  rather than hardcoded in source
- `legacy-theme/`: an optional, clearly-marked best-effort comprehensive
  theming overlay for the small number of pages Paragon tokens don't reach
- Tutor installation/configuration documentation
- Token map and upgrade/compatibility notes

## Important implementation note

The supplied corporate specification does **not** contain an original logo artwork file. Therefore the repository includes a clean typographic/monogram placeholder lockup based on the specification. Replace the four brand asset files with the approved corporate artwork when available; the required filenames are part of the Open edX brand package interface.

## Requirements

- Open edX **Ulmo** release (Tutor-based deployment).
- Paragon 23.x design tokens (this package is built and CLI-verified against `@openedx/paragon@23.23.0`; see `docs/COMPATIBILITY.md` before using with a different Paragon version).
- Node.js >= 18 (see `.nvmrc`).
- Tutor + tutor-mfe for the recommended deployment path; `tutor-contrib-heritage/` in this repository is the plugin that wires everything together.

## Quick build

```bash
npm install
npm run build
```

`npm run build` runs `build-tokens` → `build-scss` → `copy-assets` → `validate`
(see `Makefile`). The `validate` step is a cheap sanity check (balanced
braces, no regression of the font-family bug described in
`docs/TOKEN-MAP.md`) -- it is not a substitute for testing the generated CSS
against real MFEs, per `docs/RELEASE-CHECKLIST.md`.

The repository also ships pre-built `dist/core.css`, `dist/core.min.css`,
`dist/light.css`, `dist/light.min.css` and `dist/theme-urls.json`, generated
by this same real build, so the brand can be hosted immediately while a
Node build environment is being prepared.

## Runtime theming model

Open edX's `@edx/frontend-platform` loads Paragon core/theme CSS externally
through `PARAGON_THEME_URLS`. The brand override stylesheet is loaded after
the default Paragon stylesheet so the token values and brand-layer rules
take precedence. `tutor-contrib-heritage/` configures this for you; see
`docs/INSTALL-TUTOR.md` for the full setup, including the manual/DIY version
of the underlying Tutor patch if you'd rather not use the provided plugin.

## Deploying the Tutor plugin

```bash
pip install -e ./tutor-contrib-heritage
tutor plugins enable heritage
tutor config save --set HERITAGE_BRAND_BASE_URL=<your published dist/ URL>
tutor config save
tutor local restart
```

See `tutor-contrib-heritage/README.md` for every available setting.

## Customization workflow

1. Edit the JSON design tokens under `paragon/tokens/`.
2. Run `npm run build` (fails loudly via `make validate` on the specific font-array regression documented in `docs/TOKEN-MAP.md`).
3. Open `preview/index.html` and manually test the generated CSS against the target Open edX release's real MFEs -- see `docs/RELEASE-CHECKLIST.md`.
4. Commit the source and generated `dist/` files together.
5. Publish the package to a private/public npm registry, or serve the `dist/` files from an immutable, versioned HTTPS CDN URL, and point `HERITAGE_BRAND_BASE_URL` at it.

## License

Proprietary brand implementation for Heritage Institute. Open edX/Paragon remains governed by its respective project licenses. Update this file before public redistribution.
