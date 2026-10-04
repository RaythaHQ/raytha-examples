# Groundwork: a climate tech job board

A remote job board for climate tech, built on Raytha 2.0.1 by an AI agent with the
[`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type, job, company, page, menu and
function went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 15 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/groundwork-job-board](https://raytha.com/use-cases/groundwork-job-board)

![Groundwork home page](https://raytha.com/raytha/media-items/objectkey/6t-jZhocvEqtk0SbE02k_A_groundwork_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Job list filtered by category, location type and salary](https://raytha.com/raytha/media-items/objectkey/p7xjsbIEx0yMYOC3D1bSxA_groundwork_04_jobs_filtered.webp) | ![Job page](https://raytha.com/raytha/media-items/objectkey/z85eWxVh3UGWYriZdmQb4g_groundwork_06_job_detail.webp) |
| Jobs filtered by category, location type and salary | Job page with Apply link and JobPosting data |
| ![Company directory](https://raytha.com/raytha/media-items/objectkey/4PhN07UE5USi5qwvSiSoUQ_groundwork_07_companies.webp) | ![Members' Hub](https://raytha.com/raytha/media-items/objectkey/3OuQb2b_G0K1r7DeDXNJVQ_groundwork_12_hub_signed_in.webp) |
| Company directory | Members-only Hub with live salary benchmarks |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/EOcb9vEnqkKbppYthaGj3g_groundwork_13_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/Bhoc7BHPVUqSFQnTyM1VgA_groundwork_14_jobs_mobile.webp" width="240" alt="Job filters on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/uPhoqhTa_02wSPquKtEg0w_groundwork_15_job_mobile.webp" width="240" alt="Job page on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with a search hero over a stack of featured roles, live stats, featured jobs, categories with live
  counts, the companies hiring, and a call to the Members' Hub.
- A job list at `/jobs` that filters by category, location type, minimum top-of-band salary and skill, searches
  titles, summaries, locations and skills (and shows matching companies), and sorts by date or salary. Every filter is a shareable URL.
- A remote-only view at `/jobs/remote` with the same filters.
- A page per job with salary, location, seniority and employment type, an **Apply** button that goes straight to
  the employer's site, a company card and similar roles. Each page carries **JobPosting** structured data for
  Google for Jobs.
- A company directory and a profile page per company that lists every open role.
- **RSS** and **JSON Feed** versions of the board, with the same filters as the list.
- A members-only **Members' Hub** for the `members` user group: salary benchmarks by category and curated saved
  searches, all calculated live from the listings.
- An About page with an FAQ, plus restyled sign-in, 403, 404 and 500 pages.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Jobs and companies | Two **content types** in [schema.json](schema.json). Jobs use a **relationship field** to their company, **dropdowns** (category, location type, currency, employment type, seniority), a **multiple select** for skills, **number** fields for the salary band, **dates** and a **checkbox** for featured. |
| Seed content with logos | `raytha content import` from JSON Lines in [seed/](seed/). Each job points at its company by name, and `@file:` uploads each SVG logo to the media library. |
| Filterable, searchable job list | A **list view** at `/jobs`. The **Liquid** template reads `?q=`, `?category=`, `?type=`, `?salary=`, `?tag=` and `?sort=`, validates them against known values and builds a filter for `get_content_items`, such as `contains(tags,'python') and salary_max ge 130000`. |
| Remote only | A second view at `/jobs/remote` with a saved filter (`location_type eq remote`), using the same template. |
| Company pages that list their jobs | The detail template queries `company eq '<id>'`. |
| Google for Jobs | The job detail template writes a `JobPosting` JSON-LD block with salary, dates, location or remote eligibility, and the hiring organization. |
| Feeds | Two **Raytha Functions** in [functions/](functions/): `/feeds/jobs.rss` and `/feeds/jobs.json` (JSON Feed 1.1), both accepting `?category=`, `?type=` and `?tag=`. |
| Home and About | **Site pages** built from 10 custom **widget templates**, each with a settings form an editor can use in the admin. Stats, featured jobs, category counts and company tiles are queried live. |
| Members' Hub | A **user group**. The page template checks `CurrentUser.UserGroups`, so non-members never receive the members-only HTML. |
| Navigation | Two **menus**, `mainmenu` and `footer`, in [menus/](menus/). |

## Rebuild it

You need a Raytha 2.x site you can wipe (a fresh install is best), an admin API key, the `raytha` CLI, and `jq`.

1. **Run Raytha.** One-click on [Railway](https://railway.com/deploy/raytha-cms?referralCode=RU52It&utm_medium=integration&utm_source=template&utm_campaign=generic),
   or locally with Docker:

   ```bash
   git clone https://github.com/RaythaHQ/raytha.git && cd raytha
   cp .env.example .env && docker compose --env-file .env up
   ```

   Open the site, finish the setup wizard, and set the **website URL** to the address you'll browse it at.
   The feeds and the JobPosting data build absolute links from it.

2. **Create an API key.** In the admin: Settings > Administrators > your account > API keys.

3. **Install the CLI** and check the connection:

   ```bash
   curl -fsSL https://raytha.com/cli/install.sh | sh        # Windows: irm https://raytha.com/cli/install.ps1 | iex
   export RAYTHA_URL=http://localhost:5001                  # your site
   export RAYTHA_API_KEY=...                                # the key from step 2
   raytha doctor
   ```

4. **Preview, then build:**

   ```bash
   cd job-board-groundwork
   DRY_RUN=1 bash build.sh     # previews the theme push and schema import, changes nothing
   bash build.sh
   ```

   The script pushes and activates the `groundwork` theme, imports the schema, binds every view to its list
   template, imports the seed content, cleans up item URLs, creates the `members` group, the three site pages, the
   two feed functions and both menus, then runs `raytha check`. You can run it again: everything is created or
   updated in place, and seed content only goes into content types that are still empty.

   By default it makes the main and footer menus match this example and removes other items (the default Home and
   Posts links on a fresh install). Set `PRUNE_MENUS=0` to keep them.

5. **See the Members' Hub.** Create a public user in the `members` group (admin: Users), sign in, and open `/hub`.

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Idempotent rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `groundwork` theme (`raytha theme push`): `theme.json`, the custom `gw_*` web and widget templates, and the built-in templates it restyles (base layout, sign-in, 403, 404, 500). Built-ins it doesn't change are created by Raytha with their defaults. |
| [functions/](functions/) | The RSS and JSON Feed functions plus `functions.json` (names, triggers, routes) |
| [seed/](seed/) | Seed content as JSON Lines, the SVG company logos, and the script that draws them |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |

## Notes

- Everything is fictional: the companies, jobs, salaries and people. Websites and apply links use `example.com`.
- Company logos are flat SVGs drawn by [seed/make-logos.py](seed/make-logos.py). No photos, nothing third-party.
- Fonts: Fraunces for display type, DM Sans for text and IBM Plex Mono for labels, all from Google Fonts. Bootstrap
  Icons load from jsDelivr, so the theme has no media files and moves between instances cleanly.
- Job seekers never need an account. There are no registration, payment or job-posting forms; every Apply button
  links to the employer's own page.
