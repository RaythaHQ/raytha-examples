# Brightwell Medical Supply: a home medical equipment provider's website

The corporate website for Brightwell Medical Supply, a fictional durable medical equipment (DME) provider, built on
Raytha 2.0.1 by an AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content
type, product, guide, page and menu went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 35 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/brightwell-medical-supply](https://raytha.com/use-cases/brightwell-medical-supply)
- **Walkthrough video:** [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/9pdCqxo6rU2K_eFnS0krAw_brightwell_medical_supply_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Brightwell Medical Supply home page](https://raytha.com/raytha/media-items/objectkey/obNNiviyJkemqFMYRWLrrw_brightwell_dme_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Product page](https://raytha.com/raytha/media-items/objectkey/SdaASxPg90OVY8ou7u7kZQ_brightwell_dme_05_product.webp) | ![Equipment catalog](https://raytha.com/raytha/media-items/objectkey/KgpkNAyfjkCr346Lq1XbGw_brightwell_dme_04_catalog.webp) |
| A product page with the HCPCS code, specifications and coverage | The catalog, filtered by category, rent or buy, and coverage |
| ![How to order](https://raytha.com/raytha/media-items/objectkey/kTkpcam4a0-PDXkMM8JNHg_brightwell_dme_07_how_to_order.webp) | ![Locations](https://raytha.com/raytha/media-items/objectkey/yTTXDSXpbkWxI1htEcsHXg_brightwell_dme_10_locations.webp) |
| How to order, with the prescriber fax number | Locations with a map and today's hours |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/iqHcj2Zo2EqiuLj-H_XE3g_brightwell_dme_12_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/5x86ZGnNd0GIPK53m2DfWQ_brightwell_dme_13_product_mobile.webp" width="240" alt="A product on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with a search box, equipment categories with live product counts, the most ordered equipment, a
  four-step "how ordering works" strip, the insurance plans accepted, a map of locations, patient guides and
  common questions.
- An equipment catalog at `/products` you can search by name or HCPCS billing code and filter by category, by
  rent or buy, and by how it is usually paid for (Medicare, private insurance or self-pay). Every filter is a
  plain link.
- Product pages with the HCPCS code, rental or purchase options, whether a prescription is needed, a
  specifications table, what comes in the box, an explanation of coverage and cost, guides and related equipment.
- A page for each of the six categories at `/equipment/...`, with its products and guides.
- Patient resources at `/resources`: plain-language guides on ordering, Medicare and billing, and equipment care.
- An FAQ page grouped by topic, with a box that filters the questions as you type.
- Location pages with a map, services, parking and opening hours, with today's hours highlighted.
- How to order and Contact pages that explain what a doctor needs to send and who to call.
- No payment or order forms. Product pages point people to the order desk by phone or email, and prescribers to
  a fax number.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Categories, products, guides, questions, locations | Five **content types** in [schema.json](schema.json). Products have a **relationship field** to their category, **dropdowns** for rent or buy and for coverage, a **checkbox** for prescription required, an **attachment** illustration and **long text** fields for specifications and what's included. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/). Products point at their category by title; `@file:` values upload the SVG illustrations. |
| Equipment catalog | A **list view** at `/products`. The **Liquid** template reads `?category=`, `?acquire=`, `?coverage=` and `?q=`, checks each against a known list and builds a filter for `get_content_items`. |
| Specifications table | Each line of the specifications field is `Label: value`. The product template splits the lines into a table. |
| Coverage explanation | The product template picks the explanation that matches the coverage dropdown, so editors only choose an option. |
| FAQ | A content type with a topic dropdown. The list view groups by topic, and a few lines of script filter as you type. Pages show questions from one topic through a widget setting. |
| Locations and hours | A content type with an address, phone, hours and a map position. Templates place the pins on an illustrated map; a short script highlights today's hours. |
| Home, How to order, Contact | **Site pages** built from 12 custom **widget templates**. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). The footer also lists the categories from the content. |

## Rebuild it

[![Deploy on Railway](https://railway.com/button.svg)](https://raytha.com/go/railway?from=examples-medical-supply-brightwell)

Deploy Raytha first, then import this kit. The button deploys a fresh Raytha with PostgreSQL on Railway; finish the setup wizard, create an API key, and run `build.sh` below against the new site.

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, and `jq`.
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd medical-supply-brightwell
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` runs the shared [scripts/build-example.sh](../scripts/build-example.sh) with this folder's
[example.json](example.json). It pushes and activates the `brightwell` theme, imports the schema, binds every view
to its list template, imports the seed content with its illustrations, creates the three site pages and both
menus, then runs `raytha check`. You can run it again: everything is created or updated in place, and seed content
only goes into content types that are still empty.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates for the shared build script |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `brightwell` theme: the `bw_*` web and widget templates plus the restyled base layout and 404 page |
| [seed/](seed/) | Categories, products, guides, FAQs and locations as JSON Lines, plus the SVG illustrations and [make-art.py](seed/make-art.py) that draws them |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Brightwell Medical Supply, its locations, phone numbers and products are fictional. Phone numbers use the 555
  range and email links use `example.com`. Prices, HCPCS codes and coverage notes are illustrative, not billing
  advice.
- Fonts: Plus Jakarta Sans for text and headings and IBM Plex Mono for billing codes, from Google Fonts. Bootstrap
  Icons load from jsDelivr.
- The map is an illustration with pins placed from each location's map position, so it needs no map service or key.
- Raytha's Liquid does not support `{% include %}` of other web templates, so the product card markup is repeated in
  the templates that list products.
