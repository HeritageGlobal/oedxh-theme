# Heritage Institute Theme — Customization Guide

## Brand basics

| Property | Value |
|---|---|
| Name | Heritage Institute |
| Tagline EN | Purpose driven education |
| Tagline ES | Educación con propósito |
| Descriptor EN | Cross-Cultural Research & Entrepreneurship |
| Descriptor ES | Investigación y Emprendimiento Transcultural |

Tone: authoritative, scholarly, warm; depth over brevity.

## Corporate colors

| Design token | Hex | Role |
|---|---|---|
| Heritage Crimson | `#6F0119` | Primary brand / CTA bands |
| Institute Teal | `#015270` | Secondary brand / vision / accents |
| Academic Gold | `#C5A444` | Accent / rules / labels / focus |
| White | `#FFFFFF` | Dark-surface text / fills |
| Ink Black | `#0E0E0E` | Hero / program backgrounds |
| Stone | `#F4F2ED` | Light page background |
| Mist | `#E8E4DB` | Borders / cards / dividers |

## Accessibility tokens

The source specification requires solid, accessible text values on dark surfaces:

```text
--heritage-on-dark        #E8E8E8
--heritage-on-dark-muted  #ABABAB
--heritage-on-dark-sub    #8A8A8A
--heritage-on-crimson     #F5E6B8
--heritage-on-teal        #E5F4FB
```

Do not replace these with low-opacity white/black text on dark surfaces.

## Typography

- Display: Cinzel 600/700
- Editorial/body: Cormorant Garamond 300/400 + italics
- UI: Jost 300/400/500

Paragon gets Jost as the principal sans-serif token and Cormorant Garamond as the serif token. Cinzel is exposed as `--heritage-font-display` and applied to headings through the small non-tokenizable brand layer because Paragon's global typography schema does not define a separate display family.

## Spacing

```text
small  = 1rem
medium = 2rem
large  = 4rem
xlarge = 6.5rem
content max = 1160px
body max = 66ch
```

## Buttons

The corporate specification requires 44px minimum interactive height, Jost 500, 0.875rem size, 0.1em tracking, and a 1.5px border.

Use the provided `.heritage-btn--gold`, `.heritage-btn--white`, and `.heritage-btn--crimson` helper classes only for custom pages. Standard Paragon buttons should receive their base colors from Paragon tokens first.

## Motion

Only one animated moment is specified: hero entrance (`fadeUp`, 0.65s ease). All animation rules are disabled or reduced under `prefers-reduced-motion`.

## What to edit

For visual changes that correspond to design decisions, edit JSON files in:

```text
paragon/tokens/core/global/
paragon/tokens/themes/light/
```

Use `paragon/styles/heritage.scss` only when a requirement cannot be represented by the Paragon token schema.

After edits:

```bash
npm run build
```

## Production font recommendation

The reference specification names Google Fonts. For production deployments with strict CSP, privacy, or reliability requirements, self-host the approved font files and replace the Google Fonts import in `paragon/_fonts.scss` with `@font-face` declarations.
