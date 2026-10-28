# Saskell Creek Public Schools: a public school district website

The website for Saskell Creek Public Schools (fictional), a PreK–12 district of sixteen schools in the invented town of Saskell Creek, built on Raytha. The district is drawn as three feeder lines, with today's bells and status as a departure board, lunch as a week of trays, a calendar labeled in words, board meetings with agendas and votes, board policies, a staff directory by school, and members-only family and staff areas gated on the server. "Feeder lines" design — no enrollment, registration, payment or contact forms. The same kit fits a district's own communications team, or an agency or freelancer building sites for school district clients.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/saskell-creek-public-schools](https://raytha.com/use-cases/saskell-creek-public-schools)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/K1-6WN_RAkuBvf5Fc5JwiA_saskell_creek_public_schools_walkthrough.mp4)

![Saskell Creek Public Schools home](https://raytha.com/raytha/media-items/objectkey/zogjrNBpt06rqx0LFB42aA_saskell_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

8 content types (schools, news, calendar events, staff, board meetings, board policies, lunch menus, resources), 2 user groups (`families`, `staff`), site pages (home, about, accessibility, new families, family hub, staff room, search), menus. Server-rendered Liquid only. `build.sh` generates the school and news art if `seed/art` is missing, runs `../scripts/build-example.sh`, then runs the route check.

## How the home page works

- The feeder map is an inline SVG written by the template: each school has a `line` (`ridge`, `creek`, `mill`, `shared`) and a `col` (its stop position), and the template places stops and draws the lines from those fields. The early learning center and career center are drawn as shared stops at each end.
- The departure board loops over every school's `first_bell`, `dismissal`, `status` and `status_note`. Status is always written in words, not only shown as a color.
- The pinned news item (`pinned` = yes) becomes the status strip at the top of every page.
- The lunch trays are the week's `menus` items; the tray for the current weekday is marked Today on the server.
- The next board meeting (with its `agenda` field as a timed list), the upcoming dates and the news list are loops over content types; the only hard-coded block on the home page is the sample student pass that points to the family hub.

## Members-only areas

- Resources have an `audience` field (`public`, `families`, `staff`).
- Templates read `CurrentUser.UserGroups` on the server and render either the body or a lock panel with a sign-in link. Members of `staff` are also treated as families; admins see everything.
- `/families` (template `sc_families`) shows a sample student pass (story data) whose school, bells and today's status come from that school's record, plus this week's lunch, family dates and family documents.
- `/staff-room` (template `sc_staffroom`) shows professional development dates and staff-only documents.
- To try it, create a public user in the admin, add them to `families` and/or `staff`, and sign in at `/account/login`. There is no registration form on purpose.

## Notes

- School buildings and news images (`seed/art/*.svg`) are generated from `seed/make-art.py`; `build.sh` runs it when the folder is missing. No real person or place is pictured.
- Dropdown values are rendered as their developer names and mapped to labels in the templates (`replace`).
- Field values are captured into strings before they are compared, and number fields are captured before arithmetic.
- Templates write `&#36;` instead of a literal dollar sign before a digit: in Raytha 2.0.1 a child template containing `$1` is read as a regex group when it is merged into the layout.
- Everything is fictional: the district, town, schools, people, policies, meetings and addresses. Phone numbers use the 555 range.

## Files

| Path | What it is |
|---|---|
| [brief.md](brief.md) | The brief |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [schema.json](schema.json) | Content types, fields and views |
| [theme/](theme/) | Web templates (`sc_*`, login and 404) and widget templates |
| [seed/](seed/) | Seed content (JSONL) and the art generator |
| [pages/](pages/) | Site pages and their widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) | Screenshot list |
| [walkthrough.json](walkthrough.json) | Walkthrough video shot list (`../scripts/make-walkthrough.py`) |
| [screenshots/](screenshots/) | Screenshots |
