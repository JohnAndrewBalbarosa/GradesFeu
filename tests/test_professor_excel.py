from pathlib import Path

from openpyxl import Workbook

from grades_checker.models.entities import CourseOfferingSection
from grades_checker.models.entities import SubjectSections
from grades_checker.services.professor_excel import apply_professor_map
from grades_checker.services.professor_excel import load_professor_map_from_excel


def test_load_professor_map_and_apply(tmp_path: Path) -> None:
    xlsx_path = tmp_path / "profs.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["Course Code", "Section", "Professor"])
    ws.append(["CCS0003", "TC191", "Prof A"])
    ws.append(["CCS0003", "TW192", "Prof B"])
    ws.append(["CS0061", "", "Prof C"])
    wb.save(xlsx_path)

    prof_map = load_professor_map_from_excel(str(xlsx_path))

    grouped = [
        SubjectSections(
            subject_code="CCS0003",
            sections=[
                CourseOfferingSection("CCS0003", "TC191", 5, ""),
                CourseOfferingSection("CCS0003", "TW192", 4, ""),
            ],
        ),
        SubjectSections(
            subject_code="CS0061",
            sections=[
                CourseOfferingSection("CS0061", "TN31", 6, ""),
            ],
        ),
    ]

    updated = apply_professor_map(grouped, prof_map)

    assert updated[0].sections[0].professor_name == "Prof A"
    assert updated[0].sections[1].professor_name == "Prof B"
    assert updated[1].sections[0].professor_name == "Prof C"
