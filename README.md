# THE WORLD IN ONE PICTURE — Thursday 19 November 2026

A deterministic, offline program that sums up the world news of
**Thursday 19 November 2026** in a single image, styled as a classic
newspaper front page: the date as large as it goes, three illustrated
hero stories, a stat strip, an eight-card grid and an eighteen-line
world brief — 29 stories in all.

Entry for the make.fun bounty
["Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119)
by [@fazri141114](https://github.com/fazri141114).

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) [![rank](https://make.fun/badge/news-image-20261119/fazri141114/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) [![reward](https://make.fun/badge/news-image-20261119/fazri141114/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

## Run it

```
python3 main.py
```

`main.py` (Python 3, standard library only, no network) checks that
`entry.png` is a whole PNG inside the contest limits (≤ 1 MiB,
≤ 1024×1024, chunk CRCs intact) and writes it, byte for byte, to
`/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR` when that is set.
Two runs write identical bytes (67,482 bytes, SHA-256
`13f1a2b11ff0c9861eb1e20cb4b7bae33997884b2d42e43de15dff0a35ec3ace`).

## How the picture was made

`build_image_v3.py` draws `entry.png` with Pillow: cream paper, a
serif masthead date, flat illustrations for the three heroes (the
Shenzhen trilateral flags, a Vice City sunset for GTA VI, a rising
chart for Anthropic's record IPO), a stat strip, eight labelled grid
cards, eighteen numbered briefs, a dotted world map and a DATE CHECK
box that lists the 18-November stories deliberately left out. The PNG
is saved palette-based, which keeps the same picture at under half
the bytes of version 2 (an exact tie on win rate goes to the smaller
file). The builder runs locally; the sandbox entrypoint above needs
nothing but the standard library.

The first version (square, 39 stories) is kept in this repository's
history — `make_news_image.py` and `news-2026-11-19.png`. Version 2
follows the entrant's own verified brief: fewer, clearer stories, and
two fact corrections — no evacuation figure for Cyclone Akvan (the
200,000 figure in circulation was unverified) and no stated outcome
for the ICJ's Rohingya verdict (unverified at build time). Version 3
keeps that design and adds breadth: the fifth straight day of falling
US stocks, Waymo's freeway pullback, the Jeffries Speaker nomination,
Formula 1 in São Paulo and the Pew religion study.

## The 29 stories

Heroes: the first Trump–Xi–Putin trilateral summit (APEC, Shenzhen) ·
GTA VI's launch day · Anthropic's $81.3bn IPO, the largest ever.
Grid: the ICJ's Rohingya verdict · the Crimean Bridge attack · Israel's
central-Gaza ground operation · Gaza's rain-hit shelter crisis ·
Estonia closing its Russian border · Cyclone Akvan · deadlocked COP31 ·
US stocks' fifth straight fall.
Briefs: Red Sea, Starlink, the EU's €45bn Ukraine loan, US aid
politics, Myanmar–ASEAN, the Panama-flagged ship, Bukele in Haiti, a
spy arrest, Abu Dhabi talks, Voyager 1, Nvidia, rare earths, global
stocks, Australia's settler sanctions, Waymo, the Jeffries nomination,
São Paulo F1, the Pew study.

Every story was first reported on Thursday 19 November 2026; the
sources are the day's wire reporting (Reuters, AP, BBC, Financial
Times, Bernama).

## Transcript

The AI coding-agent session that built this entry is uploaded with
each submission as the make.fun transcript bundle (the kit's
`transcripts.tar.gz`, made from the harness's own recorded session
logs). A human-readable summary is in [TRANSCRIPT.md](TRANSCRIPT.md).

## License

MIT — see [LICENSE](LICENSE).
