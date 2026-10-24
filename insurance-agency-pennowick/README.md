# Pennowick Insurance Agency: an independent insurance agency website

The website for Pennowick Insurance Agency (fictional), a third-generation independent agency with three offices and ten appointed carriers, built on Raytha. Coverage lines with what is and is not usually covered, a carrier appointment matrix built from content, claims guides split into the first hour, day and week, agents, offices, an A–Z glossary, client resources, and a members-only client binder gated on the server. "Policy folder" design — no quote request, payment, registration or contact forms. The same kit fits an agency's own team, or a freelancer building sites for agency clients.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/pennowick-insurance-agency](https://raytha.com/use-cases/pennowick-insurance-agency)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/QGtaDIP5i0eiMNG2gAf0lg_pennowick_insurance_agency_walkthrough.mp4)

![Pennowick Insurance Agency home](https://raytha.com/raytha/media-items/objectkey/vnuYd1jeBU-3PK_cSRnjyw_pennowick_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

7 content types (coverage lines, carriers, agents, offices, claims guides, glossary terms, client resources), 2 user groups (`policyholders`, `business`), site pages (home, about, licenses and disclosures, client binder, search), menus. Server-rendered Liquid only.

## How the home page works

- The street-block illustration is inline SVG in `pw_home`. Each coverage line has `pin_x` and `pin_y` fields (percent of the illustration), and the template places a numbered pin for every line, colored by its `family` field. Add a coverage line and it gets a pin and a legend entry.
- The carrier appointment matrix is built from two content types: each carrier's `lines` field lists coverage `code` values (`home|auto|umbrella`), and the template marks a dot where they match. The same codes connect coverage pages to their carriers, agents and claims guides.

## Members-only areas

- Client resources have an `audience` field (`public`, `policyholders`, `business`).
- Templates read `CurrentUser.UserGroups` on the server and render either the body or a lock panel with a sign-in link. Members of `business` are also treated as policyholders; admins see everything.
- `/binder` is the client binder (template `pw_binder`): policy summary (story data), next renewal, assigned agent and the guides the account can open; business accounts get business rows and guides.
- To try it, create a public user in the admin, add them to `policyholders` and/or `business`, and sign in at `/account/login`. There is no registration form on purpose.

## Notes

- Agent portraits (`seed/art/*.svg`) are generated monograms from `seed/make-art.py`; `build.sh` runs it when the folder is missing. No real person is pictured.
- Dropdown values are rendered as their developer names and mapped to labels in the templates (`replace` / `capitalize`).
- Templates write `&#36;` instead of a literal dollar sign before a digit: in Raytha 2.0.1 a child template containing `$1` is read as a regex group when it is merged into the layout.
- Everything is fictional: the agency, people, carriers, places, license and policy numbers. Phone numbers use the 555 range.

## Files

| Path | What it is |
|---|---|
| [brief.md](brief.md) | The brief |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [schema.json](schema.json) | Content types, fields and views |
| [theme/](theme/) | Web templates (`pw_*`, login and 404) and widget templates |
| [seed/](seed/) | Seed content (JSONL) and the portrait generator |
| [pages/](pages/) | Site pages and their widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) | Screenshot list |
| [walkthrough.json](walkthrough.json) | Walkthrough video shot list (`../scripts/make-walkthrough.py`) |
| [screenshots/](screenshots/) | Screenshots |
