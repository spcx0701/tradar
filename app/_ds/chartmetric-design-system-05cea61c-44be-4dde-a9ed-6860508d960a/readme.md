# Chartmetric Design System

A design system for **Chartmetric** — the leading music-data analytics platform. "Advancing music with data & AI." Chartmetric aggregates 11M+ artists, 130M+ tracks and 26M+ playlists across 30+ sources (Spotify, Apple Music, YouTube, TikTok, Instagram, Shazam, SoundCloud, Deezer, Amazon Music, X, Twitch, Pandora…) into one dashboard for A&R teams, artist managers, digital marketers, music supervisors, brand-partnership teams, labels, and artists.

The product mantra: **"data _plus_ intuition, not data _vs._ intuition."** The interface is a light, dense, scannable analytics surface — near-white canvas, white cards, one near-black ink, a near-black sidebar, and a tightly **rationed blue accent** derived from the logo gradient.

> Use cases / products: Artist Analytics · Playlist Analytics · Track Analytics · Radio Analytics · Curator Analytics · Charts · A&R Tools · Brand Analytics · Custom Services · Developer API. Companion iOS/Android apps.

## Sources used
The authenticated app (`https://app.chartmetric.com/`) is login-gated and could not be accessed directly. This system was reconstructed from Chartmetric's **public** brand surface and documented design decisions:
- Marketing site — `https://chartmetric.com/` (brand color `#08080b`, the logo gradient, product taxonomy, voice).
- Chartmetric design team write-up — `https://hmc.chartmetric.com/chartmetric-product-updates-and-design-decisions/` ("the interface is unified by shades of blue derived from our new logo, reserved for hover states and primary interactions").
- Brandfetch — `https://brandfetch.com/chartmetric.com`; App Store / Google Play listings; G2.
- Logo + artist imagery from Chartmetric's public CDN (`cdn.sanity.io/images/zdrkqyxr/...`).

⚠️ **Not given a codebase or Figma.** Exact production type, spacing constants, and component internals are inferred, not copied. See CAVEATS at the bottom. If you can share the app's source or Figma, this system can be made pixel-exact.

---

## CONTENT FUNDAMENTALS

**Voice:** confident, plainspoken, and music-literate. Chartmetric talks to professionals who live in the data but trust their ears. Insight-first ("turn complex artist data into actionable insights"), never hype. It explains the _why_ behind the number — "providing not only the insight through data but also the explanations behind what is happening."

**Person & address:** second person ("**you**", "**your** artists"), first-person plural for the company ("**we** believe in data plus intuition"). Imperative verbs lead feature copy: _Spot · Track · Discover · Compare · Decode · Empower._

**Casing:** Title Case for nav, feature names, and section eyebrows (Artist Analytics, Talent Discovery, Noteworthy Insights). Sentence case for body and descriptions. UPPERCASE only for tiny overline/eyebrow labels (letter-spaced).

**Numbers are the message.** Always tabular, always with context — a raw value plus its delta and timeframe ("38.2M monthly listeners ▲4.3% vs 28d"). Abbreviate large counts (4.21M, 92.3K). Percentages to one decimal. Never a number without a unit or comparison.

**Tone examples**
- ✓ "Spot the next breakout before the charts do."
- ✓ "Track performance across streaming, social, and radio."
- ✓ "Chartmetric is what the new A&R's need."
- ✗ "Leverage synergistic data paradigms."
- ✗ "The world's #1 best amazing music tool!!!"

**Emoji:** sparing and purposeful in _marketing_ surfaces only (an occasional 🎶 or 🌎). **Never** inside the product UI — meaning is carried by icons, color, and the career-stage/momentum taxonomy.

**Domain vocabulary:** CM Score, Popularity, Engagement, Career Stage (Legendary → Superstar → Mainstream → Mid-Level → Developing), Recent Momentum (Explosive Growth → Decline), Network Strength, Social Engagement, Playlist Reach, Shortlist, Comparables, Trigger Cities, Curators, Noteworthy Insights.

---

## VISUAL FOUNDATIONS

