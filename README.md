# THE WORLD IN ONE PICTURE — Thursday 19 November 2026

A deterministic, offline program that sums up the world news of
**Thursday 19 November 2026** in a single image, styled as a vintage
newspaper front page.

Entry for the make.fun bounty
["Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119)
by [@fazri141114](https://github.com/fazri141114).

## Output

- `news-2026-11-19.png` — 1024 × 1024 PNG, 214,396 bytes (limit: 1 MiB)
- SHA-256: `b0f41dcea1c572efb0d853c0bf8ec6357016007343ddfe81e9011731ec706ebf`

## Run it

```bash
python3 make_news_image.py            # writes news-2026-11-19.png
python3 make_news_image.py out.png    # or any output path
```

Requires Python 3 and Pillow (`pip install Pillow`). Serif fonts used:
Noto Serif Display, Liberation Serif, Liberation Sans (standard on Linux).

## Determinism

The program uses **no network, no randomness and no clock**. All content
is fixed data in the source file. Run it twice and compare:

```bash
python3 make_news_image.py a.png
python3 make_news_image.py b.png
sha256sum a.png b.png   # identical hashes
```

## What's in the picture

39 stories from 6 continents, all first reported on 19 November 2026:

- **3 heroes:** the first Trump–Xi–Putin trilateral summit in Shenzhen;
  the GTA VI launch after a 13-year wait (99 Metacritic, 15.9m pre-orders);
  Anthropic's Nasdaq debut in the largest IPO in history (~$81bn raised).
- A stat strip, a dotted world map with numbered pins, and 36 numbered
  briefs covering the World Court's Rohingya ruling, COP31's final 48
  hours, Cyclone Akvan, the Van Gogh auction record, Voyager 1's
  one-light-day milestone, and more.
- A **DATE CHECK** footer lists stories deliberately *excluded* because
  they were first reported on 18 November or earlier (e.g. Anthropic's
  $83 pricing, set 18 Nov — the 19 Nov story is the trading debut).

Story selection was verified against the day's wire reporting
(AP news summary of 19 Nov 2026 and same-day headline roundups).

## Files

- `make_news_image.py` — the whole program (data + renderer)
- `news-2026-11-19.png` — the generated entry image
- `TRANSCRIPT.md` — transcript of the AI coding agent session that built this

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/fazri141114/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/fazri141114/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
