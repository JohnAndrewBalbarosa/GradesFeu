from pathlib import Path

from grades_checker.config.settings import load_settings
from grades_checker.logic.performance import analyze_failed_subject_recovery
from grades_checker.logic.performance import analyze_outliers_all_data
from grades_checker.logic.performance import get_failed_subjects
from grades_checker.logic.performance import round_to_half_step
from grades_checker.models.entities import CourseGrade


def test_load_settings_from_env_file(tmp_path: Path) -> None:
    env_file = tmp_path / ".env.test"
    env_file.write_text(
        "\n".join(
            [
                "GRADES_URL=https://example.com/grades",
                "CURRICULUM_URL=https://example.com/curriculum",
                "HONOR_SUMMA_MIN=3.85",
                "HONOR_MAGNA_MIN=3.65",
                "HONOR_CUM_MIN=3.45",
                "OUTLIER_Z_THRESHOLD=2.2",
                "OUTLIER_TAIL=left",
                "FAILED_GRADE_VALUES=0.0,0.5",
                "CACHE_FILE=.cache/custom.json",
            ]
        ),
        encoding="utf-8",
    )

    settings = load_settings(str(env_file))
    assert settings.grades_url == "https://example.com/grades"
    assert settings.curriculum_url == "https://example.com/curriculum"
    assert settings.honor_summa_min == 3.85
    assert settings.honor_magna_min == 3.65
    assert settings.honor_cum_min == 3.45
    assert settings.outlier_z_threshold == 2.2
    assert settings.outlier_tail == "left"
    assert settings.failed_grade_values == (0.0, 0.5)
    assert settings.cache_file == ".cache/custom.json"


def test_outlier_analysis_detects_low_subject_and_projects() -> None:
    rows = [
        CourseGrade("1 - 20232024", "A", "Sub A", 3, 3.6),
        CourseGrade("1 - 20232024", "B", "Sub B", 3, 3.5),
        CourseGrade("1 - 20232024", "C", "Sub C", 3, 2.0),
        CourseGrade("2 - 20232024", "D", "Sub D", 3, 3.7),
        CourseGrade("2 - 20232024", "E", "Sub E", 3, 2.0),
        CourseGrade("3 - 20232024", "F", "Sub F", 3, 3.5),
        CourseGrade("3 - 20232024", "G", "Sub G", 3, 3.6),
    ]

    result = analyze_outliers_all_data(
        course_grades=rows,
        completed_units=21,
        total_curriculum_units=210,
        honor_targets=(
            ("Summa Cum Laude", 3.8),
            ("Magna Cum Laude", 3.6),
            ("Cum Laude", 3.4),
        ),
        outlier_method="mad",
        outlier_tail="left",
        z_threshold=2.0,
        baseline_estimator="trimmed_mean",
    )

    assert len(result.low_outliers) == 2
    assert {item.course_code for item in result.low_outliers} == {"C", "E"}
    assert result.projected_cgpa_without_low_outliers > 3.4


def test_round_to_half_step() -> None:
    assert round_to_half_step(3.26) == 3.5
    assert round_to_half_step(3.24) == 3.0
    assert round_to_half_step(3.75) == 4.0


def test_failed_subject_detection_and_recovery() -> None:
    rows = [
        CourseGrade("1 - 20232024", "A", "Sub A", 3, 3.5),
        CourseGrade("1 - 20232024", "B", "Sub B", 3, 0.5),
        CourseGrade("1 - 20232024", "X", "Sub X", 3, 9.0),
        CourseGrade("2 - 20232024", "C", "Sub C", 3, 3.5),
        CourseGrade("2 - 20232024", "D", "Sub D", 3, 3.0),
    ]

    failed = get_failed_subjects(rows, (0.0, 0.5))
    assert len(failed) == 1
    assert failed[0].course_code == "B"

    recovery = analyze_failed_subject_recovery(
        course_grades=rows,
        completed_units=12,
        total_curriculum_units=210,
        honor_targets=(
            ("Summa Cum Laude", 3.8),
            ("Magna Cum Laude", 3.6),
            ("Cum Laude", 3.4),
        ),
        failed_grade_values=(0.0, 0.5),
        baseline_estimator="trimmed_mean",
    )

    assert len(recovery.failed_subjects) == 1
    assert recovery.replacement_grade in (3.0, 3.5, 4.0)
    assert recovery.projected_cgpa_without_failed_subjects > 0
