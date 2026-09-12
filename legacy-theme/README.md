# Optional: legacy/comprehensive theme overlay

**Status: optional, best-effort, NOT build-verified.** Read this whole file
before enabling `HERITAGE_ENABLE_LEGACY_THEME`.

## What this is for

The Paragon Design Tokens package in this repository (`paragon/`, `dist/`)
themes every MFE that reads `PARAGON_THEME_URLS` -- which, on an Ulmo
instance, is the LMS learner dashboard, profile, discussions, gradebook, the
Studio/course-authoring MFE, and the rest of the current MFE fleet. It does
**not** reach:

- A handful of remaining Django-server-rendered LMS/CMS pages that predate
  the MFE migration and were never ported to consume Paragon tokens.
- The Django admin site (`/admin/`), which edx-platform does not theme at
  all by default.

For those, and only those, edx-platform's older "comprehensive theming"
system is the only lever available -- it works at the SCSS/template level
inside the `openedx` Docker image itself, which is a completely separate
build pipeline from Paragon Design Tokens (different variables, different
compiler, different deploy step).

## Why this is marked "not build-verified"

The Paragon token pipeline in `../paragon/` and `../dist/` was verified in
this deliverable by actually installing `@openedx/paragon` and running its
real `build-tokens`/`build-scss` CLI end-to-end. There is no edx-platform
checkout available in this environment to do the equivalent for a
comprehensive theme -- `_brand-colors.scss` here is a best-effort starting
point using variable names that are current as of recent Open edX releases,
not a compiled-and-inspected result. Confirm the variable names still match
your exact Ulmo edx-platform tag before trusting this in production (see the
comment at the top of that file for the command to check).

## Enabling it

1. Review and, if needed, correct `heritage-legacy-theme/heritage/lms/static/sass/partials/_brand-colors.scss`
   against your actual edx-platform tag.
2. Mount this directory into the `openedx` image:
   ```bash
   tutor mounts add /path/to/heritage-openedx-theme/legacy-theme/heritage-legacy-theme
   ```
3. Enable the toggle and rebuild the image (comprehensive theming is baked
   into the image at build time, unlike the Paragon token layer):
   ```bash
   tutor config save --set HERITAGE_ENABLE_LEGACY_THEME=true
   tutor images build openedx
   tutor local restart
   ```
4. Manually test every legacy page and `/admin/` on a staging instance.
   Comprehensive theming can silently fail to apply if a Sass variable name
   has changed upstream -- there is no build error for "variable not found,
   default used instead."

## Rolling back

```bash
tutor config save --set HERITAGE_ENABLE_LEGACY_THEME=false
tutor images build openedx
tutor local restart
```
