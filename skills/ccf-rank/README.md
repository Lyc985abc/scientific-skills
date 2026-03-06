# ccf-rank

CCF 2026 venue rank lookup skill for conferences and journals.

## Install

```bash
npx skills add https://github.com/yorkeccak/scientific-skills --skill ccf-rank
```

## What it does

- Look up CCF rank (`A/B/C`) by venue abbreviation or full name
- Return venue type (`conference` or `journal`), area, publisher, and source URL
- Keep data in a local JSON dataset built from the official March 2026 CCF PDF

## Requirements

- Node.js 18+
- Python 3.10+ (only for dataset rebuild)
- `pypdf` (only for dataset rebuild)

## Usage

```bash
node scripts/query_ccf_rank.mjs "IJCAI"
node scripts/query_ccf_rank.mjs "IoT" --top 5
node scripts/query_ccf_rank.mjs "ICML" --type conference --rank A
```

## Rebuild dataset

```bash
python scripts/build_ccf_dataset.py \
  "/absolute/path/to/中国计算机学会推荐国际学术会议和期刊目录第七版（2026年3月更新）.pdf" \
  --out references/ccf_2026_rankings.json
```

If needed, add deleted venues to `references/excluded_venues.json` and rebuild.

## Files

- `SKILL.md`: skill trigger and runtime instructions
- `scripts/query_ccf_rank.mjs`: Node.js query entrypoint
- `scripts/build_ccf_dataset.py`: PDF-to-JSON builder
- `references/ccf_2026_rankings.json`: generated rank dataset
- `references/excluded_venues.json`: manual exclusion rules
