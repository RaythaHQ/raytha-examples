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
