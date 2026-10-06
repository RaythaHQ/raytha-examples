# Raytha examples

Complete websites built on [Raytha](https://github.com/RaythaHQ/raytha) by an AI agent with the
[`raytha` CLI](https://github.com/RaythaHQ/raytha-cli), each one with the brief it started from and everything
you need to rebuild it on your own Raytha instance with one command.

Every example folder has:

- **`brief.md`**: the brief the agent got. Nothing else went in.
- **`build.sh`**: rebuilds the whole site into a Raytha instance. Idempotent, configured from `RAYTHA_URL` and `RAYTHA_API_KEY`.
- **The site as files**: `schema.json` (content model), `theme/` (Liquid templates and widgets), `functions/`,
  `seed/` (content and images), `pages/`, `menus/`.
- **`README.md`**: screenshots, the Raytha feature behind each part of the site, and step-by-step rebuild notes.

These examples go with the weekly [use cases on raytha.com](https://raytha.com/use-cases).

## Gallery

| Example | What it shows |
|---------|---------------|
| [<img src="https://raytha.com/raytha/media-items/objectkey/uzXF7ioaKU218L0jeugYbQ_horizon_summit_01_home_hero.webp" width="360" alt="Horizon Summit 2027">](conference-horizon-summit/) | **[Horizon Summit 2027](conference-horizon-summit/)**: a conference site with a filterable agenda, speaker and session pages, a tiered sponsor wall, `.ics` downloads from a Raytha Function, site search, and a members-only Attendee Hub. 5 content types, 14 widgets, 3 functions. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/6t-jZhocvEqtk0SbE02k_A_groundwork_01_home_hero.webp" width="360" alt="Groundwork climate tech job board">](job-board-groundwork/) | **[Groundwork](job-board-groundwork/)**: a remote job board for climate tech with listings you can filter and search by category, location type, salary and skill, company profiles, an external Apply link and JobPosting JSON-LD on every job, RSS and JSON feeds from Raytha Functions, and a members-only salary hub. 2 content types, 10 widgets, 2 functions. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/yxBjCaWwv02PaLCf2EC_gg_orbitly_help_01_home_hero.webp" width="360" alt="Orbitly help center">](help-center-orbitly/) | **[Orbitly help center](help-center-orbitly/)**: a knowledge base for a fictional SaaS product with search as you type from a Raytha Function, topics, article pages with an outline and related articles, a changelog with an RSS feed, and a status page. 3 content types, 6 widgets, 2 functions. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/AJBqKggehkCGdW2HvJrzQA_atlas_lms_01_home_hero.webp" width="360" alt="Atlas Learning course portal">](lms-portal-atlas/) | **[Atlas Learning](lms-portal-atlas/)**: a course portal with a catalog filtered by topic and level, course pages with a curriculum, free preview lessons, members-only lessons that never leave the server for visitors, and a My learning dashboard, all on Raytha's login and user groups. 3 content types, 8 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/obNNiviyJkemqFMYRWLrrw_brightwell_dme_01_home_hero.webp" width="360" alt="Brightwell Medical Supply">](medical-supply-brightwell/) | **[Brightwell Medical Supply](medical-supply-brightwell/)**: a durable medical equipment provider's website with a catalog you can search by HCPCS code and filter by category, rent or buy, and coverage, product pages with specifications, patient guides, FAQs and locations with today's hours. No payment forms. 5 content types, 12 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/ysBc0hzkM0y7qJE-PF8QPQ_halftone_awards_01_home_hero.webp" width="360" alt="Halftone Awards">](awards-halftone/) | **[Halftone Awards](awards-halftone/)**: an awards site with categories and live deadline countdowns, an entry gallery filtered by category, past winners by year, and entry and nomination forms that post to Raytha Functions and save drafts for review. 4 content types, 11 widgets, 2 functions. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/UuInALAw5UuRF91xAq6tOg_commonground_01_home_hero.webp" width="360" alt="Commonground Association">](association-commonground/) | **[Commonground Association](association-commonground/)**: a nonprofit membership association with member benefits, four tiers that join through an external link (no payments), a chapter map and directory, events filtered by format and audience, news, and a members-only resource library behind Raytha login. 5 content types, 12 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/ghlpZ1oiZECxM06Pjao6AQ_lowtide_01_home_hero.webp" width="360" alt="Low Tide Festival">](music-festival-lowtide/) | **[Low Tide Festival](music-festival-lowtide/)**: a three-day music festival with a lineup you filter by day, stage and genre, a schedule grid per stage and day, artist and stage pages, an SVG venue map with a place legend, an FAQ with search, and "My picks" stars saved in the browser. Tickets link out to a placeholder partner. 4 content types, 10 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/4AfuiYBmH0SfvgHbAK9pGw_alder_01_home_hero.webp" width="360" alt="The Alder Foundation">](foundation-alder/) | **[The Alder Foundation](foundation-alder/)**: a grantmaking foundation with grant programs and deadlines, a grantee database you filter by program, year and region (with a CSV download), impact stories, annual reports with a print-to-PDF layout, and an apply page that links out to a placeholder grants portal. 5 content types, 14 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/pirXNL723U29DwHo6u8cDQ_ledger_01_home_hero.webp" width="360" alt="The Harbor Ledger">](news-harbor-ledger/) | **[The Harbor Ledger](news-harbor-ledger/)**: a local news site with section fronts, bylines and staff pages, a breaking banner switched on by a checkbox, timestamped live updates with a key-developments filter, a most-read list, and RSS and JSON feeds served by Raytha Functions. 4 content types, 10 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/C0SAAyOVg0WlEbppl3brpQ_maren_ezra_wedding_01_home_hero.webp" width="360" alt="Maren & Ezra">](wedding-maren-ezra/) | **[Maren & Ezra](wedding-maren-ezra/)**: a wedding website with a weekend schedule and add-to-calendar links, hotel room blocks with cut-off countdowns, an RSVP form that saves private drafts through a Raytha Function, and a guest page only signed-in guests can see. 8 content types, 12 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/gk6fvObkGECGJo67ivubyg_lantern_ramblers_01_home_hero.webp" width="360" alt="Lantern Ramblers">](band-lantern-ramblers/) | **[Lantern Ramblers](band-lantern-ramblers/)**: a tribute band site with upcoming and past tour dates, a setlist archive you filter by song, song stats counted live from every setlist in Liquid, and a booking form that saves private drafts. 5 content types. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/sJNessfzGUO96Rpjk_RQ2w_postmark_trips_01_home_hero.webp" width="360" alt="Postmark Trips">](travel-postmark/) | **[Postmark Trips](travel-postmark/)**: a surprise travel agency site with trip tiers shown as stamps, past reveals as postcards with a region filter, reviews with a rating breakdown worked out in Liquid, a clue envelope fed by a JSON function, and a trip planner that saves private drafts. 5 content types, 10 widgets. |
| [<img src="https://raytha.com/raytha/media-items/objectkey/5ivXGVtPpEGX7wD-c3mrlg_meridian_02_home_hero.webp" width="360" alt="Meridian Hub">](intranet-meridian-hub/) | **[Meridian Hub](intranet-meridian-hub/)**: a self-hosted company intranet and employee portal: a personal dashboard, news and announcements, an employee directory with filters, departments, a policy handbook with acknowledgements and managers-only pages, events, a resource library, IT help and system status, all behind Raytha login and user groups. 8 content types, 13 widgets. |

