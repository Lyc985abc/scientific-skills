---
name: ccf-rank
description: Query CCF (China Computer Federation) 2026 venue rankings for conferences and journals from the official March 2026 catalog. Use when users ask for CCF level (A/B/C), category/domain, or rank verification for a venue abbreviation/full name (for example ICML, CVPR, TOCS), or request batch lookup/comparison of multiple venues.
---

# ccf-rank

Use this skill to answer CCF 2026 ranking questions quickly and consistently.

## Data source

- Primary dataset: `references/ccf_2026_rankings.json`
- Source PDF used to build dataset: `中国计算机学会推荐国际学术会议和期刊目录第七版（2026年3月更新）.pdf`
- Manual exclusion list for deleted entries: `references/excluded_venues.json`

## Query workflow

1. Run the lookup script with Node.js (preferred for installable skill compatibility):
   ```bash
   node scripts/query_ccf_rank.mjs "<venue name>"
   ```
2. For ambiguous venue names, narrow by type/rank:
   ```bash
   node scripts/query_ccf_rank.mjs "<query>" --type conference --rank A --top 20
   ```
3. If user asks for several venues, run the script per venue and return a compact table with: `venue`, `type`, `rank`, `area`, `url`.
4. If there are multiple high-score matches, show the top matches and explicitly ask user to disambiguate.

## Output rules

- Always include `type` (`conference` or `journal`) and `rank` (`A/B/C`).
- Include the CCF `area` category when available.
- Include the canonical venue name and DBLP URL from the dataset.
- If no confident match is found, say so explicitly and list closest candidates.

## Update workflow (new CCF version)

1. Replace the PDF file with the newer official CCF version.
2. Rebuild dataset:
   ```bash
   python scripts/build_ccf_dataset.py "/absolute/path/to/new.pdf" --out references/ccf_2026_rankings.json
   ```
3. Update `references/excluded_venues.json` if the PDF has deleted entries that text extraction cannot reliably detect from styling.
4. Spot-check representative venues (for example `ICML`, `NeurIPS`, `CVPR`, `TOCS`) using `query_ccf_rank.mjs`.
