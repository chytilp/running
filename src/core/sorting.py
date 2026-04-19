from typing import Any

from src.core.auxiliary import get_sorted_section_or_aggregation_values
from src.core.grades import calculate_section_grades, calculate_value_grade


def sort_section_or_aggregation(data: dict[str, Any], type_: str, is_aggregagtion: bool, grades: dict[int, tuple[int, int]]
                                ) -> dict[str, tuple[int, int, int]]:
    # return attributes - tuple [order, lost, grade]
    key = "sections" if not is_aggregagtion else "aggregations"
    sorted_section_values = get_sorted_section_or_aggregation_values(data, type_, key)
    output: dict[str, tuple[int, int, int]] = {}
    if len(sorted_section_values) == 0:
        return output

    first = sorted_section_values[0][1]
    order: int = 1
    how_many: int = 1
    index: int = -1
    for date, value in sorted_section_values:
        index += 1
        if index == 0:
            pass
        elif sorted_section_values[index - 1][1] == value:
            how_many += 1
        else:
            order = order + how_many
            how_many = 1

        lost = value - first
        grade = calculate_value_grade(value, grades)

        output[date] = (order, lost, grade)

    return output


def update_section_or_aggregation_data(data: dict[str, Any], type_: str, is_aggregation: bool,
                                       sort_result: dict[str, tuple[int, int, int]]) -> dict[str, Any]:
    key = "sections" if not is_aggregation else "aggregations"
    root = data["trainings"]
    for date, value in sort_result.items():
        order, lost, grade = value
        sub_root = root[date][key][type_]
        sub_root["order"] = order
        sub_root["lost"] = lost
        sub_root["grade"] = grade
    return data