## Quickstart

### 1. Run Raytha

The fastest way is the one-click Railway template:

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/raytha-cms?referralCode=RU52It&utm_medium=integration&utm_source=template&utm_campaign=generic)

Or run it locally with Docker:

```bash
git clone https://github.com/RaythaHQ/raytha.git && cd raytha
cp .env.example .env
docker compose --env-file .env up      # then open http://localhost:5001 and finish the setup wizard
```

In the setup wizard, set the **website URL** to the address you'll actually browse. Functions and feeds build
absolute links from it. Then create an API key: Settings > Administrators > your account > API keys.

### 2. Install the CLI

```bash
curl -fsSL https://raytha.com/cli/install.sh | sh          # Windows: irm https://raytha.com/cli/install.ps1 | iex
export RAYTHA_URL=http://localhost:5001
export RAYTHA_API_KEY=...                                  # never commit this
raytha doctor                                              # checks the URL, the key and its permissions
```

You also need `jq`. The build scripts use it.

### 3. Build an example

```bash
git clone https://github.com/RaythaHQ/raytha-examples.git
cd raytha-examples/conference-horizon-summit
DRY_RUN=1 bash build.sh    # preview: theme and schema changes only, nothing is written
bash build.sh              # build it, then open $RAYTHA_URL
```

