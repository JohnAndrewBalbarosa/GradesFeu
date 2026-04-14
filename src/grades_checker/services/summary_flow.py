from grades_checker.config.settings import AppSettings
from grades_checker.config.settings import honor_targets_from_settings
from grades_checker.models.entities import ScrapedSnapshot
from grades_checker.scraping.curriculum_scraper import CurriculumScraper
from grades_checker.scraping.grades_scraper import GradesScraper
from grades_checker.scraping.session import managed_page
from grades_checker.services.analyzer import GradeAnalyzerService


def scrape_live_snapshot() -> ScrapedSnapshot:
    with managed_page(headless=False) as page:
        grades_scraper = GradesScraper(page)
        curriculum_scraper = CurriculumScraper(page)
        service = GradeAnalyzerService(grades_scraper, curriculum_scraper)
        return service.run_live_snapshot()


def build_summary(snapshot: ScrapedSnapshot, settings: AppSettings):
    return GradeAnalyzerService.build_summary(
        course_grades=snapshot.course_grades,
        curriculum_courses=snapshot.curriculum_courses,
        term_labels=snapshot.term_labels,
        honor_targets=honor_targets_from_settings(settings),
    )
