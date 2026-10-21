# Agent guide: Countdown Banner for Shopify

Instructions for AI coding agents (Claude Code, Cursor, Codex, etc.) installing or customizing this section. Humans should start with [README.md](README.md).

## What this is

A single Shopify theme section, `sections/countdown-banner.liquid`. It renders a sale banner with a live days / hours / minutes countdown. It shows between a start and end time, hides itself when the sale ends, can stick to the top of the screen and can scroll as a marquee. It is built to drop into the **header group** of any Online Store 2.0 theme without changes.

```
sections/countdown-banner.liquid   The product. Markup, CSS, JS and schema in one file.
demo/index.html                    Browser preview with no store. CSS and JS are generated.
demo/build_demo.py                 Copies the section's CSS and JS into demo/index.html
```

## Installing into a theme

With Shopify CLI, from the user's theme directory:

1. Copy `sections/countdown-banner.liquid` into the theme's `sections/` folder.
2. Add it to the header group so it shows on every page. In `sections/header-group.json`, add an entry under `sections` and put its key first in `order`:
   ```json
   "countdown_banner": { "type": "countdown-banner", "settings": {} }
   ```
   Empty `settings` uses the schema defaults. Or let the human add it in the theme editor (**Header > Add section > Countdown banner**).
3. Push to an **unpublished** theme first: `shopify theme push --unpublished --theme "With countdown"`, or `--only sections/countdown-banner.liquid --only sections/header-group.json` against an existing theme ID.
4. Ask the human before pushing to the live theme (`--allow-live`).

`header-group.json` is rewritten by the theme editor. Pull it from the store before editing so you don't overwrite the merchant's header changes.

## Hard rules when changing the section

These keep it portable. Breaking one usually works in the theme you're testing and fails in every other theme.

1. **Stay one file.** CSS goes in `{% stylesheet %}`, JS in `{% javascript %}`. No new files in `assets/` or `snippets/`. `{% stylesheet %}` and `{% javascript %}` can't contain Liquid; pass values through CSS variables or `data-` attributes on `<countdown-banner>`.
2. **No theme dependencies for core behavior.** Don't rely on a theme's classes, CSS variables or JS. Theme-specific rules are allowed only as optional extras that do nothing in other themes, like the Horizon and Dawn sticky-header rules.
3. **Prefix everything.** Classes are `countdown-banner__*`, CSS variables `--countdown-*`, the custom element is `<countdown-banner>`, the section wrapper class is `countdown-banner-section`.
4. **Every shopper-facing string is a setting**, so merchants can translate it. Schema labels are plain English, not `t:` keys, because the section can't ship locale files.
5. **Guard the element definition**: `if (customElements.get('countdown-banner')) return;`. `{% javascript %}` runs once per page.
6. **Keep the Liquid and JS countdown math in sync.** Liquid renders the first frame (no flash of `00`), JS takes over. Both round minutes up when seconds are hidden.

## How the file is laid out

Top to bottom:

1. **Liquid setup** (`{%- liquid -%}`): builds ISO strings like `2026-12-01T23:59:00-05:00` from the `start`, `end` and `timezone` settings. Works out `valid`, `expired` and `active`, and the starting days / hours / minutes / seconds. The `date` filter returns its input unchanged when it can't parse it, so a result containing `-` means a badly formatted date.
2. **Root element** `<countdown-banner>`: `data-start`, `data-end`, `data-show-seconds`, `data-sticky`, `data-scrolling`, `data-scroll-speed`, `data-editor` (theme editor only). Colors and sizes are inline CSS variables. It renders `hidden` unless the sale is live, except in the theme editor. Past the end date nothing renders at all outside the editor.
3. **`.countdown-banner__inner`**: heading, timer (`[data-unit]` spans with a `[data-value]` inside) and an optional button. The button is a `<span>`, visual only.
4. **`.countdown-banner__cover-link`**: one `<a>` covering the whole banner when a link is set. It sits outside `__inner` on purpose so scrolling copies don't duplicate it and it doesn't move.
5. **`{% stylesheet %}`**: base styles, mobile under 750px (stacked layout, `--countdown-font-size-mobile`), scrolling track and keyframes, then the sticky rules.
6. **`{% javascript %}`**: the `CountdownBanner` class, below.
7. **`{% schema %}`**: settings grouped under Schedule, Content, Timer and Style. `enabled_on.groups: ["header"]`.

