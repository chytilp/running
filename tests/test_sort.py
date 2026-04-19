from src.core.functions import sort_sections, sort_aggregations
from src.core.grades import calculate_grades
from src.core.sorting import sort_section_or_aggregation

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

def test_only_sort_section_result() -> None:
    # order, lost, grade
    grades = calculate_grades(data, "1.km", False)
    output: dict[str, tuple[int, int, int]] = sort_section_or_aggregation(data, "1.km",
                                                                          False, grades)
    assert output["2026-02-01"] == (1, 0, 1)
    assert output["2026-02-04"] == (2, 12, 2)
    assert output["2026-02-03"] == (3, 20, 3)
    assert output["2026-02-02"] == (4, 35, 4)
    assert output["2026-02-05"] == (5, 45, 5)

def test_only_sort_section_result_same_values() -> None:
    grades = calculate_grades(data_2, "1.km", False)
    output: dict[str, tuple[int, int, int]] = sort_section_or_aggregation(data_2, "1.km",
                                                                          False, grades)
    assert output["2026-02-01"] == (1, 0, 1)
    assert output["2026-02-03"] == (1, 0, 1)
    assert output["2026-02-02"] == (3, 15, 4)
    assert output["2026-02-04"] == (3, 15, 4)
    assert output["2026-02-05"] == (5, 25, 5)


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
