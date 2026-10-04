# Screenshots

A curated set, captured at 1440px (desktop) and 390px (phone) from a site built with `../build.sh`.
The images are hosted in the raytha.com media library. Click one for the full-size file.

| Screenshot | Shows |
|------------|-------|
| [![](https://raytha.com/raytha/media-items/objectkey/obNNiviyJkemqFMYRWLrrw_brightwell_dme_01_home_hero.webp)](https://raytha.com/raytha/media-items/objectkey/obNNiviyJkemqFMYRWLrrw_brightwell_dme_01_home_hero.webp) | Home, above the fold |
| [![](https://raytha.com/raytha/media-items/objectkey/QKJOn5CKNU6ZXMDFW3glKQ_brightwell_dme_02_home_full.webp)](https://raytha.com/raytha/media-items/objectkey/QKJOn5CKNU6ZXMDFW3glKQ_brightwell_dme_02_home_full.webp) | Home, full page |
| [![](https://raytha.com/raytha/media-items/objectkey/3kFp9p_2ekS6KN5TWLQWfg_brightwell_dme_03_equipment.webp)](https://raytha.com/raytha/media-items/objectkey/3kFp9p_2ekS6KN5TWLQWfg_brightwell_dme_03_equipment.webp) | Equipment categories |
| [![](https://raytha.com/raytha/media-items/objectkey/KgpkNAyfjkCr346Lq1XbGw_brightwell_dme_04_catalog.webp)](https://raytha.com/raytha/media-items/objectkey/KgpkNAyfjkCr346Lq1XbGw_brightwell_dme_04_catalog.webp) | Equipment catalog with filters |
| [![](https://raytha.com/raytha/media-items/objectkey/SdaASxPg90OVY8ou7u7kZQ_brightwell_dme_05_product.webp)](https://raytha.com/raytha/media-items/objectkey/SdaASxPg90OVY8ou7u7kZQ_brightwell_dme_05_product.webp) | A product page |
| [![](https://raytha.com/raytha/media-items/objectkey/OpAXyuyFb0iWxvXpE1fFZw_brightwell_dme_06_category.webp)](https://raytha.com/raytha/media-items/objectkey/OpAXyuyFb0iWxvXpE1fFZw_brightwell_dme_06_category.webp) | A category page |
| [![](https://raytha.com/raytha/media-items/objectkey/kTkpcam4a0-PDXkMM8JNHg_brightwell_dme_07_how_to_order.webp)](https://raytha.com/raytha/media-items/objectkey/kTkpcam4a0-PDXkMM8JNHg_brightwell_dme_07_how_to_order.webp) | How to order |
| [![](https://raytha.com/raytha/media-items/objectkey/LMlxNLQ2yE6-tovlpZzGIA_brightwell_dme_08_resource.webp)](https://raytha.com/raytha/media-items/objectkey/LMlxNLQ2yE6-tovlpZzGIA_brightwell_dme_08_resource.webp) | A patient guide |
| [![](https://raytha.com/raytha/media-items/objectkey/Ue8Vcs4SEk6SvL0LQ2IXKg_brightwell_dme_09_faq.webp)](https://raytha.com/raytha/media-items/objectkey/Ue8Vcs4SEk6SvL0LQ2IXKg_brightwell_dme_09_faq.webp) | Frequently asked questions |
| [![](https://raytha.com/raytha/media-items/objectkey/yTTXDSXpbkWxI1htEcsHXg_brightwell_dme_10_locations.webp)](https://raytha.com/raytha/media-items/objectkey/yTTXDSXpbkWxI1htEcsHXg_brightwell_dme_10_locations.webp) | Locations |
| [![](https://raytha.com/raytha/media-items/objectkey/ayYOE61IEkeKnFQjp7D2OA_brightwell_dme_11_contact.webp)](https://raytha.com/raytha/media-items/objectkey/ayYOE61IEkeKnFQjp7D2OA_brightwell_dme_11_contact.webp) | Contact |
| [<img src="https://raytha.com/raytha/media-items/objectkey/iqHcj2Zo2EqiuLj-H_XE3g_brightwell_dme_12_home_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/iqHcj2Zo2EqiuLj-H_XE3g_brightwell_dme_12_home_mobile.webp) | Home on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/5x86ZGnNd0GIPK53m2DfWQ_brightwell_dme_13_product_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/5x86ZGnNd0GIPK53m2DfWQ_brightwell_dme_13_product_mobile.webp) | A product on a phone |
| [<img src="https://raytha.com/raytha/media-items/objectkey/owkh6OVPNkSTpUYrdSomoQ_brightwell_dme_14_locations_mobile.webp" width="200">](https://raytha.com/raytha/media-items/objectkey/owkh6OVPNkSTpUYrdSomoQ_brightwell_dme_14_locations_mobile.webp) | Locations on a phone |

To capture your own (PNG, into this folder):

```bash
pip install playwright && playwright install chromium
BASE_URL=http://localhost:5001 python3 ../../scripts/capture-screenshots.py ../shots.json .
```
