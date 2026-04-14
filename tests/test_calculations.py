from grades_checker.logic.cgpa import required_average_for_target
from grades_checker.logic.terms import sort_term_labels


def test_required_average_cum_laude_for_3_333() -> None:
    needed = required_average_for_target(
        current_cgpa=3.333,
        completed_units=135,
        total_curriculum_units=210,
        target_cgpa=3.4,
    )
    assert round(needed, 4) == 3.5206


def test_required_average_magna_for_3_333() -> None:
    needed = required_average_for_target(
        current_cgpa=3.333,
        completed_units=135,
        total_curriculum_units=210,
        target_cgpa=3.6,
    )
    assert round(needed, 4) == 4.0806


def test_required_average_summa_for_3_333() -> None:
    needed = required_average_for_target(
        current_cgpa=3.333,
        completed_units=135,
        total_curriculum_units=210,
        target_cgpa=3.8,
    )
    assert round(needed, 4) == 4.6406


def test_term_labels_are_sorted_first_to_latest() -> None:
    labels = [
        "2 - 20252026",
        "1 - 20232024",
        "3 - 20242025",
        "1 - 20252026",
    ]
    sorted_labels = sort_term_labels(labels)
    assert sorted_labels == [
        "1 - 20232024",
        "3 - 20242025",
        "1 - 20252026",
        "2 - 20252026",
    ]
