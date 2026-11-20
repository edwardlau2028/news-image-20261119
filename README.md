# The World in One Day — 19 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-news--image--20261119-blue)](https://make.fun/c/news-image-20261119)
[![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

A one-page newspaper front page summing up the world's news of Thursday
19 November 2026 — eight stories, drawn in code with Python and PIL, on a
single 1024×1024 image.

## The eight stories

1. **Summit** — Trump, Xi and Putin hold first three-way summit. Leaders issue
   a "peace declaration" in Shenzhen; no Ukraine deal, no arms cuts.
2. **Justice** — World court: Myanmar committed genocide. ICJ rules the 2017
   crackdown on the Rohingya was state-sponsored genocide.
3. **Middle East** — Houthi missile hits Riyadh's tallest tower. PIF Tower
   windows blown out across seven floors; no injuries reported.
4. **Asia** — Bangladesh lockdown turns violent. Four killed in clashes; Nobel
   laureate Yunus's family home set on fire.
5. **Markets** — Anthropic debuts in record $81bn IPO. Shares open on Nasdaq
   as ANT; largest listing ever, valued near $1.5tn.
6. **Europe** — Denmark backs Greenland deal 109–0. Parliament approves U.S.
   security pact; more bases, Danish sovereignty kept.
7. **Americas** — U.S. and Venezuela sign military pact. Hegseth visits
   Caracas; joint training and intelligence sharing agreed.
8. **Migration** — Migrant boat capsizes off Senegal. Dozens missing after a
   boat carrying 50–100 people overturns near Yenne.

Sources: Reuters, AP, USA Today, Defense News, BBC, NDTV.

## How it runs

`draw_news.py` renders `entry.png` (1024×1024, under 1 MiB) from the story
list above, with a greedy word wrap and assertions that no headline runs
past three lines, no summary past two, and nothing overflows its card.
`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).

```sh
python3 draw_news.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Repository: https://github.com/edwardlau2028/news-image-20261119

License: MIT — see [LICENSE](./LICENSE).
