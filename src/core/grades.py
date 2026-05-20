import math
from typing import Any

from src.core.auxiliary import get_sorted_section_or_aggregation_values
from src.model.grade import Grades, Grade


# def calculate_grades(data: dict[str, Any], type_: str, is_aggregation: bool) -> dict[int, tuple[int, int]]:
#     # type_ is section / aggregation name
#     key = "sections" if not is_aggregation else "aggregations"
#     sorted_section_values = get_sorted_section_or_aggregation_values(data, type_, key)
#     return calculate_section_grades(sorted_section_values)

def calculate_grades(sorted_data: list[tuple[str, int]], reverse: bool = False) -> Grades:
    return calculate_section_grades(sorted_data, reverse)


def calculate_section_grades(sorted_section: list[tuple[str, int]], reverse: bool = False) -> Grades:
    values = [section_value for date, section_value in sorted_section]
    if len(values) > 0 and values[0] != max(values) and values[0] != min(values):
        raise ValueError("Section values are not sorted.")

    if not values:
        return Grades()

    first: int = values[0]
    last: int = values[-1]
    range_ = last - first
    step: int = int(math.floor(range_ / 5.0))
    grades = Grades()
    grades.add(Grade(grade=1,from_=first, to_=first + step))
    grades.add(Grade(grade=2, from_=first + step, to_=first + (2 * step)))
    grades.add(Grade(grade=3, from_=first + (2 * step), to_=first + (3 * step)))
    grades.add(Grade(grade=4, from_=first + (3 * step), to_=first + (4 * step)))
    grades.add(Grade(grade=5, from_=first + (4 * step), to_=0 if reverse else 1_000_000))
    return grades

def calculate_value_grade(value: int, grades: Grades, reverse: bool = False) -> int | None:
    def is_suitable(grade: int) -> bool:
        if grades.empty:
            raise ValueError("Grades cannot be empty.")

        g: Grade = grades.get_grade(grade)
        if g is None:
            return False

        return g.from_ <= value < g.to_

    grade_numbers = [1,2,3,4,5]
    for grade_num in grade_numbers:
        if is_suitable(grade_num):
            return grade_num
    return None

def update_section_or_aggregation_grades(data: dict[str, Any], type_: str, key: str, grades: dict[int, tuple[int, int]]) -> dict[str, Any]:
    # key = "section_grades" if not is_aggregation else "aggregation_grades"
    data[key][type_] = grades
    return data
