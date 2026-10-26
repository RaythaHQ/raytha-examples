# Corrowen & Ivesmark LLP: a law firm website

The website for Corrowen & Ivesmark LLP (fictional), a seven-lawyer litigation and business law firm with two offices in the invented river city of Wendlow, built on Raytha. Practice areas with what the firm handles, what it refers out and how it bills; attorneys as signature blocks; representative matters as a docket with court-style captions; insights as memos; offices; a client library; and a members-only client room gated on the server. "Redline" design — no contact, intake, payment or registration forms. The same kit fits a firm's own team, or an agency or freelancer building sites for law firm clients.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/corrowen-ivesmark-law](https://raytha.com/use-cases/corrowen-ivesmark-law)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/78RqpRfQtU-H9ycfnlM-TA_corrowen_ivesmark_law_walkthrough.mp4)

![Corrowen & Ivesmark LLP home](https://raytha.com/raytha/media-items/objectkey/93xTy1qAa0-tzZ3chasvKw_corrowen_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

6 content types (practice areas, attorneys, representative matters, insights, offices, client library documents), 2 user groups (`clients`, `counsel`), site pages (home, the firm, notices, client room, search), menus. Server-rendered Liquid only. `build.sh` runs `../scripts/build-example.sh`, then removes the dot from "v." in matter URLs (`matters/a-v-b`) and runs the route check.

## How the home page works

- The hero is a statement with tracked changes (`<del>` / `<ins>`), and the margin comments come from the first three attorneys' `margin_note` fields.
- The practice index counts representative matters per practice: each matter has a practice `code`, and the template counts matches. The same codes connect practice pages to their attorneys (`practices` field, `cl|ap`), matters and insights.
- The docket, signature blocks, fee table, memos and offices are all loops over content types; nothing on the home page is hard-coded except the five procedure steps.

## Members-only areas

- Client library documents have an `audience` field (`public`, `clients`, `counsel`).
- Templates read `CurrentUser.UserGroups` on the server and render either the body or a lock panel with a sign-in link. Members of `counsel` are also treated as clients; admins see everything.
- `/client-room` (template `ci_room`) shows a matter (story data) whose phase track is drawn from the commercial litigation practice's own `steps` field, the next deadlines, budget by phase, the team and the documents the account can open; `counsel` accounts also get a counsel desk.
- To try it, create a public user in the admin, add them to `clients` and/or `counsel`, and sign in at `/account/login`. There is no registration form on purpose.

## Notes

- Attorney portraits (`seed/art/*.svg`) are generated initials on ruled paper from `seed/make-art.py`; `build.sh` runs it when the folder is missing. No real person is pictured.
- Dropdown values are rendered as their developer names and mapped to labels in the templates (`replace`).
- Templates write `&#36;` instead of a literal dollar sign before a digit: in Raytha 2.0.1 a child template containing `$1` is read as a regex group when it is merged into the layout.
- Everything is fictional: the firm, people, bar numbers, courts, matters, docket numbers and places. Phone numbers use the 555 range.

## Files

| Path | What it is |
|---|---|
| [brief.md](brief.md) | The brief |
| [example.json](example.json) | Theme name, content type order, detail templates, user groups |
| [schema.json](schema.json) | Content types, fields and views |
| [theme/](theme/) | Web templates (`ci_*`, login and 404) and widget templates |
| [seed/](seed/) | Seed content (JSONL) and the portrait generator |
| [pages/](pages/) | Site pages and their widget sections |
| [menus/](menus/) | Main and footer menus |
| [shots.json](shots.json) | Screenshot list |
| [walkthrough.json](walkthrough.json) | Walkthrough video shot list (`../scripts/make-walkthrough.py`) |
| [screenshots/](screenshots/) | Screenshots |
