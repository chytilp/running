import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from colorama import Style, Fore, Back

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


def print_color_line(line: str, color: Fore) -> None:
    print(color + f"{line}")
    print(Style.RESET_ALL, end="")


def print_dates(dates: list[str]) -> None:
    for date in dates:
        color = get_line_color(date)
        print_color_line(date, color)


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


def print_training(date: str, training: dict[str, Any]) -> None:
    sekce: str = ""
    for k, sec in training["sections"].items():
        sekce += f"{k}: {to_time(sec['value'])} ({sec['order']} / {sec['grade']}), +{sec['lost']}\n"
    output: str = f"{date}, \nsections:\n{sekce}"
    aggregace: str = ""
    for k, sec in training["aggregations"].items():
        aggregace += f"{k}: {to_time(sec['value'])} ({sec['order']} / {sec['grade']}), +{sec['lost']}\n"
    output += f"\naggregations:\n{aggregace}\n"
    # if training["intervals"]:
    #     output += "intervals: \n"
    #     for interval in self.interval_sections:
    #         output += f"{interval.duration}, {interval.index} ({interval.order}), +{interval.lost}\n"
    if training["note"]:
        output += f"note:\n{training['note']}\n"
    print(f"{output}")


def only_seconds(value: int) -> int:
    return value % 60


def print_sections(type_: str, data: dict[str, Any], mark: str | None = None) -> None:
    empty_line: str = "*" * 50
    prev_seconds: int | None = None
    for date, date_values in data.items():
        if prev_seconds is not None:
            if prev_seconds >= 29 > only_seconds(date_values['value']):
                print(empty_line)
            elif prev_seconds <= 29 < only_seconds(date_values['value']):
                print(empty_line)

        lost: str = f"+{date_values['lost']}"
        line = f"{type_}, {date}, {to_time(date_values['value'])} ({date_values['order']} / {date_values['grade']}), {lost}"
        color = get_line_color(line, mark)
        print_color_line(line, color)
        prev_seconds = only_seconds(date_values['value'])

def _format_date_short(date: str) -> str:
    parts = date.split("-")
    return parts[2]

def _format_column(column: str) -> str:
    after = 8 - len(column)
    return " " + column + (after * " ")

# def print_month(month: str, data: dict[SectionType | AggregationType, list[tuple[str, int]]]) -> None:
#     print(f"month: {month}")
#     columns = [section for section in data.keys()]
#     for column in columns:
#         print(f"{_format_column(column.value)}", end="")
#     print("\r")
#     max_ = 0
#     for values in data.values():
#         if len(values) > max_:
#             max_ = len(values)
#     for index in range(max_):
#         for column in columns:
#             date, sec = data[column][index]
#             print(f" {_format_date_short(date)} {to_time(sec)} ", end="")
#         print("\r")

def _get_trainings(data: dict[tuple[str, str], dict[str, Any]]) -> list[str]:
    trainings: list[str] = []
    for key_1, key_2 in data:
        if key_1 not in trainings:
            trainings.append(key_1)
    return trainings

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
    date = date.split("-")
    return f"{date[0]}-{date[1]}"

def _print_cell_with_style_and_length(msg: str, length: int, style: CellStyle) -> None:
    add_space = length - len(msg)
    if add_space <= 0:
        message = msg
    elif add_space == 1:
        message = " " + msg
    else:
        message = " " + msg + (add_space - 1) * " "

    print(style.background_color + style.foreground_color + message + Style.RESET_ALL, end="")

def print_dashboard(data: dict[tuple[str, str], dict[str, Any]], sections: list[str], split_months: bool = False) -> None:
    trainings: list[str] = _get_trainings(data)
    length: int = 14
    _print_cell_with_length("Dates", 15)
    for col in sections:
        _print_cell_with_length(f"{col}", length)
    print("")
    month = _get_month(trainings[0])
    for date in trainings:
        current_month = _get_month(date)
        if month != current_month and split_months:
            month = current_month
            print("")

        _print_cell_with_length(date, 15)
        for col in sections:
            if (date, col) not in data.keys():
                _print_cell_with_length("", length)
            else:
                val = data[(date, col)]
                _print_cell_with_style_and_length(f"{to_time(val['value'])} ({val['order']})", length,
                                                  DASHBOARD_PRINT_STYLE[val['grade']])
        print("")


def compare_format(data: dict[str, Any]) -> str:
    s_lost: str = str(data["lost"])
    s_lost = s_lost if len(s_lost) > 1 else s_lost + " "
    lost: str = f"+{s_lost}"
    s_order: str = str(data["order"]) if data["order"] > 9 else " " + str(data["order"])
    return f"{to_time(data['value'])} ({s_order}) {lost}"


def print_compare(data_date_1: dict[str, Any], data_date_2: dict[str, Any]) -> None:
    print("\t", end="")
    print(f"\t{data_date_1['date']}", end="")
    print(f"\t{data_date_2['date']}", end="")
    print("\tdiff")
    for section_type in data_date_1["sections"]:
        print(f"{section_type}\t\t", end="")
        s1 = data_date_1['sections'][section_type]
        s2 = data_date_2['sections'][section_type]
        print(f"{compare_format(s1)}\t", end="")
        print(f"{compare_format(s2)}\t", end="")
        diff: int = s2["value"] - s1["value"]
        str_diff: str = str(diff) if diff < 0 else f"+{diff}"
        print(f"{str_diff}", end="")
        print("")
    for agg_type in data_date_1["aggregations"]:
        if len(agg_type) >= 10:
            print(f"{agg_type}\t", end="")
        else:
            print(f"{agg_type}\t\t", end="")
        a1 = data_date_1["aggregations"][agg_type]
        a1_ok: bool = False
        if a1:
            print(f"{compare_format(a1)}\t", end="")
            a1_ok = True
        else:
            print("\t\t", end="")
        a2 = data_date_2["aggregations"][agg_type]
        a2_ok: bool = False
        if a2:
            print(f"{compare_format(a2)}\t", end="")
            a2_ok = True
        else:
            print("\t\t", end="")
        if a1_ok and a2_ok:
            diff: int = a2["value"] - a1["value"]
            str_diff: str = str(diff) if diff < 0 else f"+{diff}"
            print(f"{str_diff}", end="")
        print("")
