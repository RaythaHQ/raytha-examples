# Contributing an example

Examples are welcome, whether an agent or a person built them. A good example is a site someone would actually want,
built from a short brief, that rebuilds cleanly on a fresh Raytha instance.

## Checklist

1. **Scaffold:** `bash scripts/new-example.sh <kind>-<name> "<Site title>"`, e.g. `restaurant-kiln-and-kettle`.
2. **Write the brief** in `brief.md` before building, from [templates/brief-template.md](templates/brief-template.md).
   Keep it to what the builder actually got.
3. **Build the site** on a local or throwaway Raytha instance with the `raytha` CLI, following [AGENTS.md](AGENTS.md).
4. **Export it:** `bash scripts/export-from-instance.sh <folder> <theme>`, and put seed content (JSON Lines plus images)
   in `seed/`.
5. **Write `build.sh`.** Adapt [conference-horizon-summit/build.sh](conference-horizon-summit/build.sh). It must:
   read `RAYTHA_URL` and `RAYTHA_API_KEY` from the environment; support `DRY_RUN=1`; be safe to run twice; end with
   `raytha check`.
6. **Test the rebuild on an empty instance**, run it a second time to prove it's idempotent, and confirm
   `raytha check` passes both times.
7. **Screenshots:** list them in `shots.json` and capture with `scripts/capture-screenshots.py`. Desktop at 1440px,
   phone at 390px. Link a curated set from `screenshots/README.md`.
8. **README:** what it is, screenshots, a table of features and the Raytha features behind them, the build time and
   rebuild steps. Use the conference example as the model.
9. **Add a row** to the gallery table in the root [README.md](README.md) and an entry in [llms.txt](llms.txt).
10. **Scan:** `bash scripts/scan-secrets.sh` must come back clean.

## Rules

- **Fictional data only:** invented people, companies and places; `example.com` emails and URLs; 555 phone numbers.
- **Images you can redistribute:** generated SVGs, your own screenshots, or images with an explicit open license
  (credit them in the example README). No photos of real people attached to invented names.
- **No secrets:** no API keys, passwords, connection strings, local admin URLs or credentials files. Read values
  from the environment.
- **Portable themes:** load frameworks and fonts from a CDN. Don't depend on a particular instance's media IDs or
  object keys.
- **One example per folder.** Don't change other examples in the same pull request.

## Pull requests

Open a PR with a screenshot in the description and the output of `bash build.sh` against an empty instance (with the
key removed). Questions: open an issue or email hello@raytha.com.
