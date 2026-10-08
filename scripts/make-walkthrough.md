# make-walkthrough.py: walkthrough videos for an example

`scripts/make-walkthrough.py` records a short, silent walkthrough video of a running site from a JSON shot list:
a title card, a few pages with smooth scrolling, real clicks and typing, captions, an optional phone view,
and a "Built with Raytha" end card. The output is an MP4 that X accepts as is, plus a poster frame.

- 1920x1080 (a 1440x810 desktop viewport at 4/3 device scale), 30 fps, H.264 High, yuv420p, `+faststart`, no audio
- Re-encoded at rising CRF until it fits the size budget (default 14.5 MB)
- `<slug>-walkthrough-poster.jpg` from the frame you mark with `"poster": true`

Frames are rendered one at a time: the script sets the scroll position, cursor and caption for each frame and then
grabs it, and page loads happen between frames behind a short crossfade. A slow machine or a slow page only makes
the render take longer. It never shows up as stutter or dead time in the video.

## Requirements

```bash
pip install playwright pillow && playwright install chromium   # uses /usr/bin/google-chrome instead if present
ffmpeg -encoders | grep libx264                                 # ffmpeg with libx264 on PATH
```

## Run it

```bash
# 1. Build the example into a local Raytha (see the example's README), then:
export BASE_URL=http://localhost:5001          # or pass --base
# 2. Only if a scene has "signin": true: a public site user in the members group, never an admin
export SITE_USER_EMAIL=member@example.com
export SITE_USER_PASSWORD='...'                # keep it in your shell or an untracked .env, never in the repo
# 3. Record
python3 scripts/make-walkthrough.py job-board-groundwork/walkthrough.json
# -> walkthrough-out/groundwork-job-board/groundwork-job-board-walkthrough.mp4 and ...-poster.jpg
```

Options: `--out DIR`, `--base URL`, `--fps 30`, `--max-mb 14.5`, `--keep-master` (also keeps the near-lossless
master). A render takes about 2 minutes for 30 seconds of video. Check the result quickly with a contact sheet:

```bash
ffmpeg -i walkthrough-out/<slug>/<slug>-walkthrough.mp4 -vf "fps=1,scale=480:-1,tile=4x8" -frames:v 1 sheet.jpg
```

**Do not commit the MP4.** `walkthrough-out/` and `*.mp4` are ignored. Upload the video and poster to the
raytha.com media library, set them on the use case (`walkthrough_video` and `walkthrough_poster` attachment
fields), and link the raytha.com copy from the example's README.

## Published walkthroughs