### JavaScript (`CountdownBanner`)

| Method | Job |
|---|---|
| `connectedCallback` / `disconnectedCallback` | Read the dates, collect units, watch size and tab visibility, start ticking |
| `tick` | Decides the state (bad dates, not started, live, ended), renders, and schedules the next tick exactly when the displayed number changes |
| `render` / `setUnit` | Splits milliseconds into units and writes every copy of each unit. Hides days at 0 and seconds when turned off |
| `setState` | Shows or hides the banner (always shown in the editor), builds the marquee the first time it's visible, sets the editor note |
| `buildMarquee` | Wraps `__inner` in `.countdown-banner__track` and clones it until one half of the track is wider than the screen. The CSS slides the track left by 50% |
| `collectUnits` | Maps unit names to every matching element, including scrolling copies |
| `updateHeightVar` | Sets `--countdown-banner-height` on `<html>` (0 when hidden or not sticky) |

## Sticky behavior

Shopify wraps each section in `<div class="shopify-section countdown-banner-section">`. The sticky rule goes on that wrapper, not on `<countdown-banner>`, or the banner only sticks inside its own wrapper.

The theme's sticky header has to move down by the banner's height. The stylesheet has two theme rules that read `--countdown-banner-height`:

- **Horizon:** `.header-section:has(> #header-component[sticky])`. Also sets `#header-group` to `display: contents`, so the banner sticks to the whole page and not just the header area.
- **Dawn family:** `.shopify-section-header-sticky`.

**To support another theme:** find the element the theme makes `position: sticky` or `fixed` for its header (search its CSS for `sticky`), then add one rule in the same style:

```css
body:has(countdown-banner[data-sticky]:not([hidden])) .that-themes-sticky-header {
  top: var(--countdown-banner-height, 0px);
}
```

Check the specificity beats the theme's own `top` rule. Don't remove the existing rules.

## Common changes

- **New setting:** add it to `{% schema %}` under the right header. Pass it to CSS as a `--countdown-*` variable or to JS as a `data-*` attribute on `<countdown-banner>`. Schema labels must be 50 characters or less (option labels too), or the push fails.
- **New text:** schema `text` setting with a default, rendered in Liquid.
- **Dismiss button:** must sit above `.countdown-banner__cover-link` (`z-index: 2`, `position: relative`) and outside `__inner`, or scrolling clones it and the cover link swallows the click.
- **Second phase** ("starts in" then "ends in"): add a second target date and switch the label in `tick`. Mirror the logic in the Liquid setup.

## Gotchas

- The timezone setting is a fixed UTC offset, not a named zone, so it doesn't follow daylight saving. The merchant picks the offset in effect on the end date.
- Shopify can cache pages, so the server-side "expired" check can lag. The JS is the source of truth and hides the banner on time.
- `buildMarquee` needs real widths, so it only runs once the banner is visible. It's skipped for `prefers-reduced-motion`.
- After changing the CSS or JS, run `python3 demo/build_demo.py` so the demo matches.

## Before you hand back

1. **Schema is valid JSON:**
   ```bash
   python3 -c "import re,json;s=open('sections/countdown-banner.liquid').read();json.loads(re.search(r'{% schema %}(.*?){% endschema %}',s,re.S).group(1));print('ok')"
   ```
2. **JS parses:**
   ```bash
   python3 -c "import re;s=open('sections/countdown-banner.liquid').read();open('/tmp/cdb.js','w').write(re.search(r'{% javascript %}(.*?){% endjavascript %}',s,re.S).group(1))" && node --check /tmp/cdb.js
   ```
3. **Theme check passes**, run inside a full theme (it needs `locales/` and `config/`): copy the section into a pulled theme and run `shopify theme check`. Only look at offenses for `countdown-banner.liquid`.
4. **Demo still works:** `python3 demo/build_demo.py`, open `demo/index.html`, try "Ends in 2 minutes" and "Scrolling on".
5. **Manual test on a dev store:** banner shows, counts down, sticks with the header right below it, link works anywhere on the bar, mobile size applies under 750px.
6. **Keep the docs in sync:** new settings or behavior go in README.md (for merchants) and this file (for agents).
