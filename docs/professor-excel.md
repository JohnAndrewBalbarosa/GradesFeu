# Professor Excel Mapping

## Feature

You can provide an XLSX file to enrich schedule output with professor names.

## Usage

```bash
schedule-checker --group-size 3 --prof-excel path/to/file.xlsx
```

```bash
grades-checker --schedule --group-size 3 --prof-excel path/to/file.xlsx
```

## Expected Columns

The parser auto-detects headers using keywords:

- Course/Subject/Code
- Section/Sec
- Prof/Instructor/Faculty/Teacher

It supports multi-sheet files and uses:

- exact match: course + section
- fallback match: course only

## Notes

- Supported formats: .xlsx, .xlsm
- If the file is missing, command returns an error.
