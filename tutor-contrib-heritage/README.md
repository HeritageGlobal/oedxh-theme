# tutor-contrib-heritage

A proper, pip-installable Tutor plugin that wires the Heritage Institute
Paragon Design Tokens brand package (`@heritage-institute/brand-openedx`,
in the parent directory of this repository) into an Open edX **Ulmo**
instance running on Tutor.

## Why this replaced the previous `heritage.py` file

Earlier versions of this brand package shipped a bare `heritage.py` file
(meant to be copied into `tutor plugins printroot`) alongside an incomplete
`tutor_contrib_heritage/` Python package that had no `setup.py`/`pyproject.toml`
and therefore no `tutor.plugin.v1` entry point — Tutor could never actually
discover it via `pip install`. Both also hardcoded the brand CDN URL as a
Python constant, so changing it meant editing and redistributing source code
instead of running a normal `tutor config` command.

This package fixes both problems: it is a single, real, installable plugin,
and every value an operator is likely to change is a proper Tutor
configuration setting.

## Install

```bash
pip install -e /path/to/heritage-openedx-theme/tutor-contrib-heritage
tutor plugins enable heritage
```

## Configure

```bash
# Required in production: point at your own immutable, versioned CDN release
# of the dist/ directory built from the parent brand package (see the top-level
# README.md and docs/INSTALL-TUTOR.md for how to publish it).
tutor config save --set HERITAGE_BRAND_BASE_URL=https://cdn.example.org/heritage-openedx/v1.0.0

# Optional -- defaults shown
tutor config save --set HERITAGE_PARAGON_VERSION=23.23.0   # for your own cross-checks; informational only
tutor config save --set HERITAGE_PARAGON_VARIANT=light      # only "light" is published by this brand package
tutor config save --set HERITAGE_ENABLE_LEGACY_THEME=false  # see ../legacy-theme/README.md before enabling

tutor config save
tutor local restart   # or: tutor local launch, on a fresh instance
```

No image rebuild is required for the Paragon token layer -- `PARAGON_THEME_URLS`
is consumed by `@edx/frontend-platform` at runtime in the browser, so a config
save + service restart is enough. This covers every Paragon-based MFE: the
learner dashboard, profile, discussions, gradebook, the Studio/course-authoring
MFE, and any other MFE built against `@openedx/paragon` >= 23 with design
token support.

If you enable `HERITAGE_ENABLE_LEGACY_THEME`, see `../legacy-theme/README.md` --
that path *does* require an image rebuild and is optional/best-effort, per
`../docs/COMPATIBILITY.md`.

## What this plugin does NOT do

- It does not publish the brand package for you. Build and host `dist/`
  first (see the top-level `README.md`), then point `HERITAGE_BRAND_BASE_URL`
  at that immutable location.
- It does not install `@heritage-institute/brand-openedx` as an npm package
  into any MFE's `node_modules`. That's only needed if you're doing local
  MFE development against the brand package directly (module.config.js
  aliasing) rather than the runtime-CSS path this plugin configures. See
  `../docs/INSTALL-TUTOR.md` section 5 if you need that.
