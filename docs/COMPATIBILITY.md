# Compatibility and upgrade notes

## Supported architecture

This project targets the Open edX **Ulmo** release, where Paragon Design
Tokens (Paragon >= 23) became the primary theming mechanism for MFEs, after
an alpha/testing period in Teak. `dist/` in this release was produced by
running `@openedx/paragon@23.23.0`'s own `build-tokens`/`build-scss` CLI
end-to-end against the token sources in `paragon/` -- see
`RELEASE-CHECKLIST.md` and `TOKEN-MAP.md` for exactly what was verified.

Later releases (e.g. Verawood) may ship newer Paragon major/minor versions
with schema changes -- see "Upgrade procedure" below before assuming this
package still applies unmodified. Do not treat "works on a later release"
as the default assumption; treat it as something to verify.

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
