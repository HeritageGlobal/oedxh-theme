# Compatibility and upgrade notes

## Supported architecture

This project targets the Open edX **Ulmo** release, where Paragon Design
Tokens (Paragon >= 23) became the primary theming mechanism for MFEs, after
an alpha/testing period in Teak. `dist/` in this release was produced by
running `@openedx/paragon@23.23.0`'s own `build-tokens`/`build-scss` CLI
end-to-end against the token sources in `paragon/` -- see
`RELEASE-CHECKLIST.md` and `TOKEN-MAP.md` for exactly what was verified.

### Verawood

Confirmed compatible, based on the official Verawood Developer & Operator
Release Notes (`docs.openedx.org` and the Open edX Community wiki):

- Verawood still uses Paragon v23 -- no design-token schema changes to
  account for. `HERITAGE_PARAGON_VERSION` in `tutor-contrib-heritage`
  remains `23.23.0`.
- Verawood introduces **frontend-base**, a new single-shell MFE
  architecture (OEP-65), but adoption is per-app and mostly opt-in in this
  release: the Authn and Learner Dashboard frontend-base apps ship
  *disabled* by default (their classic MFE equivalents remain active
  unless an operator opts in), while only the Instructor Dashboard and
  Notifications frontend-base apps are *enabled* by default. The
  Studio/course-authoring MFE is unaffected either way.
- Whichever pipeline ends up serving a given app, `PARAGON_THEME_URLS`
  reaches it without any extra configuration: tutor-mfe's frontend-base
  implementation auto-translates `MFE_CONFIG`/`MFE_CONFIG_OVERRIDES`
  (including `PARAGON_THEME_URLS`) into frontend-base's `SiteConfig` via
  its `/api/frontend_site_config/v1/` endpoint, and openedx-platform PR
  #38610 specifically narrows that translation to the
  `variants.<name>.urls.brandOverride` value this package sets -- exactly
  the field `tutor-contrib-heritage` populates.
- If you later enable the Authn or Learner Dashboard frontend-base apps
  (recommended by the Verawood notes as a way to test existing
  customizations ahead of Willow, where conversion becomes mandatory for
  most MFEs), re-run this package's checklist in `RELEASE-CHECKLIST.md`
  against those apps specifically -- the CSS variable layer should carry
  over unchanged, but the release notes note that "any branding, plugins,
  and forks of MFEs will need to be ported accordingly," so budget time to
  verify rather than assume.
- No changes were needed to this package's dark-mode CSS layer
  (`docs/DARK-MODE.md`) for Verawood -- it's plain CSS custom properties,
  unaffected by which shell architecture loads it.

Later releases still ship newer Paragon major/minor versions with schema
changes eventually -- see "Upgrade procedure" below before assuming this
package still applies unmodified on releases after Verawood. Do not treat
"works on a later release" as the default assumption; treat it as something
to verify.

## Important boundaries

### Paragon-enabled MFEs

These are the primary target. Configure `PARAGON_THEME_URLS` so the Paragon CSS loads first and Heritage brand overrides load after it.

### Legacy Django-rendered pages and Django admin

The design-token system is not a complete replacement for the historical
Open edX Django theme system, and does not reach the Django admin site at
all. This package's `PARAGON_THEME_URLS`/MFE layer covers the LMS, every
current Paragon-based MFE (including the Studio/course-authoring MFE), and
the learner-facing public frontend. Coverage for remaining legacy pages and
`/admin/` is provided as a separate, optional, best-effort overlay -- see
`../legacy-theme/README.md` for exactly what is and is not verified there,
and the honest caveats before enabling it.

### Third-party MFEs

A third-party MFE may use custom CSS variables or hard-coded styles. Audit it before promising full brand coverage.

### Custom/forked MFEs

Prefer Paragon tokens and frontend plugin framework slots where possible. Avoid forking solely for visual changes.

## Upgrade procedure

Before each Open edX release upgrade:

1. Record the Open edX release and Paragon version.
2. Install the new package version in a staging instance.
3. Build the brand with that Paragon version.
4. Compare all required pages and MFEs.
5. Check CSS variable names used by the brand package.
6. Re-test keyboard focus, responsive behavior, contrast and reduced-motion behavior.
7. Promote the new brand package only after staging validation.

## Rollback

Keep each generated brand package version immutable. Roll back by changing the `PARAGON_THEME_URLS` brandOverride URLs from `vX.Y.Z` to the last known-good release and restarting the MFE configuration path if required.

## External CSS considerations

Runtime theme loading is valuable because the theme can change without rebuilding every consuming MFE. However, external CSS becomes a production dependency. Use HTTPS, cache headers, immutable versioned assets, and monitoring. A CDN outage should not make the application unusable; validate the fallback behavior of the target Open edX/frontend-platform version.
