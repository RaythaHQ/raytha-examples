# Kestrel Valley Credit Union: a self-hosted credit union website

The public website of Kestrel Valley Credit Union, a fictional member-owned credit union, built on Raytha 2.0.1 by an
AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Rates with an effective date, accounts and
loans, branches and ATMs on a map, financial education, a security center with fraud alerts and a site-wide scam
warning, the board and annual reports, a loan payment calculator, and a members-only area for annual meeting documents.
Every template, content type, item, page, menu, user group and function went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/kestrel-valley-credit-union](https://raytha.com/use-cases/kestrel-valley-credit-union)
- **Walkthrough video:** [MP4, 37 s](https://raytha.com/raytha/media-items/objectkey/FDJGdH327UmgR7DKsRJCzg_kestrel_valley_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Kestrel Valley Credit Union home page](https://raytha.com/raytha/media-items/objectkey/TNQPQmxioUSa_RRpZShlyQ_kestrel_01_home.webp)

## Screenshots

| | |
|---|---|
| ![Rates](https://raytha.com/raytha/media-items/objectkey/w5U39n9inkyl_pLsO1tvtg_kestrel_03_rates.webp) | ![Branches and ATMs](https://raytha.com/raytha/media-items/objectkey/kYPKi8Cf1UezWoGgEbdJ6w_kestrel_06_locations.webp) |
| Dividend and loan rates in five tables, with the effective date and a JSON feed | Branches and ATMs on a drawn map of the valley |
| ![Security center](https://raytha.com/raytha/media-items/objectkey/59wKw9_pNkSpwf60CAaB5A_kestrel_10_security.webp) | ![Member area](https://raytha.com/raytha/media-items/objectkey/5APU3NEEd0qRFdSXniALdQ_kestrel_16_members.webp) |
| The security center, with current fraud alerts and an RSS feed | The member area, signed in, with annual meeting documents |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/YTPlob_4Zk-7KESTRgHF3A_kestrel_23_home_mobile.webp" width="240" alt="Home page on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/t2qgQUwz0ES80fIAoslqtQ_kestrel_25_rates_mobile.webp" width="240" alt="Rates on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/HFaNLQGoPk6GHAvZkhja3Q_kestrel_26_locations_mobile.webp" width="240" alt="Locations on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py) (the member area shots need a signed-in member:
set `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`).

## What's in it

- A **home page** at `/`: today's rates, the tasks members come to do, featured accounts and loans, what member
  ownership means, learning and security articles, a map of branches, news and the annual meeting.
- A **scam warning banner** on every page while a fraud alert is active, from the `alerts` content type.
- **Rates** at `/rates`, in five tables (savings and checking, certificates, auto, home, personal loans and cards), each
  rate with its term, minimum, APY or APR, an "as low as" flag and the effective date.
- **Accounts and loans** at `/products`, filterable by type (`?category=checking|savings|certificates|auto|home|personal|business`).
  Each product page has its highlights, its current rates pulled from the rates table and questions and answers.
  To open an account or apply, members are pointed to a branch, a phone number or online banking; there are no
  application, payment or registration forms.
- **Locations** at `/locations`: four branches and three ATMs on a drawn map, with lobby and drive-thru hours and
  services, and a page per location.
- **Learn** at `/learn`, articles by topic (`?topic=budgeting|credit|home|fraud|saving|youth`).
- **Security** at `/security`: current fraud alerts, how to report fraud, and a page per alert.
- **About** at `/about` (with how to become a member), the **board** at `/board`, **news** at `/news` (`?category=`),
  and **reports and documents** at `/documents`.
- A **member area** at `/members` and members-only documents, for members of the `members` user group.
- A **loan payment calculator** at `/loan-calculator` (runs in the browser), an **accessibility statement**, **disclosures**,
  **contact** and **search** at `/search?q=...` across products, rates, locations, articles, news and documents.
- **Feeds:** `/feeds/rates.json` (all rates as JSON, `?table=` for one table) and `/feeds/security.rss` (RSS 2.0,
  `?level=` for one alert level).

## How the rates, alerts and member area work

- Each rate is an item in `rates` with a relationship field to its product. The rates page, the home page rate board
  and each product page read the same items with `get_content_items`, so a rate change is one edit.
- [raytha_html_base_layout.liquid](theme/web-templates/raytha_html_base_layout.liquid) runs
  `get_content_items(ContentType="alerts", Filter="active eq 'true'", ...)` on every request and prints the scam warning
  when there is one. Turning it off is a checkbox.
- [kv_members.liquid](theme/web-templates/kv_members.liquid) and
  [kv_detail_documents.liquid](theme/web-templates/kv_detail_documents.liquid) loop over `CurrentUser.UserGroups`. Members
  (and admins) see the documents; everyone else sees a sign-in prompt. Members-only documents still appear in lists and
  search, marked "Members", but their page shows the sign-in prompt instead of the file.
- The two feeds are Raytha **Functions** with HTTP triggers, in [functions/](functions/). The organization's website URL
  is used for absolute links, so set it in the admin under Settings.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Branches, products, rates, articles, news, alerts, board members, documents | Eight **content types** in [schema.json](schema.json), with a **relationship field** (rate to product), **dropdowns**, **checkboxes** (featured, active, members only, as low as), **numbers** (rates, map positions), **dates**, **attachments** and **rich text**. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/): 70 items. Rates point at their product by name; `@file:` values upload the generated images and PDFs. |
| Scam warning banner | A query in the **base layout** for alerts with the active checkbox ticked. |
| Rates, products, locations, articles, alerts, board, news, documents | **List views** with **Liquid** templates (`kv_list_*`). |
| Detail pages | **Detail templates** (`kv_detail_*`) that pull related items with `get_content_items`. |
| Member area | A **user group** (`members`) and templates that check `CurrentUser.UserGroups`. |
| Rates feed and security alerts feed | Two **Functions** (JavaScript, HTTP trigger) at `feeds/rates.json` and `feeds/security.rss`. |
| Search | A **site page** with the `kv_search` template. |
| Home, about, contact, accessibility, disclosures, loan calculator | **Site pages** built from 10 custom **widget templates** (`kv_*`). |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). |

## Rebuild it

[![Deploy on Railway](https://railway.com/button.svg)](https://raytha.com/go/railway?from=examples-credit-union-kestrel-valley)

Deploy Raytha first, then import this kit. The button deploys a fresh Raytha with PostgreSQL on Railway; finish the setup wizard, create an API key, and run `build.sh` below against the new site.

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the artwork and documents).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd credit-union-kestrel-valley
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the logo, illustrations, portraits and PDFs into `seed/art/` with
[seed/make-art.py](seed/make-art.py) if they are not there yet. It then runs the shared
[scripts/build-example.sh](../scripts/build-example.sh) with this folder's [example.json](example.json): it pushes and
activates the `kestrel` theme, imports the schema, binds every view to its list template, imports the seed items,
creates the `members` user group, the eight site pages, both feed functions and both menus, then runs `raytha check`.
You can run it again: everything is created or updated in place, and seed content only goes into content types that
are still empty.

To see the member area, create a public user in the admin, add them to `members`, and sign in at `/account/login`.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order, detail templates and user groups |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `kestrel` theme: `kv_*` web and widget templates, the base layout, login layout and page, 404 |
| [seed/](seed/) | The eight content types as JSON Lines, plus [make-art.py](seed/make-art.py) and its spec |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [functions/](functions/) | The rates JSON and security RSS functions and `functions.json` (name, trigger, route) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Kestrel Valley Credit Union is fictional. It is not a real financial institution, the rates are invented and are not
  an offer of credit, and no deposits are insured. The site says so in a top bar and the footer, where a real credit
  union would show its NCUA and Equal Housing Opportunity notices. Email addresses use `kestrelvalley.example`, phone
  numbers use 555, the routing number is all zeros, and the "Online banking" and map links point at `.example` hosts.
- The member sign-in is a Raytha website account, not online banking. Online banking stays with your core or digital
  banking provider.
- The member area hides members-only documents in the templates. The files themselves are served from media URLs that
  are not access-controlled, so do not use this pattern for confidential documents without protecting storage too.
- Fonts: Figtree for text and Source Serif 4 for headings, from Google Fonts. Bootstrap Icons load from jsDelivr.
- The accessibility statement and disclosures are sample text. The markup follows common practice (skip link,
  landmarks, one `h1` per page, visible focus, labelled controls, table headers, alt text), but the site has not been audited.
- Dropdown and checkbox values are objects in Liquid; capture them into a string first. Checkboxes render `True`, and
  checkbox filters compare to `'true'` (`Filter="active eq 'true'"`).
