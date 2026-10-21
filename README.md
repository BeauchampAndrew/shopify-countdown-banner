# Shopify Countdown Banner

A sticky sale banner for Shopify with a live countdown. Built for BFCM, works for any sale with a deadline.

It's one file. No app, no monthly fee, no code knowledge needed to install it.

**Using Claude Code, Cursor or another AI coding tool?** Point it at this repo and tell it what you want, like "install this in my theme" or "add a dismiss button". [AGENTS.md](AGENTS.md) tells it how the section works and how to change it without breaking it in other themes.

## What it does

- Counts down in days, hours and minutes (seconds optional)
- Sticks to the top of the screen, with your theme's sticky header sitting right below it
- Optional scrolling text that slides the offer and countdown across the bar
- The whole banner is clickable when you add a link
- Turns itself on at the start time and hides itself at the end time
- Every visitor sees the same deadline, whatever timezone they're in
- Separate text sizes for desktop and mobile
- Everything is editable in the Shopify theme editor. No code changes needed for the next sale.

Built and tested on Shopify's **Horizon** theme. Also has built-in support for **Dawn** and Dawn-based themes, and works on any Online Store 2.0 theme (every free Shopify theme made since 2021).

## Install it (about 3 minutes, no coding)

**Tip:** do this on a copy of your theme first. In **Online Store > Themes**, click **...** next to your theme and choose **Duplicate**. Try it there, then publish the copy when you're happy.

### Step 1: Add the section file

1. Open [`sections/countdown-banner.liquid`](sections/countdown-banner.liquid) here on GitHub and click the **Copy raw file** button (the two-squares icon at the top right of the file).
2. In your Shopify admin, go to **Online Store > Themes**. Next to your theme, click **...** then **Edit code**.
3. In the file list on the left, find the **Sections** folder and click **Add a new section**.
4. Name it `countdown-banner` and pick **Liquid** if it asks.
5. Delete the starter code Shopify puts in the new file, paste in what you copied, and click **Save**.

### Step 2: Add the banner to your header

1. Go back to **Online Store > Themes** and click **Customize**.
2. In the left sidebar, find the **Header** area and click **Add section**.
3. Pick **Countdown banner**.
4. Drag it to the top of the header area so it sits above your announcement bar and header.
5. Set your dates, message and colors, then click **Save**.

### Using Shopify CLI instead

Copy `sections/countdown-banner.liquid` into your theme's `sections/` folder, then push to an unpublished theme to try it:

```bash
shopify theme push --unpublished --theme "Countdown banner test"
```

## Settings

| Setting | What it does |
| --- | --- |
| Start showing | When the banner appears. Format: `YYYY-MM-DD HH:MM`, 24-hour clock |
| Sale ends | The countdown target. The banner hides at this time. |
| Timezone | The timezone your start and end times are in. Pick the version (standard or daylight) that's in effect on the end date. For BFCM in the US that's standard time (EST, CST, PST). |
| Message | The offer. Supports bold, italic and links. |
| Timer label | Text before the numbers, like "Ends in" |
| Link / Button label | Add a link and the whole banner becomes clickable, scrolling or not. Add a button label too if you want a button shown as a visual cue. |
| Show seconds | Off by default |
| Days / Hrs / Min / Sec labels | Change these to translate the banner or use different wording |
| Stick to top of screen | On by default |
| Scrolling text / Scroll speed | Slides the message and countdown across the bar in a loop instead of sitting still. Pauses on hover. Turns itself off for shoppers who have reduced motion set on their device. |
| Text size (desktop) / Text size (mobile) | Separate sizes so you can go big on desktop without the banner wrapping into a tall block on phones. Mobile is anything under 750px wide. |
| Background, Text, Vertical padding | Look and feel |

A few behaviors to know:

- The days unit hides itself on the last day, so the final 24 hours read "Ends in 05 Hrs 12 Min".
- Without seconds, minutes round up, so the banner never says "0 Min" while time is still left.
- In the theme editor the banner always stays visible so you can edit it. A black note underneath tells you when customers can't see it (not started yet, or already ended).

## Preview without a store

Open `demo/index.html` in your browser. It uses the same CSS and JS as the section, and has buttons to jump to the last 2 minutes (so you can watch it hide itself) and to turn scrolling on and off.

Changed the section? Run `python3 demo/build_demo.py` to copy your new CSS and JS into the demo.

## Customize it with Claude

The code is commented and lives in one file, so it's easy to change with [Claude Code](https://claude.com/claude-code), or by pasting the file into Claude and pasting the answer back into your theme's code editor. Some prompts that work:

**Change the look**
> Make the countdown numbers look like flip-clock tiles: white boxes with dark text, one box per unit.

> Use my theme's heading font for the banner instead of the default body font.

**Change the behavior**
> Add an X button that lets shoppers dismiss the banner. Remember the choice for the rest of their visit.

> Show a different message in the last 24 hours: "LAST CHANCE: 25% OFF ENDS TONIGHT".

> When the sale ends, swap to a "Sale extended" message for 24 hours instead of hiding.

> Only show the banner on the home page and collection pages.

**Add features**
> Add an optional discount code to the banner with a click-to-copy button.

> Add a second phase: count down to Black Friday first ("Sale starts in"), then count down to Cyber Monday ("Sale ends in").

**Fit a different theme**
> I installed countdown-banner on the [theme name] theme. The sticky header covers the banner when I scroll. Fix the CSS in sections/countdown-banner.liquid so the header sits below the banner.

Claude does best when you say which theme you're on and describe exactly what you see. A screenshot helps.

### How the sticky part works (for Claude or a developer)

The banner's JS sets a CSS variable, `--countdown-banner-height`, on the page. The CSS in the section uses it to push the theme's sticky header down by that amount. There are rules for Horizon (`.header-section`) and Dawn (`.shopify-section-header-sticky`). For another theme, add one rule that sets `top: var(--countdown-banner-height)` on that theme's sticky header element.

## License

MIT. Use it on your store or your clients' stores, change it, ship it.
