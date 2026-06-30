# Grades Checker (FEU Tech SOLAR)

Tooling for FEU Tech SOLAR scraping and analysis:

- grades/honors analysis
- schedule availability checker
- PNG schedule report generation
- optional professor mapping from Excel

## Quick Start

```bash
pip install -r requirements.txt
playwright install chromium
```

```bash
grades-checker --live
schedule-checker --group-size 3 --image-output src/.cache/schedule_report.png
```

## Docs

See the docs folder:

- [docs/index.md](docs/index.md)
- [docs/getting-started.md](docs/getting-started.md)
- [docs/schedule-checker.md](docs/schedule-checker.md)
- [docs/professor-excel.md](docs/professor-excel.md)
- [docs/configuration.md](docs/configuration.md)

## Architecture (UML)

```mermaid
graph TD
    CLI["CLI Entry<br/>cli.py"]
    AnalysisFlow["Analysis Flow<br/>analysis_flow.py"]
    ScheduleFlow["Schedule Flow<br/>schedule_flow.py"]
    
    PlaywrightScraper["Playwright Scraper<br/>Web Automation"]
    DataAnalyzer["Data Analyzer<br/>grades/honors processing"]
    ReportGen["Report Generator<br/>PNG output"]
    
    ConfigModule["Config<br/>settings.py"]
    
    CLI -->|loads config| ConfigModule
    CLI -->|invokes| AnalysisFlow
    CLI -->|invokes| ScheduleFlow
    
    AnalysisFlow -->|uses| PlaywrightScraper
    AnalysisFlow -->|processes| DataAnalyzer
    
    ScheduleFlow -->|uses| PlaywrightScraper
    ScheduleFlow -->|outputs| ReportGen
    
    ConfigModule -->|shared| PlaywrightScraper
    ConfigModule -->|shared| DataAnalyzer
```

## Tech Stack

- **Python 3.10+**: Core language
- **Playwright**: Web scraping & automation
- **Rich**: CLI output formatting
- **Pillow**: Image processing
- **openpyxl**: Excel parsing
