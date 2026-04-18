# Schedule Checker

## What It Does

- Uses cached grades and availability data.
- For regular students, targets the next term after latest graded term.
- Uses curriculum term blocks to choose target subjects.
- Matches target subjects to course offerings sections.

## Commands

```bash
schedule-checker --group-size 3 --image-output src/.cache/schedule_report.png
```

```bash
grades-checker --schedule --group-size 3 --image-output src/.cache/schedule_report.png
```

## Cache Behavior

- If availability cache exists, schedule checker uses it without logging in.
- If availability cache is missing, it scrapes once and saves new availability cache.
