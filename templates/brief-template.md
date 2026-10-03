# Brief: <site name>

<!-- One paragraph: what the site is, who it is for, and what a visitor should be able to do. -->
Build a website for **<organization or project>**, <one-line description>. Build it entirely on a Raytha instance
with the `raytha` CLI. No clicking around the admin.

## Look and feel

- Overall direction: <e.g. warm editorial, dark premium tech, playful, minimal>
- Type: <font pairing, or "pick a Google Fonts pairing that fits">
- Color: <palette, or brand colors as hex>
- Signature elements: <hero style, motion, imagery, cards, illustrations>
- Must look good on a phone as well as a desktop.
- Images: generated SVGs or images you may redistribute only.

## Content model

<!-- One bullet per content type: fields and how many seed items. -->
- **<Type>** (about <n>): <field>, <field>, <relationship to another type>, <dropdown: a|b|c>
- **<Type>** (about <n>): ...

## Pages

- Home: <sections>
- <List page>: <filters, sort, layout>
- <Detail page>: <what it shows, related content>
- <Other pages>: <about, contact, FAQ, ...>

## Functionality

- <Search, gated members area (user group), feeds, downloads, forms handled elsewhere, ...>
- Navigation menus: <main, footer>
- Optional Raytha Functions: <e.g. JSON feed, calendar file, sitemap>

## Out of scope

- <Anything the agent must not build, e.g. payments, user registration, real personal data>

## Done means

- `raytha check` passes with no broken routes.
- Screenshots on desktop (1440px) and mobile (390px).
- The schema, theme, functions, seed content, pages and menus exported as files, with a `build.sh` that rebuilds
  the site into a fresh instance.
