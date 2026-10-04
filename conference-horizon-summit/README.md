# Horizon Summit 2027: a conference website

A complete website for a fictional three-day tech conference in Austin, built on Raytha 2.0.1 by an AI agent with
the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). Every template, content type, item, page, menu and
function went in through the CLI. Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** about 30 minutes of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/horizon-summit-2027](https://raytha.com/use-cases/horizon-summit-2027)

![Horizon Summit home page](https://raytha.com/raytha/media-items/objectkey/uzXF7ioaKU218L0jeugYbQ_horizon_summit_01_home_hero.webp)

## Screenshots

| | |
|---|---|
| ![Agenda filtered by day and track](https://raytha.com/raytha/media-items/objectkey/-ZnCVVc2UEuHXSQL6IiVeQ_horizon_summit_03_agenda_filtered.webp) | ![Speaker directory](https://raytha.com/raytha/media-items/objectkey/nns8Zx6FaEKY9jffRqj8xw_horizon_summit_05_speakers.webp) |
| Agenda filtered by day and track | Speaker directory |
| ![Session page](https://raytha.com/raytha/media-items/objectkey/rFZ3wnr-WEq_nLVkDoQNDQ_horizon_summit_07_session_detail.webp) | ![Attendee Hub](https://raytha.com/raytha/media-items/objectkey/3ptFAn9cIU6QgWUOpw6wnA_horizon_summit_14_attendee_hub.webp) |
| Session page with Add to calendar | Members-only Attendee Hub |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/Bi1kJZCPg0mGqvPRNYOaaw_horizon_summit_15_home_mobile.webp" width="240" alt="Home on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/trYQYEte1EGSKRIncDHFRA_horizon_summit_16_agenda_mobile.webp" width="240" alt="Agenda on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/ZJqmvWtKdkCz9U9X6khQiA_horizon_summit_17_speaker_mobile.webp" width="240" alt="Speaker page on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py).

## What's in it

- A home page with an animated hero, a live countdown, a topic marquee, featured speakers, five tracks, key dates, a
  three-tier sponsor wall, news and a save-the-date band.
- An agenda that filters by day and track, laid out as a timeline, plus a keynotes-only view.
- A speaker directory and a page per speaker listing every session they're in, co-presented ones included.
- A page per session with time, room, level, speakers, more from the same track, and **Add to calendar** (`.ics`).
- Track pages, sponsors grouped by tier, news, venue and travel, FAQ, and site search.
- A members-only **Attendee Hub** for the `attendees` user group.
- Restyled sign-in, 403, 404 and 500 pages.

## The Raytha features behind it

| Feature | How it's built |
|---------|----------------|
| Speakers, sessions, tracks, sponsors, news | Five **content types** in [schema.json](schema.json). Sessions use **relationship fields** (speaker, co-speaker, track) and **dropdowns** (day, room, format, level). |
| Seed content with photos and logos | `raytha content import` from JSON Lines in [seed/](seed/). Relationships point at the related item by name, and `@file:` uploads each image to the media library. |
| Agenda with day and track filters | A **list view** at `/agenda`. The **Liquid** template reads `?day=` and `?track=`, validates them and calls `get_content_items` with a filter. |
| Keynotes only | A second view at `/agenda/keynotes` with a saved filter (`format eq keynote`), using the same template. |
| Speaker pages that list their sessions | The detail template queries `speaker eq '<id>' or cospeaker eq '<id>'`. |
| Home, venue, FAQ | **Site pages** built from 14 custom **widget templates**, each with a settings form an editor can use in the admin. |
| Add to calendar, agenda feed | Three **Raytha Functions** in [functions/](functions/): `/calendar/session.ics?id=…`, `/calendar/horizon-summit-2027.ics`, `/calendar/agenda.json`. |
| Attendee Hub | A **user group**. The page template checks `CurrentUser.UserGroups`, so non-members never receive the members-only HTML. |
| Search | A site page whose template runs `contains()` filters over sessions, speakers and news. |
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
   The calendar functions build absolute links from it.

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
   cd conference-horizon-summit
   DRY_RUN=1 bash build.sh     # previews the theme push and schema import, changes nothing
   bash build.sh
   ```

   The script pushes and activates the `horizon` theme, imports the schema, binds every view to its list template,
   imports the seed content, lowercases item URLs, creates the `attendees` group, the five site pages, the three
   functions and both menus, then runs `raytha check`. You can run it again: everything is created or updated in
   place, and seed content only goes into content types that are still empty.

   By default it makes the main and footer menus match this example and removes other items (the default Home, About
   and Posts links on a fresh install). Set `PRUNE_MENUS=0` to keep them.

5. **See the Attendee Hub.** Create a public user in the `attendees` group (admin: Users), sign in, and open
   `/attendee-hub`.

### Doing it by hand

`build.sh` is plain CLI calls. The core of it:

```bash
raytha theme push ./theme --activate
raytha schema import schema.json --dry-run && raytha schema import schema.json
raytha content-type views settings sessions <view-id> --template hz_list_sessions   # once per view
(cd seed && raytha content import speakers --file seed-speakers.jsonl --template hz_detail_speakers)
raytha site-page create --title "Attendee Hub" --template hz_attendee_hub --route-path attendee-hub --sections @pages/hub.json
raytha function create session.ics --trigger http_request --file functions/session.ics.js --route-path calendar/session.ics
raytha user-group create attendees --label Attendees
raytha menu items create mainmenu --label Agenda --link /agenda
raytha check
```

## Files

| Path | What it is |
|------|------------|
| [brief.md](brief.md) | The brief the agent got |
| [build.sh](build.sh) | Idempotent rebuild script (`RAYTHA_URL`, `RAYTHA_API_KEY` from env) |
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | The `horizon` theme (`raytha theme push`): `theme.json`, the custom `hz_*` web and widget templates, and the built-in templates it restyles (base layout, sign-in, 403, 404, 500). Built-ins it doesn't change are created by Raytha with their defaults. |
| [functions/](functions/) | Raytha Functions plus `functions.json` (names, triggers, routes) |
| [seed/](seed/) | Seed content as JSON Lines, SVG speaker portraits and sponsor logos, and the script that draws the portraits |
| [pages/](pages/) | Site page sections and `pages.json` (title, route, template) |
| [menus/](menus/) | Main and footer menu items |
| [shots.json](shots.json) | The screenshot list for `scripts/capture-screenshots.py` |

## Notes

- Everything is fictional: the event, people, companies, addresses, Wi-Fi details and phone numbers. Emails and
  websites use `example.com`.
- Speaker portraits are flat SVG illustrations drawn by [seed/make-avatars.py](seed/make-avatars.py). Sponsor logos are
  generated SVGs too. No photos, nothing third-party.
- Bootstrap and Bootstrap Icons load from jsDelivr and fonts from Google Fonts, so the theme has no media files and
  moves between instances cleanly.
