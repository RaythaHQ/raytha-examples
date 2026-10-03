# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/CK4jAJJkZkK7NqGyHd0-1Q_horizon_summit_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/CK4jAJJkZkK7NqGyHd0-1Q_horizon_summit_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/0EwXgB7h4UGFeI_5oQES1w_horizon_summit_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/0EwXgB7h4UGFeI_5oQES1w_horizon_summit_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/4yhV7qevAEWq_Dc2YXcIJQ_horizon_summit_03_agenda_filtered.webp)](https://raytha.com/raytha/media-items/objectkey/4yhV7qevAEWq_Dc2YXcIJQ_horizon_summit_03_agenda_filtered.webp) | Agenda filtered to Day 2 and the AI & Data track |
| [![](https://raytha.com/raytha/media-items/objectkey/7im6mJtty0C5vwui7AkIWQ_horizon_summit_05_speakers.webp)](https://raytha.com/raytha/media-items/objectkey/7im6mJtty0C5vwui7AkIWQ_horizon_summit_05_speakers.webp) | Speaker directory |
| [![](https://raytha.com/raytha/media-items/objectkey/Bqd4lj7akEuHMkoHr_qFxg_horizon_summit_06_speaker_detail.webp)](https://raytha.com/raytha/media-items/objectkey/Bqd4lj7akEuHMkoHr_qFxg_horizon_summit_06_speaker_detail.webp) | Speaker page with their sessions |
| [![](https://raytha.com/raytha/media-items/objectkey/vKI0jwzZkEaxHU46A034bQ_horizon_summit_07_session_detail.webp)](https://raytha.com/raytha/media-items/objectkey/vKI0jwzZkEaxHU46A034bQ_horizon_summit_07_session_detail.webp) | Session page with Add to calendar |
| [![](https://raytha.com/raytha/media-items/objectkey/q5Jqwo9QyUGaN2PCEnQeUQ_horizon_summit_08_sponsors.webp)](https://raytha.com/raytha/media-items/objectkey/q5Jqwo9QyUGaN2PCEnQeUQ_horizon_summit_08_sponsors.webp) | Sponsors by tier |
| [![](https://raytha.com/raytha/media-items/objectkey/JssArsI_D0SGIcRkBsWorg_horizon_summit_11_search.webp)](https://raytha.com/raytha/media-items/objectkey/JssArsI_D0SGIcRkBsWorg_horizon_summit_11_search.webp) | Search results |
| [![](https://raytha.com/raytha/media-items/objectkey/UrnrGhdg0Uq-FmIKSyO4mw_horizon_summit_14_attendee_hub.webp)](https://raytha.com/raytha/media-items/objectkey/UrnrGhdg0Uq-FmIKSyO4mw_horizon_summit_14_attendee_hub.webp) | Attendee Hub, signed in as a member of `attendees` |
| [<img src="https://raytha.com/raytha/media-items/objectkey/9OLechcKZEi22T8pZFifcQ_horizon_summit_15_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/9OLechcKZEi22T8pZFifcQ_horizon_summit_15_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/vOgUj1AqTUGjqddrtyRlLg_horizon_summit_16_agenda_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/vOgUj1AqTUGjqddrtyRlLg_horizon_summit_16_agenda_mobile.webp) | Agenda on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/qq2rew6Br0yP41GAu0n4qw_horizon_summit_17_speaker_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/qq2rew6Br0yP41GAu0n4qw_horizon_summit_17_speaker_mobile.webp) | Speaker page on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
