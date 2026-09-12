# Installing Heritage Institute branding on a new Tutor/Open edX instance

## 1. Recommended production architecture

Use two CSS layers for MFEs:

1. The exact Paragon version used by the MFE.
2. The Heritage Institute brand override (`core.min.css` and `light.min.css`).

This follows the Open edX runtime theming model, where MFEs load external Paragon CSS and optional brand override CSS through `PARAGON_THEME_URLS`.

## 2. Publish the brand package

Choose one:

### Option A — npm

Publish the package as:

```text
@heritage-institute/brand-openedx
```

Recommended production command:

```bash
npm publish --access public
```

Use a private registry instead when the package is not intended to be public.

### Option B — Git + CDN

Keep this repository in GitHub/GitLab and publish `dist/` through a versioned HTTPS URL/CDN.

For a public GitHub repository, jsDelivr can be used, e.g.:

```text
https://cdn.jsdelivr.net/gh/ORG/heritage-openedx-theme@v1.0.0/dist/core.min.css
https://cdn.jsdelivr.net/gh/ORG/heritage-openedx-theme@v1.0.0/dist/light.min.css
```

Do not use `main` for production. Pin a release tag.

## 3. Configure Tutor's MFE runtime theme URLs

This repository ships a ready-made, real Tutor plugin package at
`../tutor-contrib-heritage/` -- it is a proper installable package with a
`tutor.plugin.v1` entry point (not a bare `.py` file dropped into the
plugins directory), and it exposes `PARAGON_THEME_URLS`/logo/favicon as
standard Tutor configuration settings rather than hardcoded source values:

```bash
pip install -e /path/to/heritage-openedx-theme/tutor-contrib-heritage
tutor plugins enable heritage
tutor config save --set HERITAGE_BRAND_BASE_URL=https://cdn.jsdelivr.net/gh/ORG/heritage-openedx-theme@v1.0.0/dist
tutor config save
tutor local restart
```

See `../tutor-contrib-heritage/README.md` for the full list of settings
(`HERITAGE_BRAND_BASE_URL`, `HERITAGE_PARAGON_VARIANT`,
`HERITAGE_ENABLE_LEGACY_THEME`). This has been tested end-to-end against a
real `tutor`+`tutor-mfe` install in this repository's own build process:
`tutor plugins enable heritage` correctly discovers and enables the plugin,
and `tutor config save --set HERITAGE_BRAND_BASE_URL=...` correctly updates
the rendered `PARAGON_THEME_URLS` in the generated LMS/CMS settings files.

If you would rather write your own plugin instead of using the one provided,
the underlying mechanism it wraps is still the standard one:

```python
from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item((
    "mfe-lms-common-settings",
    """
MFE_CONFIG["PARAGON_THEME_URLS"] = {
    "core": {
        "urls": {
            "default": "https://cdn.jsdelivr.net/npm/@openedx/paragon@$paragonVersion/dist/core.min.css",
            "brandOverride": "https://cdn.jsdelivr.net/gh/ORG/heritage-openedx-theme@v1.0.0/dist/core.min.css"
        }
    },
    "defaults": {"light": "light"},
    "variants": {
        "light": {
            "urls": {
                "default": "https://cdn.jsdelivr.net/npm/@openedx/paragon@$paragonVersion/dist/light.min.css",
                "brandOverride": "https://cdn.jsdelivr.net/gh/ORG/heritage-openedx-theme@v1.0.0/dist/light.min.css"
            }
        }
    }
}
""",
))
```

Prefer registering the brand URL as a real `CONFIG_DEFAULTS` setting (as
`tutor-contrib-heritage` does) over hardcoding it directly in the patch
string above -- a hardcoded value can only be changed by editing and
redistributing your plugin's source, whereas a config setting can be
changed with `tutor config save --set`.

For an installation already using the newer frontend-base runtime
configuration path (post-Ulmo), no separate action is needed: openedx-platform
includes a structural translator that maps the `variants.<name>.urls.brandOverride`
value straight into frontend-base's site-level `theme` config automatically.
Re-verify against this file's "Upgrade procedure" after any such upgrade.

## 4. Logo and favicon URLs

`tutor-contrib-heritage` already sets `MFE_CONFIG["LOGO_URL"]`,
`LOGO_TRADEMARK_URL`, `LOGO_WHITE_URL`, and `FAVICON_URL` from the same
`HERITAGE_BRAND_BASE_URL` setting above -- no separate configuration step is
needed. If you're writing your own plugin instead, set the equivalents
directly:

```python
MFE_CONFIG["LOGO_URL"] = "https://brand.example.org/heritage/logo.svg"
MFE_CONFIG["LOGO_TRADEMARK_URL"] = "https://brand.example.org/heritage/logo-trademark.svg"
MFE_CONFIG["LOGO_WHITE_URL"] = "https://brand.example.org/heritage/logo-white.svg"
MFE_CONFIG["FAVICON_URL"] = "https://brand.example.org/heritage/favicon.ico"
```

## 5. Install the brand package when an MFE needs the npm package itself

The runtime CSS path is sufficient for MFE theming. Some build pipelines/components may also need the brand package as `@edx/brand`.

The OEP-48 approach is to alias the custom package:

```bash
npm install @edx/brand@npm:@heritage-institute/brand-openedx@1.0.0
```

For Tutor, inject that installation through the relevant MFE Dockerfile npm-install hook when your release requires it.

## 6. Legacy LMS / Studio pages and Django admin

The design-token system primarily covers Paragon-enabled frontend
applications -- on Ulmo, that's the LMS, the Studio/course-authoring MFE,
and the rest of the current MFE fleet. A small number of legacy
Django-rendered pages, and the Django admin site, are not reachable this
way. Do **not** assume that setting `PARAGON_THEME_URLS` is a complete
replacement for every historical Tutor `settheme` customization.

For those, use `HERITAGE_ENABLE_LEGACY_THEME` and `../legacy-theme/README.md`
-- an optional, separate, best-effort overlay that is explicitly *not*
build-verified the way the Paragon token layer in this package is.

Use the compatibility checklist in `docs/COMPATIBILITY.md` before going to production.
