# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/yxBjCaWwv02PaLCf2EC_gg_orbitly_help_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/yxBjCaWwv02PaLCf2EC_gg_orbitly_help_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/O4JE1qXh10SzSX39EPbeMg_orbitly_help_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/O4JE1qXh10SzSX39EPbeMg_orbitly_help_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/N3Kh2HVnXEWuOBg601p2yw_orbitly_help_03_instant_search.webp)](https://raytha.com/raytha/media-items/objectkey/N3Kh2HVnXEWuOBg601p2yw_orbitly_help_03_instant_search.webp) | Search as you type |
| [![](https://raytha.com/raytha/media-items/objectkey/ZpRs6yt9K0Cm6fH6sK0Frg_orbitly_help_04_category.webp)](https://raytha.com/raytha/media-items/objectkey/ZpRs6yt9K0Cm6fH6sK0Frg_orbitly_help_04_category.webp) | A topic page |
| [![](https://raytha.com/raytha/media-items/objectkey/0CpzhI8efE-yE3uMxg8MpQ_orbitly_help_05_article.webp)](https://raytha.com/raytha/media-items/objectkey/0CpzhI8efE-yE3uMxg8MpQ_orbitly_help_05_article.webp) | Article page |
| [![](https://raytha.com/raytha/media-items/objectkey/rr35TkDYWEuFP2UgL_4iKg_orbitly_help_06_search_results.webp)](https://raytha.com/raytha/media-items/objectkey/rr35TkDYWEuFP2UgL_4iKg_orbitly_help_06_search_results.webp) | Search results for "calendar" |
| [![](https://raytha.com/raytha/media-items/objectkey/yFuNSOvQGEqgGm3LJz4pUQ_orbitly_help_07_tag_filter.webp)](https://raytha.com/raytha/media-items/objectkey/yFuNSOvQGEqgGm3LJz4pUQ_orbitly_help_07_tag_filter.webp) | Articles tagged Security |
| [![](https://raytha.com/raytha/media-items/objectkey/XZYt6xIhKkigDeDfqOSTvg_orbitly_help_08_topics.webp)](https://raytha.com/raytha/media-items/objectkey/XZYt6xIhKkigDeDfqOSTvg_orbitly_help_08_topics.webp) | All topics |
| [![](https://raytha.com/raytha/media-items/objectkey/YmP4nu8JKkG35O9HA51mUA_orbitly_help_09_changelog.webp)](https://raytha.com/raytha/media-items/objectkey/YmP4nu8JKkG35O9HA51mUA_orbitly_help_09_changelog.webp) | Changelog |
| [![](https://raytha.com/raytha/media-items/objectkey/EYD3o9oCN0aMvSdfGLcplQ_orbitly_help_10_status.webp)](https://raytha.com/raytha/media-items/objectkey/EYD3o9oCN0aMvSdfGLcplQ_orbitly_help_10_status.webp) | Status page |
| [<img src="https://raytha.com/raytha/media-items/objectkey/IBOejFjsvkWm0U1EBEKy1Q_orbitly_help_11_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/IBOejFjsvkWm0U1EBEKy1Q_orbitly_help_11_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/l7FF08y54UqwtV2Ij-9ZTQ_orbitly_help_12_article_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/l7FF08y54UqwtV2Ij-9ZTQ_orbitly_help_12_article_mobile.webp) | Article on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
