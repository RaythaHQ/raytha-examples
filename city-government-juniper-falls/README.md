# City of Juniper Falls: a self-hosted city government website

The website of the City of Juniper Falls, a fictional Hill Country city in Texas, built on Raytha 2.0.1 by an AI agent
with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). "How do I..." services, public meetings with agendas
and minutes, the mayor and council, boards and commissions, departments, public notices, news releases, a community
calendar, a site-wide alert banner, and an iCal feed of meetings and an RSS feed of notices. Every template, content
type, item, page, menu and function went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/juniper-falls-city-government](https://raytha.com/use-cases/juniper-falls-city-government)
- **Walkthrough video:** [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/da3ClwgR3UioVMR0WYZitA_juniper_falls_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![City of Juniper Falls home page](https://raytha.com/raytha/media-items/objectkey/RnTXIBV2f0uVVgQNzicnDg_juniper_01_home.webp)

## Screenshots

| | |
|---|---|
| ![How do I... services](https://raytha.com/raytha/media-items/objectkey/FK0drHCkyE213h9WvUfsOA_juniper_03_services.webp) | ![A council meeting](https://raytha.com/raytha/media-items/objectkey/76OszQISuEiNmN_qngAq-g_juniper_06_meeting.webp) |
| "How do I..." services, filtered by pay, apply, report, request and find | A council meeting with the agenda, documents and an add to calendar link |
| ![Mayor and council](https://raytha.com/raytha/media-items/objectkey/Mg5-UL7sBEiREvyQOKWQfg_juniper_07_council.webp) | ![Public notices](https://raytha.com/raytha/media-items/objectkey/NnTo_cwQcUOZsQBpKQ-Y6Q_juniper_11_notices.webp) |
| The mayor and six district council members | Public notices by kind, with an RSS feed |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/74vI1iglFkmP7Tmt_IbyEg_juniper_22_home_mobile.webp" width="240" alt="Home page on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/kcgxCS74WE6qzyzWer8XeQ_juniper_24_meetings_mobile.webp" width="240" alt="Meetings on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/3YyM2BdOeUqUa7vZhC1NMg_juniper_26_trash_mobile.webp" width="240" alt="Trash and recycling on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py). No sign-in is needed: the whole site is public.

## What's in it

- A **home page** at `/`: an alert banner, a search box with popular searches, eight top tasks, upcoming meetings, the
  latest public notices, featured and recent news, upcoming events, the council and the city at a glance.
- An **alert banner** on every page, from the `alerts` content type. Tick "Active" on an alert to show it; `/alerts`
  lists the current ones.
- **Services** at `/services`, filterable by what you want to do (`?action=pay|apply|report|request|find`). Each service
  page has the cost, time needed, department and either a link out to the city's existing system (payments, permits,
  311) or a link to the page on this site that covers it. There are no payment or registration forms.
- **Meetings** at `/meetings`, filterable by body (`?body=<board id>`) and upcoming or past (`?when=past`). Each meeting
  has the date, time and place, what is on the agenda, agenda and minutes PDFs, a video link once posted, how to comment
  and a link to the calendar feed.
- **Mayor and council** at `/council`, with a page per official (district, role, term, committees, contact).
- **Boards and commissions** at `/boards`, each with when it meets, its seats and its meetings.
- **Departments** at `/departments`: director, phone, email, address, hours, services and news.
- **Public notices** at `/notices`, filterable by kind (`?kind=hearing|bid|ordinance|election|construction`), each with
  the posted date, deadline and the notice as a PDF.
- **News releases** at `/news` (`?topic=`) and a **community calendar** at `/events` (`?category=`).
- **Trash and recycling** at `/trash-recycling` (pickup zones, what goes in each cart, holiday changes, questions),
  an **accessibility statement** at `/accessibility`, **contact** at `/contact` and **search** at `/search?q=...` across
  services, departments, meetings, notices, news and events.
- **Feeds:** `/feeds/meetings.ics` (iCalendar, `?board=<board slug>` for one board) and `/feeds/notices.rss` (RSS 2.0,
  `?kind=` for one kind of notice).

## How the alerts, meetings and feeds work

- [raytha_html_base_layout.liquid](theme/web-templates/raytha_html_base_layout.liquid) runs
  `get_content_items(ContentType="alerts", Filter="active eq 'true'", ...)` on every request and prints the banner when
  there is one. Turning an alert off is a checkbox; nothing is deployed.
- Meetings relate to their board with a relationship field and carry the agenda and minutes as attachment fields.
  [jf_list_meetings.liquid](theme/web-templates/jf_list_meetings.liquid) splits upcoming and past by comparing the start
  date with today, and filters by board.
- The two feeds are Raytha **Functions** with HTTP triggers, in [functions/](functions/). They read published items with
  the API, build iCal or RSS by hand and return them with the right content type. The organization's website URL is
  used for absolute links, so set it in the admin under Settings.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Departments, boards, officials, services, meetings, news, notices, alerts, events | Nine **content types** in [schema.json](schema.json), with **relationship fields** (department, board), **dropdowns** (service action, meeting status, news topic, notice kind, alert level, event category), **checkboxes** (top task, featured, active, free), **dates**, **numbers**, a **color**, **attachments** and **rich text**. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/): 77 items. Relationships point at their target by name; `@file:` values upload the generated portraits, news and event images and PDFs. |
| Alert banner | A query in the **base layout** for alerts with the active checkbox ticked. |
| Services, meetings, notices, news, events | **List views** with **Liquid** templates (`jf_list_*`), using query parameters for filters. |
| Service, meeting, official, board, department, notice, news and event pages | **Detail templates** (`jf_detail_*`) that pull related items with `get_content_items`. |
| Meetings calendar and notices feed | Two **Functions** (JavaScript, HTTP trigger) at `feeds/meetings.ics` and `feeds/notices.rss`. |
| Search | A **site page** with the `jf_search` template, querying six content types. |
| Home, trash and recycling, accessibility, contact | **Site pages** built from 10 custom **widget templates** (`jf_*`). |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). The footer also lists departments from the content. |

## Rebuild it

[![Deploy on Railway](https://railway.com/button.svg)](https://raytha.com/go/railway?from=examples-city-government-juniper-falls)

Deploy Raytha first, then import this kit. The button deploys a fresh Raytha with PostgreSQL on Railway; finish the setup wizard, create an API key, and run `build.sh` below against the new site.

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the artwork and documents).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd city-government-juniper-falls
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the 7 portraits, 18 news and event images and 19 agenda, minutes and notice PDFs into
`seed/art/` with [seed/make-art.py](seed/make-art.py) if they are not there yet. It then runs the shared
[scripts/build-example.sh](../scripts/build-example.sh) with this folder's [example.json](example.json): it pushes and
activates the `juniper` theme, imports the schema, binds every view to its list template, imports the seed items,
creates the five site pages, both feed functions and both menus, then runs `raytha check`. You can run it again:
everything is created or updated in place, and seed content only goes into content types that are still empty.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order and detail templates |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `juniper` theme: `jf_*` web and widget templates, the base layout, login layout and page, 404 |
| [seed/](seed/) | The nine content types as JSON Lines, plus [make-art.py](seed/make-art.py) and its spec |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [functions/](functions/) | The iCal and RSS feed functions and `functions.json` (name, trigger, route) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- The City of Juniper Falls, its officials, departments and notices are fictional. Email addresses use
  `juniperfalls.example`, phone numbers use the 555 area code and links to payment and permit systems point at `.example` hosts.
  The portraits, images and documents are generated, so everything is license-free.
- Fonts: Public Sans for text and Source Serif 4 for headings, from Google Fonts. Bootstrap Icons load from jsDelivr.
- The accessibility statement is sample text for a fictional city. The markup follows common practice (skip link,
  landmarks, one `h1` per page, visible focus, labelled filters, alt text), but the site has not been audited.
- Dropdown and checkbox values are objects in Liquid; capture them into a string first. Checkboxes render `True`, and
  checkbox filters compare to `'true'` (`Filter="active eq 'true'"`).
