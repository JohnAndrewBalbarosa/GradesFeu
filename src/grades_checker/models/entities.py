from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class CourseGrade:
    term_label: str
    course_code: str
    course_title: str
    units: float
    final_grade: float


@dataclass(frozen=True)
class TermOption:
    label: str
    value: str


@dataclass(frozen=True)
class CurriculumCourse:
    course_code: str
    course_title: str
    units: float


@dataclass(frozen=True)
class HonorResult:
    honor_name: str
    target_gpa: float
    qualified_now: bool
    needed_average_for_remaining_units: float
    reachable: bool


@dataclass(frozen=True)
class AnalysisSummary:
    current_cgpa: float
    completed_units: float
    total_curriculum_units: float
    remaining_units: float
    term_labels: List[str]
    first_term_label: str
    latest_term_label: str
    honors: List[HonorResult]


@dataclass(frozen=True)
class ScrapedSnapshot:
    scraped_at_utc: str
    term_labels: List[str]
    course_grades: List[CourseGrade]
    curriculum_courses: List[CurriculumCourse]
