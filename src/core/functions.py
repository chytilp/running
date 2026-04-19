import json
from datetime import datetime
from pathlib import Path
from typing import Any
from copy import deepcopy

from src.core.aggregation_functions import create_calculate_aggregation
from src.core.auxiliary import try_parse_date, parse_date, intervals_to_sec
from src.core.grades import calculate_grades, update_section_or_aggregation_grades
from src.core.sorting import sort_section_or_aggregation, update_section_or_aggregation_data
from src.core.data_module import data as original_data
from src.utils.time import to_sec


def read(data: dict[str, Any], files: list[str], from_: str = "", to_: str = "") -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    dt_from: datetime | None = try_parse_date(from_)
    dt_to: datetime | None = try_parse_date(to_)
    if dt_from is None:
        dt_from = datetime(2024, 1, 1)
    if dt_to is None:
        dt_to = datetime.now()
    file_data: dict[str, dict[str, Any]] = json.load(open(Path(files[0]).resolve()))

    trainings = new_data["trainings"]
    for date, values in file_data.items():
        train_dt: datetime = parse_date(date)
        training_key = train_dt.strftime("%Y-%m-%d")
        disabled: bool | None = values.get("disabled")
        if disabled is True:
            continue

        if dt_from <= train_dt <= dt_to:
            trainings[training_key] = {"note": "", "sections": {}, "aggregations": {}}
            # note
            note = values.get("note")
            if note is not None:
                trainings[training_key]["note"] = note
            # sections
            for section, value in values["sections"].items():
                trainings[training_key]["sections"][section] = {"order": -1, "lost": -1, "grade": -1, "value": -1}
                trainings[training_key]["sections"][section]["value"] = to_sec(value)

            # intervals
            intervals = values.get("intervals")
            if intervals is not None:
                trainings[training_key]["intervals"] = {"values": intervals_to_sec(intervals["values"]),
                                                        "type": int(intervals["type"])}
    return new_data


def filter_(data: dict[str, Any], from_: str = "", to_: str = "") -> dict[str, Any]:
    if from_ == "" and to_ == "":
        return data
    date_from = datetime(1970,1,1)
    if from_:
        date_from = datetime.strptime(from_, "%Y-%m-%d")
    now = datetime.today()
    date_to = datetime(now.year, now.month, now.day)
    if to_:
        date_to = datetime.strptime(to_, "%Y-%m-%d")
    new_data = deepcopy(original_data)
    for date_key, values in data["trainings"].items():
        dt = datetime.strptime(date_key, "%Y-%m-%d")
        if date_from <= dt < date_to:
            new_data["trainings"][date_key] = values
    return new_data


def calculate_aggregations(data: dict[str, Any], aggregation_types: dict[str, list[str]]) -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    for aggregation in aggregation_types.keys():
        for training_key, training in new_data["trainings"].items():
            if "aggregations" not in training:
                training["aggregations"] = {}
            agg_fce = create_calculate_aggregation(aggregation_types)
            aggregation_value: dict = agg_fce(new_data, training_key, aggregation)
            if aggregation_value:
                training["aggregations"][aggregation] = aggregation_value
    return new_data


def sort_sections(data: dict[str, Any], sections: list[str]) -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    is_aggregation: bool = False
    for section in sections:
        grades = calculate_grades(data, section, is_aggregation)
        new_data = update_section_or_aggregation_grades(new_data, section, is_aggregation, grades)
        sort_result = sort_section_or_aggregation(new_data, section, is_aggregation, grades)
        new_data = update_section_or_aggregation_data(new_data, section, is_aggregation, sort_result)
    return new_data


def sort_aggregations(data: dict[str, Any], aggregations: list[str]) -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    is_aggregation: bool = True
    for aggregation in aggregations:
        grades = calculate_grades(data, aggregation, is_aggregation)
        new_data = update_section_or_aggregation_grades(new_data, aggregation, is_aggregation, grades)
        sort_result = sort_section_or_aggregation(new_data, aggregation, is_aggregation, grades)
        new_data = update_section_or_aggregation_data(new_data, aggregation, is_aggregation, sort_result)
    return new_data


def create_month_summary(data: dict[str, Any], month: str) -> dict[str, Any]:

    return data


def read_index(index_file: Path, data_type: str) -> tuple[list[str], dict[str, list[str]], list[str], list[str], list[str]]:
    index_data = json.load(open(index_file))
    files: list[str] = index_data[data_type]["files"]
    aggregations: dict[str, list[str]] = index_data[data_type]["aggregations"]
    sections: list[str] = index_data[data_type]["sections"]
    dashboard_sections: list[str] = index_data[data_type]["dashboard_sections"]
    dashboard_aggregations: list[str] = index_data[data_type]["dashboard_aggregations"]
    return files, aggregations, sections, dashboard_sections, dashboard_aggregations
