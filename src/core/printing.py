import re
from dataclasses import dataclass
from datetime import datetime

from colorama import Fore, Style, Back

from src.model.printing import TrainingsModel, RouteModel, TrainingModel, SectionModel, SectionsModel, GradeModel, \
    DashboardModel, CellIdentModel, CompareModel
from src.utils.time import to_time

DT_09_2025: datetime = datetime(2025, 9, 1)
DT_01_2025: datetime = datetime(2025, 1, 1)
DT_01_2026: datetime = datetime(2026, 1, 1)

def _more_than_09_2025(date: str) -> bool:
    dt = datetime.strptime(date, "%Y-%m-%d")
    return dt >= DT_09_2025


def _more_than_01_2025(date: str) -> bool:
    dt = datetime.strptime(date, "%Y-%m-%d")
    return dt >= DT_01_2025


def _more_than_01_2026(date: str) -> bool:
    dt = datetime.strptime(date, "%Y-%m-%d")
    return dt >= DT_01_2026

def get_line_color(line: str, mark: str | None = None) -> Fore:
    match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", line)
    if match:
        date = match.group(0)
        if mark and mark == date:
            return Fore.RED
        if _more_than_01_2026(date):
            return Fore.BLUE
        if _more_than_09_2025(date):
            return Fore.GREEN
        if _more_than_01_2025(date):
            return Fore.YELLOW
    return Fore.WHITE


def print_color_line(line: str, color: Fore) -> None:
    print(color + f"{line}")
    print(Style.RESET_ALL, end="")


def print_routes(routes: list[RouteModel]) -> None:
    for route in routes:
        print(f"{route.name} - {route.description}")


def print_dates(dates: TrainingsModel) -> None:
    for date in dates.dates:
        color = get_line_color(date)
        print_color_line(date, color)


def print_training(training: TrainingModel) -> None:
    sekce: str = ""
    for sec in training.sections:
        sekce += f"{sec.name}: {to_time(sec.value)} ({sec.order} / {sec.grade}), +{sec.lost}\n"
    output: str = f"{training.date}, \nsections:\n{sekce}"
    aggregace: str = ""
    for sec in training.aggregations:
        if sec.time_convertible:
            aggregace += f"{sec.name}: {to_time(sec.value)} ({sec.order} / {sec.grade}), +{sec.lost}\n"
        else:
            aggregace += f"{sec.name}: {sec.value} ({sec.order} / {sec.grade}), +{sec.lost}\n"
    output += f"\naggregations:\n{aggregace}\n"
    # if training["intervals"]:
    #     output += "intervals: \n"
    #     for interval in self.interval_sections:
    #         output += f"{interval.duration}, {interval.index} ({interval.order}), +{interval.lost}\n"
    if training.note:
        output += f"note:\n{training.note}\n"
    print(f"{output}")


def only_seconds(value: int) -> int:
    return value % 60


def print_sections(section: SectionsModel) -> None:
    empty_line: str = "*" * 50
    prev_seconds: int | None = None
    section_name = ""
    if len(section.date_sections.keys()) > 0:
        section_name = section.date_sections[list(section.date_sections.keys())[0]].name
    for date, date_values in section.date_sections.items():
        if prev_seconds is not None:
            if prev_seconds >= 29 > only_seconds(date_values.value):
                print(empty_line)
            elif prev_seconds <= 29 < only_seconds(date_values.value):
                print(empty_line)

        lost: str = f"+{date_values.lost}"
        if date_values.time_convertible:
            line = f"{section_name}, {date}, {to_time(date_values.value)} ({date_values.order} / {date_values.grade}), {lost}"
        else:
            line = f"{section_name}, {date}, {date_values.value} ({date_values.order} / {date_values.grade}), {lost}"
        color = get_line_color(line, section.mark_date)
        print_color_line(line, color)
        prev_seconds = only_seconds(date_values.value)

def print_grades(grades: list[GradeModel]) -> None:
    for grade in grades:
        if grade.time_convertible:
            print(f"{grade.grade}: <{to_time(grade.from_)} - {to_time(grade.to_)})")
        else:
            print(f"{grade.grade}: <{grade.from_} - {grade.to_})")


@dataclass
class CellStyle:
    foreground_color: Fore
    background_color: Back

