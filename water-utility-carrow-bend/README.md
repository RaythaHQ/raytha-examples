# Carrow Bend Water: a local water utility website

The website of Carrow Bend Water & Sewer District (fictional), a local water utility on the fictional Ossel River, built on Raytha. Pay-a-bill and start/stop pages, service alerts that stay published when resolved, water quality reports in plain language, rates as a table, board agendas and minutes, and conservation guides. Municipal operations-hub design — no real payment or customer data.

- **Brief:** [brief.md](brief.md)
- **Build time:** under an hour
- **Write-up:** [raytha.com/use-cases/carrow-bend-water](https://raytha.com/use-cases/carrow-bend-water)
- **Walkthrough:** [MP4](https://raytha.com/raytha/media-items/objectkey/X5217q-SC0eGXwkWTGrF_w_carrow_bend_water_walkthrough.mp4)

![Carrow Bend Water home](https://raytha.com/raytha/media-items/objectkey/akDuphNnTEOQYU3KDCP0kw_carrowbend_01_home.webp)

## Rebuild

```bash
RAYTHA_URL=https://your-site.example RAYTHA_API_KEY=... bash build.sh
```

4 content types (service alerts, water quality reports, board meetings, conservation guides), site pages, menus, search. Server-rendered Liquid only.
