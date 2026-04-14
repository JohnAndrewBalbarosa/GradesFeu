import re
from typing import List

from playwright.sync_api import Page

from grades_checker.config.settings import load_settings
from grades_checker.models.entities import CurriculumCourse

COURSE_CODE_PATTERN = re.compile(r"([A-Z]{2,}\d|NSTP|OJT|THS)")


class CurriculumScraper:
    def __init__(self, page: Page, curriculum_url: str | None = None) -> None:
        self.page = page
        self.curriculum_url = curriculum_url or load_settings().curriculum_url

    def open(self) -> None:
        self.page.goto(self.curriculum_url, wait_until="domcontentloaded")

    def scrape_courses(self) -> List[CurriculumCourse]:
        rows = self.page.locator("table tbody tr")
        courses: List[CurriculumCourse] = []

        for idx in range(rows.count()):
            cols = rows.nth(idx).locator("td")
            if cols.count() < 3:
                continue

            code = cols.nth(0).inner_text().strip()
            title = cols.nth(1).inner_text().strip()
            units_text = cols.nth(2).inner_text().strip()

            if not COURSE_CODE_PATTERN.search(code):
                continue

            try:
                units = float(units_text)
            except ValueError:
                continue

            courses.append(
                CurriculumCourse(course_code=code, course_title=title, units=units)
            )

        return courses
