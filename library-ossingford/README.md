# Ossingford Public Library: a public library website

The website for Ossingford Public Library (fictional), a county library system with four branches and a Bookmobile in an invented county, built on Raytha. Today's hours for every branch on the home page, a weekly program planner, new arrivals drawn as book spines on a shelf with catalog-card title pages, reading lists, digital resources A to Z, library news, and members-only pages for cardholders and staff gated on the server. "Card catalog" design — no payment, registration, hold, sign-up or contact forms. The same kit fits a library's own web team, or an agency building sites for libraries and other public institutions.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/ossingford-public-library](https://raytha.com/use-cases/ossingford-public-library)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/TcUQC8kiUEWJQPSUE7qFaQ_ossingford_public_library_walkthrough.mp4)

![Ossingford Public Library home](https://raytha.com/raytha/media-items/objectkey/V11XbAJokkaQeFc-QObgIA_ossingford_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

6 content types (branches, programs, titles, lists, resources, news), 2 user groups (`cardholders`, `staff`), site pages (home, about, get a card, my library, staff room, search), menus. Server-rendered Liquid only. `build.sh` generates the covers, branch drawings and news art if `seed/art` is missing, runs `../scripts/build-example.sh`, then runs the route check.

## How the pages work

- Each branch stores its hours in seven fields (`mon` … `sun`). Templates read the weekday on the server (`"now" | date: "%a"`) and pick the matching field, so "open today" on the home page and the highlighted day on branch and program pages stay current without edits.
- Programs repeat weekly: each has a `weekday`, a time, a branch and an audience. `/programs` lays them out Monday to Sunday; `?for=kids` (or teens, adults, seniors, all) filters on the server.
- New arrivals (`titles`) store format, shelf, call number, copies, holds, a spine color and height, and the branches that hold a copy (`central|millrace|…`). The home page and `/new` draw spines from those fields; `/new?shelf=kids` filters on the server. Title pages show availability by branch.
- Reading lists store their picks as `Title :: Author :: note` separated by `||`.
- Digital resources have an index `letter`, and `/resources` files them A to Z.
- Search runs `get_content_items` with an OData `contains(...)` filter across six content types.

## Members-only areas

- Resources have an `audience` field (`public`, `cardholders`, `staff`).
- Templates read `CurrentUser.UserGroups` on the server and render either the access details or a lock panel with a sign-in link. Staff see everything cardholders see; admins see everything. Staff tools are left out of the A–Z list and search for everyone else.
- `/my-library` (template `ol_card`) shows the cardholder's library card, the cardholder resources, notices and the museum pass table (widgets in the page's section, rendered only for cardholders).
- `/staff-room` (template `ol_staff`) shows the desk schedule, staff notices and staff procedures, only for the `staff` group.
- To try it, create a public user in the admin, add them to `cardholders` and/or `staff`, and sign in at `/account/login`. There is no registration form on purpose.

## Notes

- Covers, branch elevation drawings and news images (`seed/art/*.svg`) are generated from `seed/make-art.py`; `build.sh` runs it when the folder is missing. No real book, building or person is pictured.
- Dropdown values are rendered as their developer names and mapped to labels in the templates with `case`.
- Field values are captured into strings before they are compared, and number fields are captured before arithmetic.
- Everything is fictional: the library, county, branches, people, books, authors, providers and figures. Phone numbers use the 555 range.

## Files

| Path | What it is |
|---|---|
| [brief.md](brief.md) | The brief |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [schema.json](schema.json) | Content types, fields and views |
| [theme/](theme/) | Web templates (`ol_*`, login and 404) and widget templates |
| [seed/](seed/) | Seed content (JSONL) and the art generator |
| [pages/](pages/) | Site pages and their widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) | Screenshot list |
| [walkthrough.json](walkthrough.json) | Walkthrough video shot list (`../scripts/make-walkthrough.py`) |
| [screenshots/](screenshots/) | Screenshots |
