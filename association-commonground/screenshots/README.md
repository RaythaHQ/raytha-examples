# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/UuInALAw5UuRF91xAq6tOg_commonground_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/UuInALAw5UuRF91xAq6tOg_commonground_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/pr7AE0cyiUGBtnnQk5Bc1w_commonground_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/pr7AE0cyiUGBtnnQk5Bc1w_commonground_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/1LcfWh4lDk6_vJ1YCgq2_A_commonground_03_membership.webp)](https://raytha.com/raytha/media-items/objectkey/1LcfWh4lDk6_vJ1YCgq2_A_commonground_03_membership.webp) | Membership tiers, ways to join and FAQ |
| [![](https://raytha.com/raytha/media-items/objectkey/J4AWFClbkEOoF495I0K67g_commonground_04_tier.webp)](https://raytha.com/raytha/media-items/objectkey/J4AWFClbkEOoF495I0K67g_commonground_04_tier.webp) | A tier page |
| [![](https://raytha.com/raytha/media-items/objectkey/JXjcz-1K0EO0Xdd1d8h-HQ_commonground_05_chapters.webp)](https://raytha.com/raytha/media-items/objectkey/JXjcz-1K0EO0Xdd1d8h-HQ_commonground_05_chapters.webp) | Chapter map and directory |
| [![](https://raytha.com/raytha/media-items/objectkey/UaXVbyFLvUm8BVQz0HhCSw_commonground_06_chapter.webp)](https://raytha.com/raytha/media-items/objectkey/UaXVbyFLvUm8BVQz0HhCSw_commonground_06_chapter.webp) | A chapter page |
| [![](https://raytha.com/raytha/media-items/objectkey/j1ePFLyYNke_0vOlV7p1Jg_commonground_07_events.webp)](https://raytha.com/raytha/media-items/objectkey/j1ePFLyYNke_0vOlV7p1Jg_commonground_07_events.webp) | Events with filters |
| [![](https://raytha.com/raytha/media-items/objectkey/pCQb2AR-cE2d09XWJYwRtw_commonground_08_event.webp)](https://raytha.com/raytha/media-items/objectkey/pCQb2AR-cE2d09XWJYwRtw_commonground_08_event.webp) | An event page |
| [![](https://raytha.com/raytha/media-items/objectkey/1kvHpS9qTk6_SYWejxs_IA_commonground_09_resources_locked.webp)](https://raytha.com/raytha/media-items/objectkey/1kvHpS9qTk6_SYWejxs_IA_commonground_09_resources_locked.webp) | The resource library, signed out |
| [![](https://raytha.com/raytha/media-items/objectkey/H-E9LNryxEuUzuHS9irqxA_commonground_10_resource_locked.webp)](https://raytha.com/raytha/media-items/objectkey/H-E9LNryxEuUzuHS9irqxA_commonground_10_resource_locked.webp) | A locked resource |
| [![](https://raytha.com/raytha/media-items/objectkey/yNSwy_HWakSAlWt0HIzhRQ_commonground_11_member_dashboard.webp)](https://raytha.com/raytha/media-items/objectkey/yNSwy_HWakSAlWt0HIzhRQ_commonground_11_member_dashboard.webp) | A member's dashboard, signed in |
| [![](https://raytha.com/raytha/media-items/objectkey/1nu1VR7WnUGLZngzhLTE0g_commonground_12_resource_open.webp)](https://raytha.com/raytha/media-items/objectkey/1nu1VR7WnUGLZngzhLTE0g_commonground_12_resource_open.webp) | A resource, signed in as a member |
| [![](https://raytha.com/raytha/media-items/objectkey/fECQzj7ArkOJ7rn6twsUdg_commonground_13_news.webp)](https://raytha.com/raytha/media-items/objectkey/fECQzj7ArkOJ7rn6twsUdg_commonground_13_news.webp) | News |
| [![](https://raytha.com/raytha/media-items/objectkey/beyZztTl_UKZ5yTO-sT92g_commonground_14_login.webp)](https://raytha.com/raytha/media-items/objectkey/beyZztTl_UKZ5yTO-sT92g_commonground_14_login.webp) | Member sign in |
| [<img src="https://raytha.com/raytha/media-items/objectkey/wbxs2Rt4H0i1_8A3ReV1eA_commonground_15_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/wbxs2Rt4H0i1_8A3ReV1eA_commonground_15_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/gYkQ3eJD_EKSj3wjrwLz6w_commonground_16_chapters_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/gYkQ3eJD_EKSj3wjrwLz6w_commonground_16_chapters_mobile.webp) | Chapters on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/JdTwCIRUd0SVnKA0rmzGdA_commonground_17_membership_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/JdTwCIRUd0SVnKA0rmzGdA_commonground_17_membership_mobile.webp) | Tiers on a phone |

To capture your own (PNG, into this folder). The signed-in shots need a member account:

```bash
pip install playwright && playwright install chromium
SITE_USER_EMAIL=member@example.com SITE_USER_PASSWORD=... \
  BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