DASHBOARD_PRINT_STYLE: dict[int, CellStyle] = {
    1: CellStyle(background_color=Back.GREEN, foreground_color=Fore.BLACK),
    2: CellStyle(background_color=Back.LIGHTYELLOW_EX, foreground_color=Fore.BLACK),
    3: CellStyle(background_color=Back.BLUE, foreground_color=Fore.WHITE),
    4: CellStyle(background_color=Back.MAGENTA, foreground_color=Fore.WHITE),
    5: CellStyle(background_color=Back.RED, foreground_color=Fore.WHITE),
}


def _print_cell_with_length(msg: str, length: int) -> None:
    add_space = length - len(msg)
    if add_space <= 0:
        print(msg, end="")
    elif add_space == 1:
        print(" " + msg, end="")
    else:
        print(" " + msg + (add_space - 1) * " ", end="")


def _get_month(date: str) -> str:
    parts = date.split("-")
    return f"{parts[0]}-{parts[1]}"


def _print_cell_with_style_and_length(msg: str, length: int, style: CellStyle) -> None:
    add_space = length - len(msg)
    if add_space <= 0:
        message = msg
    elif add_space == 1:
        message = " " + msg
    else:
        message = " " + msg + (add_space - 1) * " "

    print(style.background_color + style.foreground_color + message + Style.RESET_ALL, end="")


def print_dashboard(dashboard_data: DashboardModel, split_months: bool = False) -> None:
    trainings: list[str] = dashboard_data.get_dates()
    length: int = 14
    _print_cell_with_length("Dates", 15)
    sections_and_aggs: list[str] = dashboard_data.sections + dashboard_data.aggregations
    for col in sections_and_aggs:
        _print_cell_with_length(f"{col}", length)
    print("")
    month = _get_month(trainings[0])
    for date in trainings:
        current_month = _get_month(date)
        if month != current_month and split_months:
            month = current_month
            print("")

        _print_cell_with_length(date, 15)
        for col in sections_and_aggs:
            if not dashboard_data.exists_key(date=date, section=col):
                _print_cell_with_length("", length)
            else:
                val = dashboard_data.get_data(date=date, section=col)
                assert val is not None
                if val.time_convertible:
                    _print_cell_with_style_and_length(f"{to_time(val.value)} ({val.order})", length,
                                                      DASHBOARD_PRINT_STYLE[val.grade])
                else:
                    _print_cell_with_style_and_length(f"{val.value} ({val.order})", length,
                                                      DASHBOARD_PRINT_STYLE[val.grade])
        print("")


def _compare_format(section_data: SectionModel) -> str:
    s_lost: str = str(section_data.lost)
    s_lost = s_lost if len(s_lost) > 1 else s_lost + " "
    lost: str = f"+{s_lost}"
    s_order: str = str(section_data.order) if section_data.order > 9 else " " + str(section_data.order)
    if section_data.time_convertible:
        return f"{to_time(section_data.value)} ({s_order}) {lost}"
    else:
        return f"{section_data.value} ({s_order}) {lost}"


def print_compare(compare_data: CompareModel) -> None:
    print("\t", end="")
    print(f"\t{compare_data.data_1.date}", end="")
    print(f"\t{compare_data.data_2.date}", end="")
    print("\tdiff")
    diff: int = 0
    str_diff: str = ""
    for section_type in compare_data.data_1.sections:
        print(f"{section_type.name}\t\t", end="")
        s1, s2 = compare_data.get_sections(section_type.name)
        assert s1 is not None
        assert s2 is not None
        print(f"{_compare_format(s1)}\t", end="")
        print(f"{_compare_format(s2)}\t", end="")
        diff = s2.value - s1.value
        str_diff = str(diff) if diff < 0 else f"+{diff}"
        print(f"{str_diff}", end="")
        print("")
    for agg_type in compare_data.data_1.aggregations:
        if len(agg_type.name) >= 10:
            print(f"{agg_type.name}\t", end="")
        else:
            print(f"{agg_type.name}\t\t", end="")

        a1, a2 = compare_data.get_aggregations(agg_type.name)
        a1_ok: bool = False
        if a1:
            print(f"{_compare_format(a1)}\t", end="")
            a1_ok = True
        else:
            print("\t\t", end="")

        a2_ok: bool = False
        if a2:
            print(f"{_compare_format(a2)}\t", end="")
            a2_ok = True
        else:
            print("\t\t", end="")
        if a1_ok and a2_ok:
            assert a1 is not None
            assert a2 is not None
            diff = a2.value - a1.value
            str_diff = str(diff) if diff < 0 else f"+{diff}"
            print(f"{str_diff}", end="")
        print("")