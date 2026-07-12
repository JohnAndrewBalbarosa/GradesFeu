# GradesFeu

## Overview

FEU Tech SOLAR grades and schedule analysis tool

Repository: [JohnAndrewBalbarosa/GradesFeu](https://github.com/JohnAndrewBalbarosa/GradesFeu)

## Problem and Goal

**Problem.** FEU Tech students manually combine SOLAR grade and schedule data to estimate standing, honors eligibility, and available time.

**Goal.** Collect the student’s own rendered SOLAR data, normalize grades/schedules, calculate academic summaries, and generate reviewable reports.

## System Design

- `src/grades_checker/`: grade collection, normalization, calculations, and CLI.
- `src/schedule_checker/`: schedule collection and availability analysis.
- Playwright: rendered SOLAR access; Rich: CLI output; Pillow: images; OpenPyXL: workbook mappings.
- `tests/`: offline verification of calculations and flows.

## Setup and Usage

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python -m grades_checker.cli --help
python -m schedule_checker.cli --help
```

## Evaluation Method

- Define the project task and expected behavior.
- Run representative examples or user flows.
- Record correctness, speed, reliability, usability, and failure cases.

## Results

- No validated quantitative results are published yet.
- Current README status: implementation and usage are documented before formal measurement.

## Interpretation

- The project can be described as implemented or in progress, but impact claims should stay limited until measurements are collected.
- Use the evaluation plan below to turn the project into resume-ready, evidence-backed work.

## Limitations

- Results should only be treated as validated when this README includes the dataset, sample size, metric definition, and reproduction steps.
- Any AI-generated, OCR-based, scraped, or heuristic output requires manual review before being used as ground truth.
- Environment-dependent measurements such as latency, memory use, browser behavior, and API reliability should be re-measured on the target machine.

## Recommendations and Future Work

- Number of grade records parsed correctly.
- Forecast accuracy or error rate if prediction is enabled.
- Time saved compared with manual spreadsheet work.

## Documentation Standard

This README follows a technical-project structure: overview, goal, system design, setup, evaluation method, results, interpretation, limitations, and recommendations. Update the Results section whenever new measurements are available so project claims stay evidence-backed.
