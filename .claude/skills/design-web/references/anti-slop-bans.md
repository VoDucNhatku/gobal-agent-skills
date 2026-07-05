# Anti-Slop Banned Patterns

Explicitly banned defaults. Any surface matching these patterns gets a finding.
Read this file; reference it, never inline it.

## Banned Fonts

Never use as primary or body: Inter, Roboto, Arial, Helvetica, system-ui.
If using them at all, pair with a strong display face and restrict to small UI labels only.

## Banned Gradients

Never use the SaaS purple gradient: `#7C3AED` → `#DB2777` (or any near-equivalent hue shift).
This includes hero blobs, button gradients, and card borders.

## Banned Layouts

- Centered hero + 3 feature cards + accordion FAQ + CTA band
- Every section the same full-width padded box with no rhythm
- Predictable card grids with equal spacing and no asymmetry

## Banned Components

- Untouched default shadcn with default radius (0.5rem), default shadow, default spacing
- Emoji used as icons (in buttons, nav, feature bullets, empty states)

## Banned Color Strategies

- Five colors at equal weight with no dominant or accent
- Flat pure `#FFF` / `#000` backgrounds with no atmosphere

## Banned Clusters (do not match any of these)

(a) Warm cream + serif + terracotta "editorial feel" without reinterpretation
(b) Near-black + acid-green/vermilion "cyber" without reinterpretation
(c) Broadsheet hairlines + serif "newspaper" without reinterpretation
