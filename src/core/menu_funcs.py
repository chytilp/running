from typing import Any

from src.core.data_module import get, filter_sections, filter_aggregations
from src.core.printing import print_dates, print_training, print_sections, print_dashboard, print_compare


def get_dates(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    dates: list[str] = [date for date in data["trainings"].keys()]
    print_dates(dates)


def get_date(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    if not arguments.date:
        raise ValueError("Date argument must be specified.")

    date_data = get(data, ["trainings", arguments.date])
    if date_data:
        print_training(arguments.date, date_data)
    else:
        raise ValueError(f"No training data found for {arguments.date}")


def get_section(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    if not arguments.section:
        raise ValueError("Section argument must be specified.")

    section: str = arguments.section.lower()
    data = get(data, ["trainings", "*", "sections", section])
    data = dict(sorted(data.items(), key=lambda item: item[1]["order"]))
    mark = None
    if arguments.mark:
        mark = arguments.mark.strip()
    print_sections(section, data, mark)


def get_aggregation(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    if not arguments.aggregation:
        raise ValueError("Aggregation argument must be specified.")

    aggregation: str = arguments.aggregation.lower()
    data = get(data, ["trainings", "*", "aggregations", aggregation])
    data = dict(sorted(data.items(), key=lambda item: item[1]["order"]))
    mark = None
    if arguments.mark:
        mark = arguments.mark.strip()
    print_sections(aggregation, data, mark)


def get_grades(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    if not arguments.section and not arguments.aggregation:
        raise ValueError("At least one of section or aggregation must be specified.")

    if arguments.section:
        section: str = arguments.section.lower()
        grades = get(data, ["section_grades", section])
        print(f"grades {section}: {grades}")
    elif arguments.aggregation:
        aggregation: str = arguments.aggregation.lower()
        grades = get(data, ["aggregation_grades", aggregation])
        print(f"grades {aggregation}: {grades}")


def _merge(data_1: dict[tuple[str, str], dict[str, Any]], data_2: dict[tuple[str, str], dict[str, Any]]
           ) -> dict[tuple[str, str], dict[str, Any]]:
    output: dict[tuple[str, str], dict[str, Any]] = data_1
    for (key_1, key_2), value in data_2.items():
        output[(key_1, key_2)] = value
    return output

def get_dashboard(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    sections = kwargs.get("sections", []) + kwargs.get("aggregations", [])
    sections_data: dict[tuple[str, str], dict[str, Any]] = get(data, ["trainings", "*", "sections", "*"])
    aggregations_data = get(data, ["trainings", "*", "aggregations", "*"])
    data_for_print: dict[tuple[str, str], dict[str, Any]] = _merge(sections_data, aggregations_data)
    print_dashboard(data_for_print, sections, True)


def _prepare_training(data_: dict[str, Any], date: str, sections: list[str], aggregations: list[str]) -> dict[str, Any]:
    data_1 = get(data_, ["trainings", date])
    data_1 = filter_sections(data_1, sections)
    return filter_aggregations(data_1, aggregations)


def get_compare(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    if not arguments.compare:
        raise ValueError("No 2 dates for comparison found.")

    sections: list[str] = kwargs.get("sections", [])
    aggregations: list[str] = kwargs.get("aggregations", [])
    dates = arguments.compare
    dates_list = dates.split(",")
    date_1 = dates_list[0]
    date_2 = dates_list[1]
    data_1 = _prepare_training(data, date_1, sections, aggregations)
    data_1["date"] = date_1
    data_2 = _prepare_training(data, date_2, sections, aggregations)
    data_2["date"] = date_2
    print_compare(data_1, data_2)


def get_top(data: dict[str, Any], arguments: Any, **kwargs) -> None:
    if not arguments.top:
        raise ValueError("Top argument must be specified.")