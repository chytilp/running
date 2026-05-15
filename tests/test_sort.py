from src.core.functions import sort_sections, sort_aggregations
from src.core.grades import calculate_grades
from src.core.sorting import sort_section_or_aggregation
from src.model.sorting import SortResult

data: dict = {
    "section_grades": {},
    "aggregation_grades": {},
    "trainings": {
        "2026-02-01": {
            "sections": {
                "1.km": {"value": 295}
            },
            "aggregations": {
                "1.round": {"value": 1440}
            }
        },
        "2026-02-02": {
            "sections": {
                "1.km": {"value": 330}
            },
            "aggregations": {
                "1.round": {"value": 1400}
            }
        },
        "2026-02-03": {
            "sections": {
                "1.km": {"value": 315}
            },
            "aggregations": {
                "1.round": {"value": 1390}
            }
        },
        "2026-02-04": {
            "sections": {
                "1.km": {"value": 307}
            },
            "aggregations": {
                "1.round": {"value": 1445}
            }
        },
        "2026-02-05": {
            "sections": {
                "1.km": {"value": 340}
            },
            "aggregations": {
                "1.round": {"value": 1435}
            }
        },
    }
}

data_2: dict = {
    "section_grades": {},
    "aggregation_grades": {},
    "trainings": {
        "2026-02-01": {
            "sections": {
                "1.km": {"value": 295}
            }
        },
        "2026-02-02": {
            "sections": {
                "1.km": {"value": 310}
            }
        },
        "2026-02-03": {
            "sections": {
                "1.km": {"value": 295}
            }
        },
        "2026-02-04": {
            "sections": {
                "1.km": {"value": 310}
            }
        },
        "2026-02-05": {
            "sections": {
                "1.km": {"value": 320}
            }
        },
    }
}


def assert_sort_result(result: SortResult, expected_order: int, expected_lost: int, expected_grade: int) -> None:
    assert result.order == expected_order
    assert result.lost == expected_lost
    assert result.grade == expected_grade


def test_only_sort_section_result() -> None:
    # order, lost, grade
    grades = calculate_grades(data, "1.km", False)
    output: dict[str, SortResult] = sort_section_or_aggregation(data, "1.km",
                                                                          False, grades)
    assert_sort_result(output["2026-02-01"], expected_order=1, expected_lost=0, expected_grade=1)
    assert_sort_result(output["2026-02-04"], expected_order=2, expected_lost=12, expected_grade=2)
    assert_sort_result(output["2026-02-03"], expected_order=3, expected_lost=20, expected_grade=3)
    assert_sort_result(output["2026-02-02"], expected_order=4, expected_lost=35, expected_grade=4)
    assert_sort_result(output["2026-02-05"], expected_order=5, expected_lost=45, expected_grade=5)

def test_only_sort_section_result_same_values() -> None:
    grades = calculate_grades(data_2, "1.km", False)
    output: dict[str, SortResult] = sort_section_or_aggregation(data_2, "1.km",
                                                                          False, grades)
    assert_sort_result(output["2026-02-01"], expected_order=1, expected_lost=0, expected_grade=1)
    assert_sort_result(output["2026-02-03"], expected_order=1, expected_lost=0, expected_grade=1)
    assert_sort_result(output["2026-02-02"], expected_order=3, expected_lost=15, expected_grade=4)
    assert_sort_result(output["2026-02-04"], expected_order=3, expected_lost=15, expected_grade=4)
    assert_sort_result(output["2026-02-05"], expected_order=5, expected_lost=25, expected_grade=5)


def test_sort_sections() -> None:
    result = sort_sections(data, ["1.km",])
    root = result["trainings"]
    assert root["2026-02-01"]["sections"]["1.km"] == {"value": 295, "order": 1, "lost": 0, "grade": 1}
    assert root["2026-02-04"]["sections"]["1.km"] == {"value": 307, "order": 2, "lost": 12, "grade": 2}
    assert root["2026-02-03"]["sections"]["1.km"] == {"value": 315, "order": 3, "lost": 20, "grade": 3}
    assert root["2026-02-02"]["sections"]["1.km"] == {"value": 330, "order": 4, "lost": 35, "grade": 4}
    assert root["2026-02-05"]["sections"]["1.km"] == {"value": 340, "order": 5, "lost": 45, "grade": 5}
    assert "1.km" in list(result["section_grades"].keys())
    assert result["section_grades"]["1.km"] == {1: (295, 304), 2: (304, 313), 3: (313, 322), 4: (322, 331), 5: (331, 341)}
    assert id(data) != id(result)


def test_sort_aggregations() -> None:
    result = sort_aggregations(data, ["1.round",])
    root = result["trainings"]
    assert root["2026-02-01"]["aggregations"]["1.round"] == {"value": 1440, "order": 4, "lost": 50, "grade": 5}
    assert root["2026-02-04"]["aggregations"]["1.round"] == {"value": 1445, "order": 5, "lost": 55, "grade": 5}
    assert root["2026-02-03"]["aggregations"]["1.round"] == {"value": 1390, "order": 1, "lost": 0, "grade": 1}
    assert root["2026-02-02"]["aggregations"]["1.round"] == {"value": 1400, "order": 2, "lost": 10, "grade": 1}
    assert root["2026-02-05"]["aggregations"]["1.round"] == {"value": 1435, "order": 3, "lost": 45, "grade": 5}
    assert "1.round" in list(result["aggregation_grades"].keys())
    assert result["aggregation_grades"]["1.round"] == {1: (1390, 1401), 2: (1401, 1412), 3: (1412, 1423), 4: (1423, 1434),
                                                       5: (1434, 1446)}
    assert id(data) != id(result)
