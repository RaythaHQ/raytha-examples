# Marlowe Architecture: a website for a solo architect with a client portal

The website of Marlowe Architecture, the fictional solo practice of Elena Marlowe, AIA, in Austin, Texas, built on Raytha 2.0.1 by an
AI agent with the [`raytha` CLI](https://github.com/RaythaHQ/raytha-cli). A portfolio of houses, ADUs and remodels, an about page in first person,
services, a journal, ways to start, and a members-only client portal with project rooms, weekly updates and drawings. Every template, content type, item, page, menu and user group went in through the CLI.
Nobody opened the admin.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour of agent time, from an empty install to `raytha check` passing
- **Write-up:** [raytha.com/use-cases/elena-marlowe-architect](https://raytha.com/use-cases/elena-marlowe-architect)
- **Walkthrough video:** [MP4](https://raytha.com/raytha/media-items/objectkey/ADdks-DErUWGx9LfPasu8Q_elena_marlowe_architect_walkthrough.mp4) (shot list: [walkthrough.json](walkthrough.json))

![Marlowe Architecture home page](https://raytha.com/raytha/media-items/objectkey/WkjjkRNFeUOf-iLDQPBtHQ_marlowe_01_home.webp)

## Screenshots

| | |
|---|---|
| ![Projects](https://raytha.com/raytha/media-items/objectkey/lrBAUq90vECXRREITb1V9w_marlowe_03_work.webp) | ![A project](https://raytha.com/raytha/media-items/objectkey/w3xN-9k_mEG8saLW4u7vEg_marlowe_06_project_top.webp) |
| Projects, filterable by type | A project case study |
| ![Client portal](https://raytha.com/raytha/media-items/objectkey/w03bZySLzEG1CUP4JSgyLA_marlowe_19_portal_client.webp) | ![Project room](https://raytha.com/raytha/media-items/objectkey/H1LLPdK5Q0O_dZLoCijmeQ_marlowe_20_project_room.webp) |
| The client portal, signed in as a homeowner | A project room with updates and drawings |

<p>
  <img src="https://raytha.com/raytha/media-items/objectkey/EE8QjGz5q0Gpet8u4dRR5A_marlowe_26_home_mobile.webp" width="240" alt="Home page on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/TlBSBUSNa0iTU4J72_f2Gg_marlowe_28_project_mobile.webp" width="240" alt="A project on a phone">
  <img src="https://raytha.com/raytha/media-items/objectkey/wVg2jAo6lU6m8RggtUZrOQ_marlowe_29_portal_mobile.webp" width="240" alt="Client portal on a phone">
</p>

More in [screenshots/](screenshots/). Recapture them from your own build with [shots.json](shots.json) and
[`scripts/capture-screenshots.py`](../scripts/capture-screenshots.py) (the portal shots need a signed-in member of a
`client_` group or `studio`: set `SITE_USER_EMAIL` and `SITE_USER_PASSWORD`).

## What's in it

- A **home page** at `/`: three featured houses, services, how working with a solo architect works, a testimonial and recent journal entries.
- **Projects** at `/work`, filterable by type (`?industry=`). Each has the land and brief, what Elena designed, materials, results, a plan-and-materials board and a homeowner quote, and relates to its client.
- **Clients** at `/clients`, each with a monogram, a short profile and the house done for them.
- **Services** at `/services` (new homes, ADUs, remodels, consultations), each with deliverables, a typical timeline and related houses.
- An **about** page at `/studio` and Elena's profile at `/about/elena-marlowe`, a **journal** at `/journal` and **ways to start** at `/start`
  (consultations say how to get in touch; there is no booking form).
- A **client portal** at `/portal` with project rooms at `/portal/projects/...` and drawings and files at `/portal/files/...`, for the `client_andersen`, `client_okafor` and `studio` user groups.
- **Contact**, **accessibility** and **search** at `/search?q=...`.

## How the client portal works

- Each project and file has a `client_group` field naming the user group that may see it.
- [ma_portal.liquid](theme/web-templates/ma_portal.liquid),
  [ma_detail_projects.liquid](theme/web-templates/ma_detail_projects.liquid) and
  [ma_detail_deliverables.liquid](theme/web-templates/ma_detail_deliverables.liquid) build a list of the visitor's
  groups from `CurrentUser.UserGroups` on the server. A client sees only items for their own group, the `studio` group
  (and admins) see every client, and signed-out visitors get a sign-in prompt. A client who opens another client's
  project sees a "belongs to another client" notice instead of the content, and portal pages use a generic title and
  description so nothing leaks into the page head.
- Projects, services and journal entries use relationship fields to clients and the architect, so pages link to
  each other without duplicated data. Listings and search read the same items with `get_content_items`.
- Widget templates read their settings from `widget.settings`.

## Rebuild it

```bash
# From a Raytha 2.x install with RAYTHA_URL and RAYTHA_API_KEY set:
bash build.sh
```

`build.sh` generates seed art if needed, then runs [`scripts/build-example.sh`](../scripts/build-example.sh), which
imports the schema, pushes the theme, seeds content, creates the `studio`, `client_andersen` and `client_okafor` user
groups, the site pages and menus, then runs `raytha check`.

To see the portal, create a public user in the admin, add them to `client_andersen`, `client_okafor` or `studio`,
and sign in at `/account/login`.

## Notes

- Marlowe Architecture is fictional. Its architect, clients, houses and files are invented.
- The portal sign-in is a Raytha website account for project updates and drawings. Invoices and contracts are not on the site.
- There are no payment or booking forms on this site.

## Layout of this folder

| Path | Purpose |
|------|---------|
| [schema.json](schema.json) | Content types, fields, choices and views (`raytha schema import`) |
| [theme/](theme/) | Liquid web and widget templates |
| [seed/](seed/) | JSONL content plus `make-art.py` (generated images and PDFs are gitignored) |
| [pages/](pages/) | Site pages and widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) / [walkthrough.json](walkthrough.json) | Screenshot and video shot lists |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [build.sh](build.sh) | One-command rebuild |
