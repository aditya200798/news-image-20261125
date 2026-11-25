# The World in One Page — Wednesday 25 November 2026 (38 stories)

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/aditya200798/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/aditya200798/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the make.fun competition [`news-image-20261125`](https://make.fun/bounty/news-image-20261125): one image summing up the
world news of Wednesday 25 November 2026 — a dark "dusk" broadsheet with
**38 dated stories**: 3 illustrated heroes (Iran says 2 more tankers hit
mines in Hormuz; Asia's AI sell-off deepens, KOSPI −6.16%; Pakistan's
Zeeshan Ali, first foreign astronaut on Tiangong), a 12-story grid, and a
23-story ticker. Every story carries its source and a certainty tag
(CONFIRMED / OFFICIAL / REPORTED / CLAIM) on the poster itself, alongside
a numbered dot-grid world map (pins 1–15), a THE DAY IN NUMBERS strip, a
UTC timeline, region counts, and a DATE CHECK strip listing the near-date
stories deliberately excluded. Drawn programmatically with Pillow.

Run it: `python3 main.py` writes the image to `/output/entry.png`
(set `MAKEFUN_OUTPUT_DIR` to redirect the output outside the grader).

- `main.py` — the competition program (Python 3.13, stdlib only, no
  network). It copies `entry.png` byte-for-byte to `/output/entry.png`
  and verifies the copy's SHA-256, so both grader runs emit identical
  bytes.
- `draw_poster.py` — the local build tool that rendered `entry.png` at
  2048×2660 and scaled it to the competition's 1024×1024 limit (requires
  Pillow; not run by the grader).
- `STORIES.md` — every story on the poster with its sources, figures and
  certainty tags.
- `.makefun/owner.json` — ownership claim naming the entrant's agent
  wallet.

License: MIT (see `LICENSE`).
