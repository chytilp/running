from dataclasses import dataclass
from typing import Any

from src.core.data_module import get, filter_sections, filter_aggregations
from src.core.printing import print_routes, print_dates, print_sections, print_training, print_grades, print_dashboard, print_compare
from src.core.lib_funcs import (get_routes as lib_routes, get_dates as lib_dates, get_date as lib_date,
                                get_section as lib_section, get_aggregation as lib_aggregation,
                                get_section_grades as lib_section_grades,
                                get_aggregation_grades as lib_aggregation_grades,
                                get_dashboard as lib_dashboard, get_compare as lib_compare,)

from src.model.printing import RouteModel, TrainingsModel, TrainingModel, SectionsModel, GradeModel, DashboardModel, \
    CompareModel

@dataclass
class Range:
    from_: str
    to_: str


def _get_from_to(arguments: Any) -> Range:
    start: str = ""
    if arguments.start:
        start = arguments.start.strip()
    end: str = ""
    if arguments.end:
        end = arguments.end.strip()
    return Range(from_=start, to_=end)

def get_routes(arguments: Any, **kwargs) -> None:
    routes: list[RouteModel] = lib_routes()
    print_routes(routes)


def get_dates(arguments: Any, **kwargs) -> None:
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)
    dates: TrainingsModel = lib_dates(route)
    print_dates(dates)


def get_date(arguments: Any, **kwargs) -> None:
    if not arguments.date:
        raise ValueError("Date argument must be specified.")
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)
    training: TrainingModel = lib_date(route, arguments.date)
    print_training(training)


def get_section(arguments: Any, **kwargs) -> None:
    if not arguments.section:
        raise ValueError("Section argument must be specified.")
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)
    section: str = arguments.section.lower()
    mark = ""
    if arguments.mark:
        mark = arguments.mark.strip()
    range_: Range = _get_from_to(arguments)
    section_data: SectionsModel = lib_section(route, section, from_=range_.from_, to_=range_.to_, mark_date=mark)
    print_sections(section_data)


def get_aggregation(arguments: Any, **kwargs) -> None:
    if not arguments.aggregation:
        raise ValueError("Aggregation argument must be specified.")
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)
    aggregation: str = arguments.aggregation.lower()
    mark = ""
    if arguments.mark:
        mark = arguments.mark.strip()
    range_: Range = _get_from_to(arguments)
    agg_data: SectionsModel = lib_aggregation(route, aggregation, from_=range_.from_, to_=range_.to_, mark_date=mark)
    print_sections(agg_data)


def get_grades(arguments: Any, **kwargs) -> None:
    if not arguments.section and not arguments.aggregation:
        raise ValueError("At least one of section or aggregation must be specified.")
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)
    range_: Range = _get_from_to(arguments)
    grades: list[GradeModel] = []
    if arguments.section:
        section: str = arguments.section.lower()
        grades = lib_section_grades(route, section, from_=range_.from_, to_=range_.to_)
        print_grades(grades)
    elif arguments.aggregation:
        aggregation: str = arguments.aggregation.lower()
        grades = lib_aggregation_grades(route, aggregation, from_=range_.from_, to_=range_.to_)
        print_grades(grades)


def get_dashboard(arguments: Any, **kwargs) -> None:
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)
    range_: Range = _get_from_to(arguments)
    result: DashboardModel = lib_dashboard(route, from_=range_.from_, to_=range_.to_)
    print_dashboard(result, True)


def _prepare_training(data_: dict[str, Any], date: str, sections: list[str], aggregations: list[str]) -> dict[str, Any]:
    data_1 = get(data_, ["trainings", date])
    data_1 = filter_sections(data_1, sections)
    return filter_aggregations(data_1, aggregations)


def get_compare(arguments: Any, **kwargs) -> None:
    if not arguments.compare:
        raise ValueError("No 2 dates for comparison found.")
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)
    dates = arguments.compare
    dates_list = dates.split(",")
    date_1 = dates_list[0]
    date_2 = dates_list[1]
    result: CompareModel = lib_compare(route, date_1=date_1, date_2=date_2)
    print_compare(result)


def get_top(arguments: Any, **kwargs) -> None:
    if not arguments.top:
        raise ValueError("Top argument must be specified.")
    if not arguments.route:
        raise ValueError("Route argument must be specified.")
    route = RouteModel(name=arguments.route)