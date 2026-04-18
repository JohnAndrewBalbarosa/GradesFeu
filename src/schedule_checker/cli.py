import argparse

from grades_checker.services.schedule_flow import run_schedule_from_cache


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("group size must be at least 1")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check available sections for latest-term subjects using cached grades and SOLAR offerings."
    )
    parser.add_argument("--group-size", type=_positive_int, required=True, help="Number of students in your group.")
    parser.add_argument("--image-output", default=".cache/schedule_report.png", help="PNG path for schedule visual output.")
    parser.add_argument("--prof-excel", help="Optional XLSX file containing subject/section professor assignments.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_schedule_from_cache(
        group_size=args.group_size,
        image_output=args.image_output,
        prof_excel_path=args.prof_excel,
    )


if __name__ == "__main__":
    main()
