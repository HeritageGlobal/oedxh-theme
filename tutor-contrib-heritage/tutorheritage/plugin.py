"""
Tutor plugin: Heritage Institute Open edX branding.

Wires the @heritage-institute/brand-openedx Paragon Design Tokens package into
an Open edX instance (Ulmo release) running on Tutor, by configuring
PARAGON_THEME_URLS (consumed by every Paragon-based MFE: learner dashboard,
profile, discussions, gradebook, and the Studio/course-authoring MFE) plus the
standard MFE logo/favicon settings.

This replaces the previous "drop a heritage.py file into the Tutor plugins
root" approach. That approach worked, but it hardcoded BRAND_BASE_URL as a
Python constant, meaning every change required editing and redistributing the
source file. This package instead registers real Tutor configuration
settings, so the brand URL, Paragon variant, and optional legacy-theme toggle
can all be set with the standard `tutor config save --set` workflow.
"""
from tutor import hooks

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# All settings are prefixed with HERITAGE_ per Tutor plugin convention, and
# registered as *defaults* (not "unique"/required), so the plugin works
# out-of-the-box against the published Heritage Institute CDN release, while
# remaining fully overridable per-instance, e.g.:
#
#   tutor config save --set HERITAGE_BRAND_BASE_URL=https://cdn.myschool.org/heritage/v1.0.0
#   tutor config save --set HERITAGE_PARAGON_VERSION=23.23.0
#
hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Immutable, versioned HTTPS location where this package's dist/
        # directory is published (npm+jsDelivr, a GitHub release tag+jsDelivr,
        # or any other CDN/static host). Never point this at an unversioned
        # "latest"/"main" URL in production -- see docs/COMPATIBILITY.md.
        ("HERITAGE_BRAND_BASE_URL", "https://cdn.jsdelivr.net/npm/@heritage-institute/brand-openedx@1.0.0/dist"),
        # Pin the exact @openedx/paragon version this brand package was built
        # and tested against, so $paragonVersion resolution in frontend-platform
        # can be cross-checked against docs/COMPATIBILITY.md during upgrades.
        ("HERITAGE_PARAGON_VERSION", "23.23.0"),
        # Only "light" is published by this brand package (see brand-metadata.json).
        ("HERITAGE_PARAGON_VARIANT", "light"),
        # Optional, best-effort legacy/comprehensive theming for Django-rendered
        # pages that do not consume Paragon Design Tokens at all (e.g. certain
        # legacy LMS views, some Studio views, Django admin). Off by default:
        # most Ulmo instances only need the Paragon token layer above, which
        # already covers the LMS/CMS MFEs (including the Studio/course-authoring
        # MFE), the learner-facing frontend, and any other Paragon-based MFE.
        # See docs/COMPATIBILITY.md and legacy-theme/README.md before enabling.
        ("HERITAGE_ENABLE_LEGACY_THEME", False),
    ]
)

