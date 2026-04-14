import argparse
from grades_checker.services.analysis_flow import run_live
from grades_checker.services.analysis_flow import run_simulation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check FEU Tech honors eligibility from SOLAR grades.")
    parser.add_argument("--live", action="store_true", help="Run live scrape from SOLAR using browser login.")
    parser.add_argument("--simulate-cgpa", type=float, help="Simulate honors from a known CGPA.")
    parser.add_argument("--simulate-completed-units", type=float, help="Completed units for simulation mode.")
    parser.add_argument("--simulate-total-units", type=float, default=210.0, help="Total curriculum units for simulation mode.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.live:
        run_live()
        return

    if args.simulate_cgpa is not None and args.simulate_completed_units is not None:
        run_simulation(args.simulate_cgpa, args.simulate_completed_units, args.simulate_total_units)
        return

    raise SystemExit(
        "Use --live for scraping, or pass --simulate-cgpa and --simulate-completed-units for calculations."
    )


if __name__ == "__main__":
    main()
