import math
from typing import Any

from src.core.auxiliary import get_sorted_section_or_aggregation_values


def calculate_grades(data: dict[str, Any], type_: str, is_aggregation: bool) -> dict[int, tuple[int, int]]:
    key = "sections" if not is_aggregation else "aggregations"
    sorted_section_values = get_sorted_section_or_aggregation_values(data, type_, key)
    return calculate_section_grades(sorted_section_values)


def calculate_section_grades(sorted_section: list[tuple[str, int]]) -> dict[int, tuple[int, int]]:
    values = [section_value for date, section_value in sorted_section]
    if values != sorted(values):
        raise ValueError("Section values are not sorted.")

    if not values:
        return {}

    first: int = values[0]
    last: int = values[-1]
    range_ = last - first
    step: int = int(math.floor(range_ / 5.0))
    return {
        1: (first, first + step),
        2: (first + step, first + (2 * step)),
        3: (first + (2 * step), first + (3 * step)),
        4: (first + (3 * step), first + (4 * step)),
        5: (first + (4 * step), last + 1),
    }

def calculate_value_grade(value: int, grades: dict[int, tuple[int, int]]) -> int | None:
    def is_suitable(grade: int) -> bool:
        min_, max_ = grades[grade]
        return min_ <= value < max_

    grade_numbers = [1,2,3,4,5]
    for grade_num in grade_numbers:
        if is_suitable(grade_num):
            return grade_num
    return None

# def get_key_by_type(type_: SectionType | AggregationType) -> str:
#     if isinstance(type_, AggregationType):
#         return "aggregation_grades"
#     elif isinstance(type_, SectionType):
#         return "section_grades"
#     else:
#         raise ValueError(f"Unsupported type {type_}")


def update_section_or_aggregation_grades(data: dict[str, Any], type_: str, is_aggregation: bool, grades: dict[int, tuple[int, int]]) -> dict[str, Any]:
    key = "section_grades" if not is_aggregation else "aggregation_grades"
    data[key][type_] = grades
    return data
