import json
from datetime import datetime
from pathlib import Path
from typing import Any
from copy import deepcopy

from src.core.aggregation_functions import create_calculate_aggregation
from src.core.auxiliary import try_parse_date, parse_date, intervals_to_sec, get_sorted_section_or_aggregation_values
from src.core.grades import calculate_grades, update_section_or_aggregation_grades
from src.core.sorting import compare_section_or_aggregation, update_section_or_aggregation_data
from src.core.data_module import data as original_data
from src.model.aggregation_desc import AggregationDesc, Filter, SortDefinition
from src.utils.time import to_sec


def read(data: dict[str, Any], files: list[str], from_: str = "", to_: str = "") -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    dt_from: datetime | None = try_parse_date(from_)
    dt_to: datetime | None = try_parse_date(to_)
    if dt_from is None:
        dt_from = datetime(2020, 1, 1)
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


def calculate_aggregations(data: dict[str, Any], aggregation_types: dict[str, Any]) -> dict[str, Any]:
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
    for section in sections:
        new_data = sort_section(new_data, section)
    return new_data


def sort_aggregations(data: dict[str, Any], aggregations: list[AggregationDesc]) -> dict[str, Any]:
    new_data: dict[str, Any] = deepcopy(data)
    for aggregation in aggregations:
        new_data = sort_aggregation(new_data, aggregation)
    return new_data

def sort_aggregation(data: dict[str, Any], aggregation: AggregationDesc) -> dict[str, Any]:
    sorted_agg_values = get_sorted_section_or_aggregation_values(data, aggregation.name, "aggregations",
                                                                 reverse=aggregation.reverse)
    grades = calculate_grades(sorted_agg_values, aggregation.reverse)
    new_data = update_section_or_aggregation_grades(data, aggregation.name, "aggregation_grades", grades.get_dict())
    sort_result = compare_section_or_aggregation(sorted_agg_values, grades, aggregation.reverse)
    new_data = update_section_or_aggregation_data(new_data, aggregation.name, "aggregations", sort_result)
    return new_data


def sort_section(data: dict[str, Any], section: str) -> dict[str, Any]:
    sorted_section_values = get_sorted_section_or_aggregation_values(data, section, "sections")
    grades = calculate_grades(sorted_section_values)
    new_data = update_section_or_aggregation_grades(data, section, "section_grades", grades.get_dict())
    sort_result = compare_section_or_aggregation(sorted_section_values, grades)
    new_data = update_section_or_aggregation_data(new_data, section, "sections", sort_result)
    return new_data


def create_month_summary(data: dict[str, Any], month: str) -> dict[str, Any]:

    return data


def read_index(index_file: Path, data_type: str, version: int = 1) -> tuple[list[str], dict[str, Any], list[str], list[str], list[str]]:
    index_data = json.load(open(index_file))
    if index_data.get(data_type) is None:
        raise ValueError(f"Unknown data type: {data_type}")

    files: list[str] = index_data[data_type]["files"]
    if version == 1:
        aggregations: dict[str, Any] = index_data[data_type]["aggregations"]
    elif version == 2:
        aggregations: dict[str, AggregationDesc] = {}
        aggregation_desc: dict[str, Any] = index_data[data_type]["aggregations"]
        for aag_name, agg_desc in aggregation_desc.items():
            operations: dict = agg_desc["operations"]
            filters: list[dict] = operations.get("filters") or []
            filters_objs: list[Filter] = []
            for filter_ in filters:
                filters_objs.append(Filter(
                    operator=filter_["operator"],
                    value=filter_["value"],
                ))
            sort_def: SortDefinition = SortDefinition.LESS_IS_BEST
            if agg_desc.get("sort_definition") is not None:
                sort_def = SortDefinition(agg_desc["sort_definition"])

            agg_obj = AggregationDesc(
                name=aag_name,
                inputs=agg_desc["inputs"],
                reducer=operations["reducer"],
                filters=filters_objs,
                sort_definition=sort_def,
            )
            aggregations[aag_name] = agg_obj
    else:
        raise Exception(f"Unknown version of aggregation description: {version}")

    sections: list[str] = index_data[data_type]["sections"]
    dashboard_sections: list[str] = index_data[data_type]["dashboard_sections"]
    dashboard_aggregations: list[str] = index_data[data_type]["dashboard_aggregations"]
    return files, aggregations, sections, dashboard_sections, dashboard_aggregations