Use a fresh instance. The scripts activate the example's theme and, unless you set `PRUNE_MENUS=0`, make the
menus match the example.

## One-shot your own site with an AI agent

The examples were built from a short brief with no human help. To do the same for your own site:

1. Copy [templates/brief-template.md](templates/brief-template.md) and fill it in: what the site is for, the
   look, the content model, the pages, and what "done" means.
2. Give your coding agent (Cursor, Claude Code, Codex, or any agent that can run a shell) the CLI and a key:
   `RAYTHA_URL` and `RAYTHA_API_KEY` in its environment.
3. Add the rules: copy [AGENTS.md](AGENTS.md) into your project, and install the skills:
   - the official CLI skill, [`raytha-cli/skills/raytha/SKILL.md`](https://github.com/RaythaHQ/raytha-cli/blob/main/skills/raytha/SKILL.md)
   - this repo's [skills/raytha-site-builder/SKILL.md](skills/raytha-site-builder/SKILL.md): the brief-to-finished-site workflow
4. Prompt it:

   > Build the site described in brief.md on the Raytha instance at $RAYTHA_URL using the raytha CLI. Follow
   > AGENTS.md and the raytha-site-builder skill. Work from files in ./site, dry-run before every push, and finish
   > with `raytha check` passing and desktop and mobile screenshots.

5. Review the screenshots, ask for changes, and keep `./site` in git. That folder is your site.

## Repository layout

```
.
├── conference-horizon-summit/   # one folder per example
│   ├── brief.md  README.md  build.sh  schema.json  shots.json
│   ├── theme/  functions/  seed/  pages/  menus/  screenshots/
├── job-board-groundwork/
├── help-center-orbitly/         # newer examples share scripts/build-example.sh
├── lms-portal-atlas/
├── medical-supply-brightwell/
├── awards-halftone/
├── association-commonground/
├── music-festival-lowtide/
├── foundation-alder/
├── news-harbor-ledger/
├── wedding-maren-ezra/
├── band-lantern-ramblers/
├── travel-postmark/
├── intranet-meridian-hub/
├── skills/raytha-site-builder/  # agent skill: brief -> finished Raytha site
├── templates/brief-template.md  # fill-in brief
├── scripts/                     # shared build script, scaffold, screenshots, walkthroughs, export, secret scan
├── AGENTS.md                    # rules for coding agents building Raytha sites
├── CONTRIBUTING.md
├── llms.txt
└── LICENSE                      # MIT
```

## Scripts

| Script | What it does |
|--------|--------------|
| [scripts/build-example.sh](scripts/build-example.sh) | Rebuilds an example folder from its `example.json`; the newer examples' `build.sh` files call it |
| [scripts/new-example.sh](scripts/new-example.sh) | Scaffolds `<name>/` with a brief, README, build script and empty folders |
| [scripts/export-from-instance.sh](scripts/export-from-instance.sh) | Pulls a site's theme, schema, functions, pages and menus into an example folder |
| [scripts/capture-screenshots.py](scripts/capture-screenshots.py) | Desktop and mobile screenshots with Playwright, from a `shots.json` |
| [scripts/make-walkthrough.py](scripts/make-walkthrough.py) | Records a 20 to 40 second walkthrough video of a built site from a `walkthrough.json` shot list ([usage](scripts/make-walkthrough.md)) |
| [scripts/scan-secrets.sh](scripts/scan-secrets.sh) | Checks for keys, passwords, local URLs and real email addresses before you commit |

## Contributing

New examples are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE), the same as Raytha. All example content is fictional.
