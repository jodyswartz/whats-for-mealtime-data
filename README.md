# whats-for-mealtime-data

## Description
This repository stores:

- **Raw data** exported from Astro’s Journal (`rawdata/`)
- **Formatted data** used by graph/chart apps (`formatteddata/`)

A GitHub Action runs on pushes to `main` that change `rawdata/**/*.json`:
1. Validates the changed raw JSON file(s)
2. Runs the formatter
3. Writes/updates the yearly output in `formatteddata/`

---

## File Structure

```

.
├── formatteddata/
│   ├── 2023_bargraph.json
│   ├── 2024_bargraph.json
│   ├── 2025_bargraph.json
│   └── 2026_bargraph.json
├── rawdata/
│   ├── 2023/
│   │   ├── astro_journal_2023_11_03.json
│   │   └── astro_journal_2023_11_09.json
│   ├── 2024/
│   │   └── ...
│   ├── 2025/
│   │   └── ...
│   └── 2026/
│       └── ...
├── .github/
│   ├── scripts/
│   │   └── validate_rawdata.py
│   └── workflows/
│       └── format-rawdata.yml
├── LICENSE
└── README.md

````

> Note: Raw files are expected to be placed under `rawdata/<YEAR>/...json` so the workflow can derive which year to regenerate.

---

## Raw Data Format

Each file under `rawdata/<YEAR>/` should be a JSON array of entries shaped like:

```json
[
  { "date": "2026-01-09", "name": "Breakfast", "amount": "1" },
  { "date": "2026-01-09", "name": "Lunch", "amount": "2" }
]
````

Validation checks (at minimum):

* top-level is a non-empty list
* each entry has `date`, `name`, `amount`
* `date` is `YYYY-MM-DD`
* `amount` is integer-like (e.g. `"3"` or `3`)

---

## Formatted Data Format

The formatter generates yearly Chart.js JSON files:

* `formatteddata/<YEAR>_bargraph.json`

Format:

```json
{
  "labels": ["January", "February", "...", "December"],
  "datasets": [
    {
      "label": "Some Name",
      "data": [0, 3, 1, 5, 0, 2, 7, 1, 0, 4, 2, 6],
      "backgroundColor": "#FBBB62",
      "borderColor": "rgba(255,99,132,1)",
      "borderWidth": 1
    }
  ]
}
```

---

## Automation: Validate + Generate formatteddata

On push to `main` for changes to `rawdata/**/*.json`, the workflow:

* detects changed raw JSON file(s)
* validates the changed file
* checks out the private formatter repo
* regenerates `formatteddata/<YEAR>_bargraph.json` for the year derived from the rawdata path
* commits the updated formatted file back to this repo

### Required repo secret

Because the formatter repo is private, the workflow requires a repo secret:

* `FORMATTER_REPO_TOKEN` (fine-grained PAT with **read** access to the formatter repo)

---

## Apps which use this data

* What’s for Mealtime Graph (private): [https://github.com/jodyswartz/whats-for-mealtime-graph](https://github.com/jodyswartz/whats-for-mealtime-graph)