**Color.** A disciplined, mostly-monochrome data surface with rationed color.
- **Canvas** `--cm-n-50` (#F6F8FA); **surfaces** pure white; **ink** `--cm-n-900` (#0C0D11); **sidebar** the brand near-black `--cm-ink-black` (#08080B).
- **Accent** a single brand **blue** (`--cm-blue-500` #1D68F0) for primary actions, active nav, links, and focus — _used sparingly_, exactly as the Chartmetric team describes.
- **Signature gradient** cyan→blue→violet (`--cm-gradient-brand`), lifted from the logo mark; reserved for hero/brand moments, account avatars, and score accents — not for everyday UI chrome.
- **Semantic data palette** drives every metric: growth green `--cm-positive`, decline red `--cm-negative`, steady gray, warning amber. These colors _mean_ something and are never decorative.
- **Career-stage ramp** (gold→violet→blue→cyan→slate) doubles for Momentum / Network / Engagement tiers.
- **Platform colors** carry each data source's real brand hue.

**Type.** `Inter` for everything UI (humanist grotesque with excellent tabular figures); `JetBrains Mono` for IDs/API/code. Compact **14px base** for density; tight display sizes for metric headlines (700–800 weight, −0.02em). **Tabular lining numerals everywhere data appears** so columns align — non-negotiable. Eyebrow labels are 11px uppercase, letter-spaced, gray.

**Spacing & layout.** 4px base grid; dense control padding, 16px tile gaps, 24px page gutters. Fixed **240px** dark sidebar + sticky **60px** top bar with the global search ("Add Data" lives in search). Content max-width ~1200px, centered. Dashboards are card grids; tables are wide and dense with **sticky headers**.

**Cards.** White fill, **1px `--cm-border` hairline**, `--cm-radius-xl` (10px) corners, and a whisper `--cm-shadow-card`. Borders do most of the separation work; shadows are reserved for raised/floating surfaces (menus, popovers, hover-lifted rows).

**Corners.** Gently rounded, never pill-soft: 6px controls, 8px nested panels, 10px cards, 14px feature cards, full-round for badges/avatars/switches.

**Elevation & shadows.** Restrained and cool-tinted (`rgba(12,13,17,…)`). Five steps: xs (card rest) → xl (modal). No colored or glow shadows except the blue focus ring.

**Backgrounds.** Flat. No photographic or gradient page backgrounds in-product; the only gradient is the brand mark. Marketing surfaces add subtle decorative SVGs (stars, asterisks, circular lines) and artist photography, but the app stays clean.

**Imagery.** Artist/track artwork (square for releases, circle for artists) is the only imagery in-product, full-color as supplied by the platforms. No filters or duotones.

**Borders & dividers.** 1px `--cm-border` (#E1E6EC) hairlines; row separators are the lighter `--cm-n-100`.

**Transparency & blur.** Sparingly — the sticky top bar uses a translucent white + backdrop blur; overlays use a soft scrim. Otherwise surfaces are opaque.

**Motion.** Quick and functional, **no bounce**. 120–240ms, one standard ease `cubic-bezier(0.2,0.6,0.2,1)`. Charts/score-rings draw in (~360ms). Reduced-motion fully honored (durations → 0).

**Hover states.** Background/border shift, never scale: buttons darken (`--cm-blue-600`), ghost/nav items gain a faint fill, table rows tint `--cm-n-50`, cards may lift to `--cm-shadow-md`.

**Press states.** Darken further (`--cm-blue-700`); no shrink/scale.

**Focus.** A 3px blue ring (`--cm-glow-accent`) on `:focus-visible` for every interactive control.

---

## ICONOGRAPHY

Chartmetric's interface is icon-light and meaning-dense; icons are simple line glyphs at small sizes, paired with text labels in nav and used solo in toolbars/table rows.

- **UI icons — Material Symbols Rounded (Google Fonts), substituted.** Chartmetric's exact in-app icon set isn't public, so this system standardizes on **Material Symbols Rounded** — a clean, neutral, rounded line set that matches the product's calm, modern feel and is colorable/scalable via CSS. Load the font and use `<span class="ms">search</span>` (a helper `Icon` component ships in the UI kit). _Flag: swap for the real set if provided._
- **Platform glyphs — real brand marks, inlined SVG.** Data-source logos (Spotify, Apple Music, YouTube, TikTok, Instagram, SoundCloud, Shazam, Deezer, X, Twitch, Pandora) are **not** hand-drawn — they are the real Simple Icons single-path marks, embedded directly in the `PlatformIcon` component (`components/data/PlatformIcon.jsx`), rendered in each platform's brand color or as a filled brand-color chip. No network dependency.
- **Logo.** The Chartmetric gradient wordmark (SVG) is referenced from the brand CDN — see `assets/README.md`.
- **No emoji as iconography** in-product. Marketing may use the occasional 🎶/🌎; the app does not.
- **No Unicode-glyph icons.** Arrows in deltas (▲▼) are the one intentional exception — they read as data, not decoration, and sit in tabular metric contexts.

---

## INDEX / MANIFEST

Root
- **`styles.css`** — the one file consumers link. `@import`s only.
- **`readme.md`** — this guide. **`SKILL.md`** — Agent-Skills entry point.

`tokens/` (all `@import`ed by `styles.css`)
- `fonts.css` · `colors.css` · `typography.css` · `spacing.css` · `radius.css` · `shadows.css` · `motion.css`

`components/` — React primitives (read via `window.ChartmetricDesignSystem_05cea6`)
- **core/** — `Button`, `IconButton`, `Badge`, `Tag`, `Input`, `Select`, `Switch`, `Avatar`, `Tabs`
- **data/** — `MetricStat`, `ScoreRing`, `TrendDelta`, `Sparkline`, `PlatformIcon`, `StageBadge` (+ exports `CM_PLATFORMS`, `CM_CAREER_STAGES`)
- Each has `.jsx` + `.d.ts` + `.prompt.md`; one `@dsCard` HTML per directory.

`guidelines/` — foundation specimen cards (Design System tab): Colors (Brand Blue, Gradient, Neutrals, Semantic, Career Stages, Platforms), Type (Scale, Numerals, Weights), Spacing (Scale, Radius, Elevation), Brand (Logo, Voice & Tone).

`ui_kits/app/` — interactive Chartmetric app recreation: Artist Profile · Charts leaderboard · Talent Discovery. See its `README.md`.

`assets/` — logo + icon source references (`README.md`).

---

## CAVEATS
- **No codebase/Figma was provided and the app is login-gated**, so component internals, exact spacing/type constants, and some color values are faithful inferences from public brand material — not copied source. Treat numbers as a strong, coherent approximation.
- **Fonts substituted:** Inter (UI) + JetBrains Mono. The real in-app typeface is unconfirmed.
- **Icons substituted:** Material Symbols Rounded for UI glyphs. Platform marks and the logo are real (loaded from CDNs); brand binaries are referenced, not vendored (sandbox blocks cross-origin binary copy).
