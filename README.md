# Grades Checker (FEU Tech SOLAR)

A modular Python tool that:
- Logs into SOLAR via browser
- Scrapes Grade Report terms in chronological order (first available term to latest)
- Scrapes Program Curriculum
- Saves scraped data locally to avoid repeated sign-in
- Computes weighted CGPA
- Estimates honors eligibility (Summa, Magna, Cum Laude)
- Runs outlier-based term analysis and projected honors without low outliers
- Marks failed-subject records as automatic Latin-honors disqualification
- Simulates a what-if path where failed subjects are replaced by baseline performance
- Prints sentence-form guidance

## Architecture

The project follows decoupling principles with separated logic:
- `src/grades_checker/config`: `.env` settings and thresholds
- `src/grades_checker/scraping`: page navigation and data extraction
- `src/grades_checker/logic`: pure GPA and honors formulas
- `src/grades_checker/models`: dataclasses
- `src/grades_checker/services`: orchestration/service layer
- `src/grades_checker/cli.py`: CLI entrypoint
- `src/main.py`: interactive menu (cache/source/analysis)
- `tests`: calculation tests

## Install

```bash
pip install -r requirements.txt
playwright install chromium
```

Or with project metadata:

```bash
pip install -e .
pip install -e .[dev]
playwright install chromium
```

## Run Live Scrape

```bash
grades-checker --live
```

Or:

```bash
python -m grades_checker.cli --live
```

When the browser opens, sign in to Microsoft, then return to terminal and press Enter.
After scraping, the program asks for only one input: your current CGPA.
If you just press Enter, it uses the CGPA computed from the scraped grade table.

## Run Interactive Menu

```bash
python src/main.py
```

Flow in the menu:
1. Pick data source: use saved data or login and refresh.
2. Run one of the analysis options:
	- Honors check (current CGPA input)
	- Previous performance summary by term
	- Outlier-based projection per term
	- Manual simulation

## Run Simulation

Example for your 3rd year 1st term scenario:

```bash
grades-checker --simulate-cgpa 3.333 --simulate-completed-units 135 --simulate-total-units 210
```

## Formula

For a target cumulative GPA:

required_average = (target_gpa * total_units - current_cgpa * completed_units) / remaining_units

where:
- `remaining_units = total_units - completed_units`

## Environment Variables

Copy `.env.example` to `.env` and edit values.

Main keys:
- `HONOR_SUMMA_MIN`, `HONOR_MAGNA_MIN`, `HONOR_CUM_MIN`
- `HONOR_SUMMA_MAX`, `HONOR_MAGNA_MAX`, `HONOR_CUM_MAX`
- `OUTLIER_METHOD` (`mad` or `iqr`)
- `OUTLIER_TAIL` (`left`) for low-grade outliers only
- `OUTLIER_Z_THRESHOLD`
- `BASELINE_ESTIMATOR` (`trimmed_mean` or `median`)
- `FAILED_GRADE_VALUES` (comma-separated, default `5.0,9.0`)
- `CACHE_ENABLED`
- `CACHE_FILE`

## Test

```bash
pytest
```
