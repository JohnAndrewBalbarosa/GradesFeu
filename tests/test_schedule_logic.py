from grades_checker.logic.schedule import group_sections_for_subjects
from grades_checker.logic.schedule import latest_term_subject_codes
from grades_checker.logic.schedule import choose_offerings_term_and_year
from grades_checker.models.entities import CourseGrade
from grades_checker.models.entities import CourseOfferingSection
from grades_checker.models.entities import EnrollmentStatus


def test_latest_term_subject_codes_uses_latest_label() -> None:
    grades = [
        CourseGrade("1 - 20242025", "MATH101", "Math 1", 3.0, 3.0),
        CourseGrade("2 - 20242025", "COMP201", "Comp 2", 3.0, 3.5),
        CourseGrade("2 - 20242025", "COMP201", "Comp 2", 3.0, 3.5),
        CourseGrade("2 - 20242025", "ENG202", "Eng 2", 3.0, 3.0),
    ]

    codes = latest_term_subject_codes(grades, ["1 - 20242025", "2 - 20242025"])
    assert codes == ["COMP201", "ENG202"]


def test_group_sections_for_subjects_filters_by_group_size() -> None:
    offerings = [
        CourseOfferingSection("COMP201", "S11", 5, "row1"),
        CourseOfferingSection("COMP201", "S12", 1, "row2"),
        CourseOfferingSection("ENG202", "S21", 2, "row3"),
        CourseOfferingSection("ENG202", "S22", None, "row4"),
    ]

    grouped = group_sections_for_subjects(
        subject_codes=["COMP201", "ENG202"],
        offerings=offerings,
        group_size=2,
    )

    assert len(grouped) == 2
    assert [item.section_code for item in grouped[0].sections] == ["S11"]
    assert [item.section_code for item in grouped[1].sections] == ["S21", "S22"]


def test_choose_offerings_term_and_year_prefers_regular_profile_status() -> None:
    enrollment_status = EnrollmentStatus(
        term_number=3,
        school_year="20252026",
        year_level=3,
        student_type="REGULAR",
        is_regular=True,
        heading_text="Enrollment Status: Term 3 SY 20252026",
    )

    term, school_year, used_profile = choose_offerings_term_and_year(
        enrollment_status=enrollment_status,
        term_labels=["1 - 20242025", "2 - 20242025"],
        fallback_course_grades=[],
    )

    assert term == 3
    assert school_year == "20242025"
    assert used_profile is True


def test_choose_offerings_term_and_year_falls_back_for_irregular() -> None:
    enrollment_status = EnrollmentStatus(
        term_number=1,
        school_year="20232024",
        year_level=3,
        student_type="IRREGULAR",
        is_regular=False,
        heading_text="Enrollment Status: Term 1 SY 20232024",
    )

    term, school_year, used_profile = choose_offerings_term_and_year(
        enrollment_status=enrollment_status,
        term_labels=["2 - 20242025", "3 - 20242025"],
        fallback_course_grades=[],
    )

    assert term == 3
    assert school_year == "20242025"
    assert used_profile is False
