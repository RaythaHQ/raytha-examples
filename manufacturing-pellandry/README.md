# Pellandry Fluid Controls: a manufacturing company website

The website for Pellandry Fluid Controls (fictional), a maker of industrial valves, actuators and pumps with two plants and a repair center in invented towns, built on Raytha. Twelve product series with spec tables and part-number decoders, a weekly lead-time board next to plant cell load, industry and plant pages, an open literature library, a distributor directory by region, and members-only distributor and service portals gated on the server. "Drawing sheet" design — no quote, order, registration, payment or contact forms. The same kit fits a manufacturer's own marketing team, or an agency building sites for industrial clients.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/pellandry-fluid-controls](https://raytha.com/use-cases/pellandry-fluid-controls)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/xD4Mi5tYGE6dHXMUldcT0g_pellandry_fluid_controls_walkthrough.mp4)

![Pellandry Fluid Controls home](https://raytha.com/raytha/media-items/objectkey/ETD4Tlx0xU6omxcnRT4EAw_pellandry_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

6 content types (products, industries, plants, literature, news, distributors), 2 user groups (`distributors`, `service`), site pages (home, company, quality, distributor portal, service desk, search), menus. Server-rendered Liquid only. `build.sh` generates the product drawings and art if `seed/art` is missing, runs `../scripts/build-example.sh`, then runs the route check.

## How the pages work

- Each product series stores its specs as `Label :: value` pairs separated by `||` (`specs`) and its part-number segments the same way (`pn`); templates split them into the spec table and the decoder strip.
- The lead-time board loops over every product's `lead_weeks` and `plant`; bars over eight weeks are flagged. Plant cell load comes from each plant's `cells` field (`Cell :: load % :: note`).
- Product pages pull related literature (by `product` code), industries (by `industries` codes) and distributors that carry the family (by `lines`).
- Search runs `get_content_items` with an OData `contains(...)` filter across six content types.

## Members-only areas

- Literature has an `audience` field (`public`, `distributors`, `service`).
- Templates read `CurrentUser.UserGroups` on the server and render either the body or a lock panel with a sign-in link. Admins see everything.
- `/portal` (template `pf_portal`) shows price bands, lead times and multipliers by series plus distributor documents. Product pages show the price band only to distributors.
- `/service-desk` (template `pf_service`) shows service bulletins, repair procedures and plant status.
- To try it, create a public user in the admin, add them to `distributors` and/or `service`, and sign in at `/account/login`. There is no registration form on purpose.

## Notes

- Product drawings, industry and news images (`seed/art/*.svg`) are generated from `seed/make-art.py`; `build.sh` runs it when the folder is missing. No real product, plant or person is pictured.
- Dropdown values are rendered as their developer names and mapped to labels in the templates (`replace`).
- Field values are captured into strings before they are compared, and number fields are captured before arithmetic.
- Everything is fictional: the company, towns, plants, products, part numbers, people, distributors and figures. Phone numbers use the 555 range.

## Files

| Path | What it is |
|---|---|
| [brief.md](brief.md) | The brief |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [schema.json](schema.json) | Content types, fields and views |
| [theme/](theme/) | Web templates (`pf_*`, login and 404) and widget templates |
| [seed/](seed/) | Seed content (JSONL) and the art generator |
| [pages/](pages/) | Site pages and their widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) | Screenshot list |
| [walkthrough.json](walkthrough.json) | Walkthrough video shot list (`../scripts/make-walkthrough.py`) |
| [screenshots/](screenshots/) | Screenshots |
