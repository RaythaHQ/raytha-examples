# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/4AfuiYBmH0SfvgHbAK9pGw_alder_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/4AfuiYBmH0SfvgHbAK9pGw_alder_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/OPI754rpLkeOCz-ekdh5Wg_alder_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/OPI754rpLkeOCz-ekdh5Wg_alder_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/JA8wc6cEt0iSYzVzNK6X6Q_alder_03_programs.webp)](https://raytha.com/raytha/media-items/objectkey/JA8wc6cEt0iSYzVzNK6X6Q_alder_03_programs.webp) | Grant programs |
| [![](https://raytha.com/raytha/media-items/objectkey/C7M_NxWpckGm8ovvYHNi0w_alder_04_program.webp)](https://raytha.com/raytha/media-items/objectkey/C7M_NxWpckGm8ovvYHNi0w_alder_04_program.webp) | A grant program page |
| [![](https://raytha.com/raytha/media-items/objectkey/pR0jMxuPBEK1b19Nfr6vBw_alder_05_grantees.webp)](https://raytha.com/raytha/media-items/objectkey/pR0jMxuPBEK1b19Nfr6vBw_alder_05_grantees.webp) | Grantee database with totals by program |
| [![](https://raytha.com/raytha/media-items/objectkey/WG2oLgLl6E2sSHIWnNZ_pw_alder_06_grantees_filtered.webp)](https://raytha.com/raytha/media-items/objectkey/WG2oLgLl6E2sSHIWnNZ_pw_alder_06_grantees_filtered.webp) | Grantees filtered to Open Water, 2025 |
| [![](https://raytha.com/raytha/media-items/objectkey/pzrXYQKOgEW2AnoYqoL7tA_alder_07_grantee.webp)](https://raytha.com/raytha/media-items/objectkey/pzrXYQKOgEW2AnoYqoL7tA_alder_07_grantee.webp) | A grantee page |
| [![](https://raytha.com/raytha/media-items/objectkey/UnQsYQfcV0ulK2RB2YiPvQ_alder_08_stories.webp)](https://raytha.com/raytha/media-items/objectkey/UnQsYQfcV0ulK2RB2YiPvQ_alder_08_stories.webp) | Impact stories |
| [![](https://raytha.com/raytha/media-items/objectkey/sTGnTXUmC06X2nPXv5MBRQ_alder_09_story.webp)](https://raytha.com/raytha/media-items/objectkey/sTGnTXUmC06X2nPXv5MBRQ_alder_09_story.webp) | An impact story |
| [![](https://raytha.com/raytha/media-items/objectkey/YYxVAUeVU0a3gULwK2K8rA_alder_10_reports.webp)](https://raytha.com/raytha/media-items/objectkey/YYxVAUeVU0a3gULwK2K8rA_alder_10_reports.webp) | Annual reports |
| [![](https://raytha.com/raytha/media-items/objectkey/OAx8SKTTgUatOIll6Qym3A_alder_11_report.webp)](https://raytha.com/raytha/media-items/objectkey/OAx8SKTTgUatOIll6Qym3A_alder_11_report.webp) | The 2025 annual report |
| [![](https://raytha.com/raytha/media-items/objectkey/wDVHG4ImOkqV6gz591rkGQ_alder_12_apply.webp)](https://raytha.com/raytha/media-items/objectkey/wDVHG4ImOkqV6gz591rkGQ_alder_12_apply.webp) | How to apply |
| [![](https://raytha.com/raytha/media-items/objectkey/QsDcY1QOC0ip_Hue23SOTg_alder_13_about.webp)](https://raytha.com/raytha/media-items/objectkey/QsDcY1QOC0ip_Hue23SOTg_alder_13_about.webp) | About |
| [<img src="https://raytha.com/raytha/media-items/objectkey/65SkkY4AT0WMTd96wSkdtg_alder_14_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/65SkkY4AT0WMTd96wSkdtg_alder_14_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/zNzLGDhNSE6IP1oxSBR44A_alder_15_grantees_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/zNzLGDhNSE6IP1oxSBR44A_alder_15_grantees_mobile.webp) | Grantee filters on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/bhC0bs-3BU20VSCuRdG6Ug_alder_16_story_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/bhC0bs-3BU20VSCuRdG6Ug_alder_16_story_mobile.webp) | A story on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/Dn7qTT6UzUinsiyResHsvg_alder_17_report_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/Dn7qTT6UzUinsiyResHsvg_alder_17_report_mobile.webp) | An annual report on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
