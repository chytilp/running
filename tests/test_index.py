from pathlib import Path

from src.core.functions import read_index
from src.model.aggregation_desc import AggregationDesc, Filter


def test_old_format() -> None:
    files, aggregations, sections, dashboard_sections, dashboard_aggregations = read_index(
        Path(__file__).parent / "data" / "indexOld.json", "barr", 1)
    assert files == ["./data/example_data_1.json"]
    assert sections == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km"]
    assert list(aggregations.keys()) == ["1.round", "2.round", "rounds", "first5", "first9", "1.2km", "2.2km", "3.2km",
                                         "4.2km", "1.3km", "2.3km", "3.3km", "intervals_3", "intervals_5"]
    assert aggregations["1.round"] == ["1.km", "2.km", "3.km", "4.km"]
    assert aggregations["2.round"] == ["5.km", "6.km", "7.km", "8.km"]
    assert aggregations["rounds"] == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km"]
    assert dashboard_sections == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km"]
    assert dashboard_aggregations == ["1.round", "2.round", "rounds"]


def assert_aggregation_desc(agg_desc: AggregationDesc, expected_inputs: list[str], expected_reducer: str,
                            expected_filters: list[Filter]) -> None:
    assert agg_desc.inputs == expected_inputs
    assert agg_desc.reducer == expected_reducer
    assert agg_desc.filters == expected_filters


def test_new_format() -> None:
    files, aggregations, sections, dashboard_sections, dashboard_aggregations = read_index(
        Path(__file__).parent / "data" / "indexNew.json", "barr", 2)
    assert files == ["./data/example_data_1.json"]
    assert list(aggregations.keys()) == ["1.round", "under6", "woutFilters"]
    assert_aggregation_desc(aggregations["1.round"], ["1.km", "2.km", "3.km", "4.km"], "sum", [])
    assert_aggregation_desc(aggregations["under6"],
                            ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km", "10.km"], "len",
                            [Filter(operator="<", value=360)])
    assert_aggregation_desc(aggregations["woutFilters"],
                            ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km", "10.km"], "max",
                            [])