# ---------------------------------------------------------------------------
# Paragon Design Tokens: MFE runtime theming (LMS, CMS/Studio MFE, and every
# other Paragon-based MFE all read the same site-wide MFE_CONFIG key)
# ---------------------------------------------------------------------------
# NOTE: the "{{ HERITAGE_BRAND_BASE_URL }}" tags below are Jinja placeholders
# resolved by Tutor's template renderer against the *current* config.yml
# value when `tutor config save` runs -- they are intentionally NOT Python
# f-string substitutions. An f-string would bake in whatever value the
# plugin's default happened to be at import time and silently ignore any
# `tutor config save --set HERITAGE_BRAND_BASE_URL=...` override, which was
# the bug in the previous single-file version of this plugin.
#
# "$paragonVersion" (note: single braces, no Jinja) is a literal token that
# @edx/frontend-platform substitutes client-side at runtime with the Paragon
# version actually installed in that MFE build -- it must NOT be templated
# by Tutor/Jinja here.
_PARAGON_THEME_URLS_PATCH = """\
MFE_CONFIG["PARAGON_THEME_URLS"] = {
    "core": {
        "urls": {
            "default": "https://cdn.jsdelivr.net/npm/@openedx/paragon@$paragonVersion/dist/core.min.css",
            "brandOverride": "{{ HERITAGE_BRAND_BASE_URL }}/core.min.css"
        }
    },
    "defaults": {
        "{{ HERITAGE_PARAGON_VARIANT }}": "{{ HERITAGE_PARAGON_VARIANT }}"
    },
    "variants": {
        "{{ HERITAGE_PARAGON_VARIANT }}": {
            "urls": {
                "default": "https://cdn.jsdelivr.net/npm/@openedx/paragon@$paragonVersion/dist/{{ HERITAGE_PARAGON_VARIANT }}.min.css",
                "brandOverride": "{{ HERITAGE_BRAND_BASE_URL }}/{{ HERITAGE_PARAGON_VARIANT }}.min.css"
            }
        }
    }
}
MFE_CONFIG["LOGO_URL"] = "{{ HERITAGE_BRAND_BASE_URL }}/logo.svg"
MFE_CONFIG["LOGO_TRADEMARK_URL"] = "{{ HERITAGE_BRAND_BASE_URL }}/logo-trademark.svg"
MFE_CONFIG["LOGO_WHITE_URL"] = "{{ HERITAGE_BRAND_BASE_URL }}/logo-white.svg"
MFE_CONFIG["FAVICON_URL"] = "{{ HERITAGE_BRAND_BASE_URL }}/favicon.ico"
"""

hooks.Filters.ENV_PATCHES.add_item(
    ("mfe-lms-common-settings", _PARAGON_THEME_URLS_PATCH)
)

# frontend-base (the newer, single-app MFE architecture landing after Ulmo)
# reads a structurally-translated version of PARAGON_THEME_URLS automatically
# -- openedx-platform PR #38610 added a translator that maps the legacy
# `variants.<name>.urls.brandOverride` value straight into frontend-base's
# SiteConfig `theme` setting. No separate patch is required here: instances
# that upgrade to frontend-base will keep working from the same MFE_CONFIG
# entry above. Re-validate against docs/COMPATIBILITY.md after any such
# upgrade, since this behavior is newer than the Ulmo release this package
# targets.

# ---------------------------------------------------------------------------
# Optional, best-effort legacy/comprehensive theming
# ---------------------------------------------------------------------------
# Django-rendered pages that never consume Paragon Design Tokens at all
# (see docs/COMPATIBILITY.md) are NOT reachable through PARAGON_THEME_URLS.
# For those, edx-platform's older "comprehensive theming" mechanism is the
# only lever available. This is intentionally opt-in and best-effort: it has
# not been build/rendering-verified against a live edx-platform image the
# way the Paragon token pipeline in this repository has been, and Tutor
# requires an image rebuild (`tutor images build openedx`) for it to take
# effect. See legacy-theme/README.md for the full, honest set of caveats
# before enabling this in production.
_LEGACY_THEME_DIR_NAME = "heritage"

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "{% if HERITAGE_ENABLE_LEGACY_THEME %}\n"
        "ENABLE_COMPREHENSIVE_THEMING = True\n"
        f'COMPREHENSIVE_THEME_DIRS.append("/openedx/themes")\n'
        f'DEFAULT_SITE_THEME = "{_LEGACY_THEME_DIR_NAME}"\n'
        "{% endif %}",
    )
)


# Declares that a host directory *named* "heritage-legacy-theme" (matched by
# name, not path -- see the Tutor mounts documentation) should be bind-mounted
# into the "openedx" image's /mnt/heritage-legacy-theme at build and run time.
# This only takes effect if the operator actually runs:
#     tutor mounts add /path/to/legacy-theme/heritage-legacy-theme
# AND sets HERITAGE_ENABLE_LEGACY_THEME=true. Declaring it here just teaches
# Tutor to recognize that directory name; it does not by itself enable or
# ship any theme content. See legacy-theme/README.md.
hooks.Filters.MOUNTED_DIRECTORIES.add_item(("openedx", "heritage-legacy-theme"))
