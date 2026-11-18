# Gablefen Realty: a real estate website

The website for Gablefen Realty (fictional), an independent residential brokerage in a mill town, built on Raytha. The home page is built like the listing window at 12 Courthouse Square: six property cards hang on a rail in a wooden frame, and each card shows a house elevation drawn on the server from the listing's style, stories, siding color and roof. Next to the window, an open-house board works out happening now, today and this weekend from stored weekday hours. There is a town plat whose neighborhood washes and numbered listing pins come from content, floor plans drawn from a rooms field, recently sold prices, and members-only desks for buyer clients and agents. "Listing window" design, with no offer, payment, registration or sign-up forms. The kit suits a brokerage that wants to run its own site, or an agency or freelancer building realtor websites for clients.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/gablefen-realty](https://raytha.com/use-cases/gablefen-realty)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/YRBRJOWg8U-Mx02Uvmg29g_gablefen_realty_walkthrough.mp4)

![Gablefen Realty home](https://raytha.com/raytha/media-items/objectkey/hqYFk0tvVEyL_Qt5PgwrJQ_gablefen_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

8 content types (listings, neighborhoods, agents, open houses, house styles, landmarks, bulletins, showings), 2 user groups (`clients`, `agents`), site pages (home, town plat, recently sold, Buy with us, Sell with us, about, client desk, agent desk, search), menus. Server-rendered Liquid only. `build.sh` runs `../scripts/build-example.sh`.

## How the pages work

- **The clock.** Every template starts from `"now" | date` (weekday, hour and minute in the site's time zone). Set the time zone in the admin (Settings) so the open-house board matches local time; the example was built with America/Chicago.
- **Open houses.** Each open house stores a weekday and a start and end time in minutes after midnight, not a single calendar date, so the board stays current week after week. The template works out happening now, today, later this week or this weekend. `/open-houses` groups the board the same way.
- **Elevations.** Each listing points at a house style. The template draws an inline SVG from the style plus the listing's stories, siding color and roof, so the office changes a card by editing the listing, not the artwork. No real house is pictured.
- **Floor plans.** Listings store a `rooms` field (floor, name and dimensions). The listing page draws a simple plan on the server from those rooms.
- **The town plat.** An inline SVG: neighborhood washes come from a path stored with each neighborhood, landmarks from their map positions, and every home is a numbered pin from its `map_x` / `map_y` fields. The office moves a pin by editing content.
- **Days on the market** are computed from the listed date. Prices, square footage and lot size are captured into strings before they are formatted or compared, because decimal field values are not directly numeric in Liquid.
- Search runs `get_content_items` with an OData `contains(...)` filter across the public types, and hides the contents of client- and agent-only items from browsers that should not see them.

## Members-only areas

- Bulletins and showings have an `audience` field (`everyone`, `clients`, `agents`).
- Templates read `CurrentUser.UserGroups` on the server and render either the content or a lock panel with a sign-in link. Admins see everything. Lists show members-only titles with a lock and leave their contents out; the page description in the HTML head uses a generic line for members-only items. Private remarks on a listing are rendered only for signed-in agents.
- `/clients` (template `gf_clients`) shows a client badge, this weekend's tours and shortlist notes, only for the `clients` group.
- `/desk` (template `gf_desk`) shows the deal board (active and coming listings, days on the market, private remarks), desk notes and agent-only showings, only for the `agents` group. Each area points a signed-in member of the other group back to their own.
- To try it, create a public user in the admin, add them to `clients` and/or `agents`, and sign in at `/account/login`. There is no registration form on purpose: in the story, the office opens accounts after a first meeting.

## Notes

- Everything is fictional: the town, the firm, the people, the houses and the figures. Phone numbers use the 555 range. Email addresses use the reserved `.example` TLD.
- Dropdown values are rendered as their developer names and mapped to labels in the templates with `case`.
- Number fields are converted with `append: "" | plus: 0` before arithmetic; field values are captured into strings before they are compared or formatted.
- Web template includes are not used; shared pieces are inlined in each template.
- There are no offer, payment or sign-up forms; offers are written at the office.

## Files

| Path | What it is |
|---|---|
| [brief.md](brief.md) | The brief |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [schema.json](schema.json) | Content types, fields and views |
| [theme/](theme/) | Web templates (`gf_*`, login and 404) and widget templates |
| [seed/](seed/) | Seed content (JSONL) |
| [pages/](pages/) | Site pages and their widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) | Screenshot list |
| [walkthrough.json](walkthrough.json) | Walkthrough video shot list (`../scripts/make-walkthrough.py`) |
| [screenshots/](screenshots/) | Screenshots |
