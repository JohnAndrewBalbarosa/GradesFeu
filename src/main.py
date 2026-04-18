from grades_checker.config.settings import load_settings
from grades_checker.config.settings import AppSettings
from grades_checker.models.entities import ScrapedSnapshot
from grades_checker.services.analysis_flow import run_honors_from_snapshot
from grades_checker.services.analysis_flow import run_outlier_report
from grades_checker.services.analysis_flow import run_performance_report
from grades_checker.services.analysis_flow import run_simulation
from grades_checker.services.analysis_flow import scrape_live_snapshot_and_cache_availability
from grades_checker.services.cache_service import CacheService
from grades_checker.services.schedule_flow import run_schedule_from_cache


def _print_data_source_menu(has_cache: bool) -> None:
    print("Data Source")
    if has_cache:
        print("1. Use saved data")
        print("2. Login and refresh data")
        print("3. Exit")
    else:
        print("1. Login and scrape now")
        print("2. Exit")


def _print_analysis_menu() -> None:
    print()
    print("Analysis Options")
    print("1. Honors check (with current CGPA input)")
    print("2. Previous performance summary")
    print("3. Outlier-based projection")
    print("4. Simulation mode")
    print("5. Schedule checker (latest-term subjects)")
    print("6. Exit")


def _get_snapshot(
    cache_service: CacheService,
    has_cache: bool,
    cache_enabled: bool,
    settings: AppSettings,
) -> ScrapedSnapshot | None:
    while True:
        _print_data_source_menu(has_cache)
        choice = input("Choose an option: ").strip()

        if has_cache:
            if choice == "1":
                snapshot = cache_service.load_snapshot()
                print(f"Loaded saved data scraped at {snapshot.scraped_at_utc}")
                return snapshot
            if choice == "2":
                snapshot = scrape_live_snapshot_and_cache_availability(settings)
                if cache_enabled:
                    cache_service.save_snapshot(snapshot)
                    print("Saved latest scraped data to cache.")
                    print(f"Saved availability cache to {settings.availability_cache_file}")
                return snapshot
            if choice == "3":
                return None
            print("Invalid option. Please choose 1, 2, or 3.")
            continue

        if choice == "1":
            snapshot = scrape_live_snapshot_and_cache_availability(settings)
            if cache_enabled:
                cache_service.save_snapshot(snapshot)
                print("Saved latest scraped data to cache.")
                print(f"Saved availability cache to {settings.availability_cache_file}")
            return snapshot
        if choice == "2":
            return None
        print("Invalid option. Please choose 1 or 2.")


def main() -> None:
    settings = load_settings()
    cache_service = CacheService(settings.cache_file)
    has_cache = settings.cache_enabled and cache_service.exists()

    snapshot = _get_snapshot(cache_service, has_cache, settings.cache_enabled, settings)
    if snapshot is None:
        print("Goodbye.")
        return

    while True:
        _print_analysis_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            run_honors_from_snapshot(snapshot, settings)
            continue

        if choice == "2":
            run_performance_report(snapshot)
            continue

        if choice == "3":
            run_outlier_report(snapshot, settings)
            continue

        if choice == "4":
            cgpa = float(input("Enter current CGPA: ").strip())
            completed_units = float(input("Enter completed units: ").strip())
            total_units_raw = input("Enter total curriculum units (default 210): ").strip()
            total_units = float(total_units_raw) if total_units_raw else 210.0
            run_simulation(cgpa, completed_units, total_units)
            continue

        if choice == "5":
            group_size = int(input("Enter number of students in your group: ").strip())
            if group_size < 1:
                print("Group size must be at least 1.")
                print()
                continue
            image_output = input("Image output path (default .cache/schedule_report.png): ").strip()
            prof_excel = input("Professor Excel path (optional): ").strip()
            run_schedule_from_cache(
                group_size=group_size,
                image_output=image_output or ".cache/schedule_report.png",
                prof_excel_path=prof_excel or None,
            )
            continue

        if choice == "6":
            print("Goodbye.")
            return

        print("Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")
        print()


if __name__ == "__main__":
    main()
