# Meridian Hub: a self-hosted company intranet and employee portal

The intranet of Meridian Waterworks, a fictional maker of water meters, built on Raytha 2.0.1 by an AI agent with
the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). News and announcements, an employee directory,
departments, a policy handbook, events, a resource library, IT help and system status, all behind Raytha's sign-in
and user groups. Every template, content type, item, page, menu and user group went in through the CLI. Nobody
opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 90 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/meridian-hub-intranet](https://raytha.com/use-cases/meridian-hub-intranet)
- **Walkthrough video:** [MP4, 35 s](https://raytha.com/raytha/media-items/objectkey/u-mtvWpRi0yFKzFIb7eJiw_meridian_hub_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Meridian Hub dashboard](https://raytha.com/raytha/media-items/objectkey/5ivXGVtPpEGX7wD-c3mrlg_meridian_02_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Sign-in page](https://raytha.com/raytha/media-items/objectkey/Xp5D9sDRCEWATnzrWhsINg_meridian_01_sign_in_gate.webp) | ![Employee directory](https://raytha.com/raytha/media-items/objectkey/ChOaUGr3KEOWRanVcpBVbg_meridian_06_people_directory.webp) |
| Anyone who is not signed in gets the sign-in page, on every URL | The employee directory, searchable by name, role or skill and filterable by department and office |
| ![Handbook](https://raytha.com/raytha/media-items/objectkey/AI2SNv8DuU2JpxN2KUaylQ_meridian_09_handbook.webp) | ![Managers-only policy](https://raytha.com/raytha/media-items/objectkey/80j-xt-WJkCUo6Wxh6ejkQ_meridian_11_managers_only.webp) |
| The handbook by section, with acknowledgements and managers-only policies marked | A managers-only policy, as an employee outside the managers group sees it |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/MTBh7nfBqEemTqaJowkkEw_meridian_17_home_mobile.webp" width="240" alt="Dashboard on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/yrRyYaEPekqfWmfhSBRxWw_meridian_18_people_mobile.webp" width="240" alt="Directory on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/BYn7Hgnrpk6HXm_rWcpa2Q_meridian_19_gate_mobile.webp" width="240" alt="Sign-in page on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py) (most shots need a signed-in employee: set
`SITE_USER_EMAIL` and `SITE_USER_PASSWORD`).

## What's in it

- **Sign-in for the whole site.** Every URL shows a sign-in landing page until you sign in as a member of the
  `employees` group (or an admin). The restyled login page has no sign-up link, because the company creates accounts.
- A **dashboard** at `/`: a greeting with the user's first name, quick links, the pinned announcement, latest news, a
  to-do list (announcements marked "action needed" and policies to acknowledge), upcoming events, new starters,
  popular IT help and system status.
- **News** at `/news`, filterable by category (`?cat=company|people|it|operations|product|facilities`),
  with pinned and "action needed" flags, department and author.
- An **employee directory** at `/people` with `?q=` (name, role or skill), `?dept=<department-slug>` and
  `?office=austin|tulsa|denver|rotterdam|remote`, and a profile page per person.
- **Departments** at `/departments`, each with its mission, headcount, location, chat channel, team, the policies it
  owns, news and documents.
- A **handbook** at `/handbook`: 16 policies grouped by section, with owner, version, effective and review dates.
  Three ask the reader to acknowledge them, and two are for the `managers` group only.
- **Events** at `/events`, grouped by month, each with an "add to calendar" `.ics` file made in the browser.
- A **resource library** at `/resources`: templates, forms and guides with their format and a generated PDF, two of
  them managers-only.
- **IT help** at `/it-help` with topics and a search box, and **system status** at `/status`. The top bar shows how
  many systems need attention on every page.
- **Search** at `/search?q=...` across people, news, policies, resources and IT help.
- **About Meridian** at `/company`: values, offices and the leadership team.

## How sign-in, user groups and managers-only pages work

- [raytha_html_base_layout.liquid](theme/web-templates/raytha_html_base_layout.liquid) loops over
  `CurrentUser.UserGroups` and sets `is_emp` (employees group or `CurrentUser.IsAdmin`) and `is_mgr`. It captures
  `{% renderbody %}` and only outputs it for employees. Everyone else gets the sign-in landing, so page content is
  never sent to visitors. The login pages set a `gate_open` flag so they can render for signed-out users.
- Policies and resources have a `managers_only` checkbox. [mh_detail_policies.liquid](theme/web-templates/mh_detail_policies.liquid)
  and [mh_detail_resources.liquid](theme/web-templates/mh_detail_resources.liquid) check for the `managers` group and
  show a short note instead of the content to everyone else. List pages mark those items with a lock.
- `build.sh` creates the `employees` and `managers` groups (from [example.json](example.json)). It does not create
  users: add your own in the admin under Users and put them in the groups. A people manager belongs to both.
- Policy acknowledgements and the to-do count are stored in the browser (`localStorage`, key `mh:ack`) for this demo.
  To record them per user, save each confirmation through a Raytha Function.
- Raytha supports SAML and JWT single sign-on. Turn one on in the admin and users who sign in through it can be put in
  the same groups; the templates don't change.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Departments, people, announcements, policies, events, resources, IT help, systems | Eight **content types** in [schema.json](schema.json), with **relationship fields** (department, author, owner, host), **dropdowns** (office, category, section, event type and format, resource kind, help topic, system status), **checkboxes** (pinned, action needed, acknowledge, managers only, popular, leadership), **dates**, **numbers**, a **color**, **attachments** and **rich text**. |
| Seed content | `raytha content import` from JSON Lines in [seed/](seed/): 110 items. Relationships point at their target by name; `@file:` values upload the generated portraits, covers and PDFs. |
| Sign-in for the whole site | Raytha **login** and **user groups**, checked in the **base layout**; restyled login layout and login page. |
| Managers-only policies and documents | A checkbox plus a **user group** check in the detail templates. |
| Directory, news, handbook, events, resources, IT help, status | **List views** with **Liquid** templates (`mh_list_*`), using query parameters for filters. |
| Profile, department, policy, event, resource and article pages | **Detail templates** (`mh_detail_*`) that pull related items with `get_content_items`. |
| Search | A **site page** with the `mh_search` template, querying five content types with `contains()` filters. |
| Dashboard and About | **Site pages** built from 13 custom **widget templates** (`mh_*`). |
| Navigation | Two **menus**, `mainmenu` (the sidebar) and `quicklinks`, in [menus/](menus/). |

## Rebuild it

[![Deploy on Railway](https://railway.com/button.svg)](https://raytha.com/go/railway?from=examples-intranet-meridian-hub)

Deploy Raytha first, then import this kit. The button deploys a fresh Raytha with PostgreSQL on Railway; finish the setup wizard, create an API key, and run `build.sh` below against the new site.

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, `jq` and
`python3` (to draw the artwork).
Follow steps 1 to 3 of the [Quickstart](../README.md#quickstart) to run Raytha, create a key and install the CLI, then:

```bash
cd intranet-meridian-hub
DRY_RUN=1 bash build.sh     # previews the schema import, changes nothing
bash build.sh
```

`build.sh` first draws the 24 portraits, 12 news covers and 12 PDF documents into `seed/art/` with
[seed/make-art.py](seed/make-art.py) if they are not there yet. It then runs the shared
[scripts/build-example.sh](../scripts/build-example.sh) with this folder's [example.json](example.json): it pushes and
activates the `meridian` theme, imports the schema, binds every view to its list template, imports the seed items,
creates the `employees` and `managers` user groups, the three site pages and both menus, then runs `raytha check`.
You can run it again: everything is created or updated in place, and seed content only goes into content types that
are still empty.

Then create a user in the admin, add them to `employees` (and `managers` to see the managers-only pages), and sign in.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [example.json](example.json) | Theme name, import order, detail templates and user groups |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `meridian` theme: `mh_*` web and widget templates, the base layout, login layout and page, 403 and 404 |
| [seed/](seed/) | The eight content types as JSON Lines, plus [make-art.py](seed/make-art.py) and its spec |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Sidebar and quick links menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |
| [walkthrough.json](walkthrough.json) | The shot list for [`scripts/make-walkthrough.py`](../scripts/make-walkthrough.md) |

## Notes

- Meridian Waterworks, its people and its policies are fictional. Email addresses use `meridian.example`. The
  portraits, covers and documents are generated, so every image is license-free.
- Fonts: Geist for text and Geist Mono for labels, from Google Fonts. Bootstrap Icons load from jsDelivr; the base
  layout also declares the icon font itself, because the CSS bundled with Raytha's default theme has no `@font-face`.
- The gate captures `{% renderbody %}` into a variable first and decides afterwards whether to print it.
- Raytha's Liquid does not allow parentheses in conditions, so the directory filters combine with an `ok` flag.
- Dropdown and checkbox values are objects in Liquid; capture them into a string first. Checkboxes render `True`, and
  checkbox filters compare to `'true'` (`Filter="pinned eq 'true'"`).
