# Release Checklist — Heritage Institute Open edX Brand Package

## Before release

- [ ] Confirm target Open edX release is **Ulmo** (see `docs/COMPATIBILITY.md` before targeting anything else).
- [ ] Run `make build` (or `npm run build`) and confirm `dist/core.css`, `dist/core.min.css`, `dist/light.css`, `dist/light.min.css`, and `dist/theme-urls.json` are regenerated. `make validate` runs automatically as part of this and will fail the build on the font-array regression described in `docs/TOKEN-MAP.md`.
- [ ] Confirm the Heritage logo assets and favicon are the intended production artwork (see the placeholder note in `README.md`).
- [ ] Check `brand-metadata.json` version numbers and target Paragon version.
- [ ] Test the generated CSS against the actual Open edX MFEs used by the instance -- `make validate` is a cheap automated sanity check, not a substitute for this.
- [ ] Verify keyboard focus, skip navigation, reduced-motion behavior, language attributes, and dark-surface contrast.
- [ ] Test the external CSS URLs over HTTPS from the same browser/network conditions expected for students.
- [ ] If `HERITAGE_ENABLE_LEGACY_THEME` will be used, complete the separate checklist in `../legacy-theme/README.md` first -- that layer is not build-verified the way the Paragon token layer above is.

## Publish

Publish the contents of `dist/` at an immutable versioned URL or publish the
package to npm. Do not overwrite an in-use version in place. Point
`HERITAGE_BRAND_BASE_URL` (the Tutor config setting exposed by
`tutor-contrib-heritage`) at that immutable release.

## Deploy

1. `pip install -e ./tutor-contrib-heritage && tutor plugins enable heritage`, or apply the equivalent `MFE_CONFIG` settings manually (see `docs/INSTALL-TUTOR.md`).
2. `tutor config save --set HERITAGE_BRAND_BASE_URL=<immutable dist/ URL>`.
3. `tutor config save`.
4. Restart or rebuild the required MFE services according to the Open edX release and deployment mode -- the Paragon token layer only needs a restart (client-side CSS load), not an image rebuild.
5. Test LMS, Studio (course-authoring MFE), and every other MFE that consumes `PARAGON_THEME_URLS`.
6. Keep the previous brand URL available until rollback testing is complete.

## Rollback

Rollback means changing `HERITAGE_BRAND_BASE_URL` to the previous known-good
immutable version (`tutor config save --set HERITAGE_BRAND_BASE_URL=...`),
saving Tutor configuration, and restarting the affected MFE services.
