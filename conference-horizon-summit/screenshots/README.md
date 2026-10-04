# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/uzXF7ioaKU218L0jeugYbQ_horizon_summit_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/uzXF7ioaKU218L0jeugYbQ_horizon_summit_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/EvzfC4UEukmIZpcx1Ga0eQ_horizon_summit_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/EvzfC4UEukmIZpcx1Ga0eQ_horizon_summit_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/-ZnCVVc2UEuHXSQL6IiVeQ_horizon_summit_03_agenda_filtered.webp)](https://raytha.com/raytha/media-items/objectkey/-ZnCVVc2UEuHXSQL6IiVeQ_horizon_summit_03_agenda_filtered.webp) | Agenda filtered to Day 2 and the AI & Data track |
| [![](https://raytha.com/raytha/media-items/objectkey/nns8Zx6FaEKY9jffRqj8xw_horizon_summit_05_speakers.webp)](https://raytha.com/raytha/media-items/objectkey/nns8Zx6FaEKY9jffRqj8xw_horizon_summit_05_speakers.webp) | Speaker directory |
| [![](https://raytha.com/raytha/media-items/objectkey/cyTTyEPc90-HJj86-8h9NA_horizon_summit_06_speaker_detail.webp)](https://raytha.com/raytha/media-items/objectkey/cyTTyEPc90-HJj86-8h9NA_horizon_summit_06_speaker_detail.webp) | Speaker page with their sessions |
| [![](https://raytha.com/raytha/media-items/objectkey/rFZ3wnr-WEq_nLVkDoQNDQ_horizon_summit_07_session_detail.webp)](https://raytha.com/raytha/media-items/objectkey/rFZ3wnr-WEq_nLVkDoQNDQ_horizon_summit_07_session_detail.webp) | Session page with Add to calendar |
| [![](https://raytha.com/raytha/media-items/objectkey/1BBmuKVK_Ei5ilxlVsrXNg_horizon_summit_08_sponsors.webp)](https://raytha.com/raytha/media-items/objectkey/1BBmuKVK_Ei5ilxlVsrXNg_horizon_summit_08_sponsors.webp) | Sponsors by tier |
| [![](https://raytha.com/raytha/media-items/objectkey/OEmO_GzlMUSN3rAwEgt72Q_horizon_summit_11_search.webp)](https://raytha.com/raytha/media-items/objectkey/OEmO_GzlMUSN3rAwEgt72Q_horizon_summit_11_search.webp) | Search results |
| [![](https://raytha.com/raytha/media-items/objectkey/3ptFAn9cIU6QgWUOpw6wnA_horizon_summit_14_attendee_hub.webp)](https://raytha.com/raytha/media-items/objectkey/3ptFAn9cIU6QgWUOpw6wnA_horizon_summit_14_attendee_hub.webp) | Attendee Hub, signed in as a member of `attendees` |
| [<img src="https://raytha.com/raytha/media-items/objectkey/Bi1kJZCPg0mGqvPRNYOaaw_horizon_summit_15_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/Bi1kJZCPg0mGqvPRNYOaaw_horizon_summit_15_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/trYQYEte1EGSKRIncDHFRA_horizon_summit_16_agenda_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/trYQYEte1EGSKRIncDHFRA_horizon_summit_16_agenda_mobile.webp) | Agenda on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/ZJqmvWtKdkCz9U9X6khQiA_horizon_summit_17_speaker_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/ZJqmvWtKdkCz9U9X6khQiA_horizon_summit_17_speaker_mobile.webp) | Speaker page on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