| Example | Shot list | Video (hosted on raytha.com, not in this repo) |
|---------|-----------|-------|
| Horizon Summit 2027 | [walkthrough.json](../conference-horizon-summit/walkthrough.json) | [use case page](https://raytha.com/use-cases/horizon-summit-2027#walkthrough) · [MP4, 32 s](https://raytha.com/raytha/media-items/objectkey/47Ij3hbgO0SBPUGwoXh-6w_horizon_summit_2027_walkthrough.mp4) |
| Groundwork | [walkthrough.json](../job-board-groundwork/walkthrough.json) | [use case page](https://raytha.com/use-cases/groundwork-job-board#walkthrough) · [MP4, 34 s](https://raytha.com/raytha/media-items/objectkey/iPe_Om6NCkubPr8z3fgViA_groundwork_job_board_walkthrough.mp4) |
| Orbitly help center | [walkthrough.json](../help-center-orbitly/walkthrough.json) | [use case page](https://raytha.com/use-cases/orbitly-help-center#walkthrough) · [MP4, 30 s](https://raytha.com/raytha/media-items/objectkey/e5CN46HnDkaUUrwTxrHCsQ_orbitly_help_center_walkthrough.mp4) |
| Atlas Learning | [walkthrough.json](../lms-portal-atlas/walkthrough.json) | [use case page](https://raytha.com/use-cases/atlas-learning-portal#walkthrough) · [MP4, 34 s](https://raytha.com/raytha/media-items/objectkey/lWLEOS8HTkGjXHxXdgeczw_atlas_learning_portal_walkthrough.mp4) |
| Brightwell Medical Supply | [walkthrough.json](../medical-supply-brightwell/walkthrough.json) | [use case page](https://raytha.com/use-cases/brightwell-medical-supply#walkthrough) · [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/9pdCqxo6rU2K_eFnS0krAw_brightwell_medical_supply_walkthrough.mp4) |
| Halftone Awards | [walkthrough.json](../awards-halftone/walkthrough.json) | [use case page](https://raytha.com/use-cases/halftone-awards#walkthrough) · [MP4, 35 s](https://raytha.com/raytha/media-items/objectkey/Ibglwxveok6Ukqruh0ssig_halftone_awards_walkthrough.mp4) |
| Commonground Association | [walkthrough.json](../association-commonground/walkthrough.json) | [use case page](https://raytha.com/use-cases/commonground-association#walkthrough) · [MP4, 39 s](https://raytha.com/raytha/media-items/objectkey/xPX-nCH0fkG6GoPxTFSprA_commonground_association_walkthrough.mp4) |
| Low Tide Festival | [walkthrough.json](../music-festival-lowtide/walkthrough.json) | [use case page](https://raytha.com/use-cases/lowtide-festival#walkthrough) · [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/7dyazsM6iUqbjDM165vTUw_lowtide_festival_walkthrough.mp4) |
| The Alder Foundation | [walkthrough.json](../foundation-alder/walkthrough.json) | [use case page](https://raytha.com/use-cases/alder-foundation#walkthrough) · [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/lkhhwl3oCUCKTjrwtUHLbA_alder_foundation_walkthrough.mp4) |
| The Harbor Ledger | [walkthrough.json](../news-harbor-ledger/walkthrough.json) | [use case page](https://raytha.com/use-cases/harbor-ledger#walkthrough) · [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/1_Sl05emvkSkn4xPU4Gy8g_harbor_ledger_walkthrough.mp4) |
| Maren & Ezra | [walkthrough.json](../wedding-maren-ezra/walkthrough.json) | [use case page](https://raytha.com/use-cases/maren-ezra-wedding#walkthrough) · [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/i_3WFE8xnE-bJVinoQkQSA_maren_ezra_wedding_walkthrough.mp4) |
| Lantern Ramblers | [walkthrough.json](../band-lantern-ramblers/walkthrough.json) | [use case page](https://raytha.com/use-cases/lantern-ramblers#walkthrough) · [MP4, 38 s](https://raytha.com/raytha/media-items/objectkey/wKhcWTQbC0OPJaPvBSbscw_lantern_ramblers_walkthrough.mp4) |
| Postmark Trips | [walkthrough.json](../travel-postmark/walkthrough.json) | [use case page](https://raytha.com/use-cases/postmark-trips#walkthrough) · [MP4, 40 s](https://raytha.com/raytha/media-items/objectkey/4hPyDoV7ekOOo_YWwd3Ekg_postmark_trips_walkthrough.mp4) |
| Meridian Hub | [walkthrough.json](../intranet-meridian-hub/walkthrough.json) | [use case page](https://raytha.com/use-cases/meridian-hub-intranet#walkthrough) · [MP4, 35 s](https://raytha.com/raytha/media-items/objectkey/u-mtvWpRi0yFKzFIb7eJiw_meridian_hub_walkthrough.mp4) |
| City of Juniper Falls | [walkthrough.json](../city-government-juniper-falls/walkthrough.json) | [use case page](https://raytha.com/use-cases/juniper-falls-city-government#walkthrough) · [MP4, 36 s](https://raytha.com/raytha/media-items/objectkey/da3ClwgR3UioVMR0WYZitA_juniper_falls_walkthrough.mp4) |

## Shot list

See [conference-horizon-summit/walkthrough.json](../conference-horizon-summit/walkthrough.json) and
[job-board-groundwork/walkthrough.json](../job-board-groundwork/walkthrough.json).

```jsonc
{
  "slug": "groundwork-job-board",            // output file names
  "base": "http://localhost:5001",           // optional; BASE_URL or --base override it
  "colorScheme": "light",                    // prefers-color-scheme for the site
  "title": { "kicker": "Raytha use case · Week 2", "heading": "Groundwork",
             "subheading": "One line about the site.", "hold": 1.6 },   // or "title": false
  "end":   { "heading": "Built with Raytha", "subheading": "...",
             "url": "raytha.com/use-cases/groundwork-job-board", "hold": 2.6 },  // or "end": false
  "login": { "path": "/account/login", "emailEnv": "SITE_USER_EMAIL", "passwordEnv": "SITE_USER_PASSWORD" },
  "prepJs": "optional JS run after every page load (e.g. to dismiss a banner)",
  "css": "optional CSS injected into every page",
  "scenes": [
    { "url": "/", "caption": "Climate tech jobs, with the salary on every listing",
      "actions": [
        { "hold": 1.1, "poster": true },
        { "type": { "selector": ".hero-search input[name=q]", "text": "python", "cps": 10 }, "press": "Enter" },
        { "scroll": 420, "dur": 1.6 }
      ] },
    { "url": "/jobs", "startScroll": { "selector": "a.chip[href='/jobs?salary=130000']", "offset": 430 },
      "caption": "Filters by salary, skill and type",
      "actions": [ { "click": "a.chip[href='/jobs?salary=130000']", "dur": 0.9 }, { "hold": 0.5 } ] },
    { "url": "/hub", "signin": true, "caption": "Members-only hub", "actions": [ { "hold": 0.8 } ] },
    { "url": "/jobs", "phone": true, "phoneCaption": { "kicker": "Responsive", "text": "Search and apply from a phone" },
      "actions": [ { "hold": 0.5 }, { "scroll": 900, "dur": 1.9 } ] }
  ]
}
```

Scene keys: `url`, `caption` (a small pill at the bottom left), `startScroll` (where the scene opens), `signin`
(sign in off camera before loading the scene), `phone` (render a 390x844 mobile viewport inside a phone frame
next to `phoneCaption`; phone scenes take `hold` and `scroll` only), `fade` (crossfade seconds, default 0.5).

Actions, in order:

| action | does |
|--------|------|
| `{"hold": 1.2, "poster": true}` | stay still for 1.2 s; `poster` uses the middle frame as the poster |
| `{"scroll": 900}` / `{"scroll": "bottom"}` / `{"scroll": {"selector": "#faq", "offset": 90}}` | eased scroll; `dur` seconds (default 2) |
| `{"click": "css", "dur": 0.9}` | glide the cursor to the element, press, crossfade to the page it opens. Add `"navigates": false` for in-page clicks |
| `{"type": {"selector": "css", "text": "python", "cps": 12}, "press": "Enter"}` | glide, click, type at `cps` characters per second, optionally press a key that navigates |
| `{"hover": "css", "hold": 0.6}` | glide and hover (shows hover styles) |
| `{"move": "css"}` | glide the cursor to an element without clicking |
| `{"caption": "New text"}` / `{"caption": ""}` | change or hide the caption mid-scene |
| `{"cursor": false}` | fade the cursor out |
| `{"eval": "js"}` | run JavaScript in the page |

Click and type targets must already be on screen. Scroll to them first (or use `startScroll`), so the cursor
never jumps. The script stops with a clear error if a selector is missing or off screen.

Tips: aim for 25 to 35 seconds (the script warns outside 20 to 40). Five or six scenes of about 4 to 5 seconds
each work well: home, a filtered list, a detail page, the members area, then the phone view. Content that fades
in on scroll (`.reveal`, `[data-reveal]`, `[data-aos]` and similar) is shown up front so nothing pops in on
camera, and lazy images are loaded before recording.
