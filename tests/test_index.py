from pathlib import Path

from src.core.functions import read_index


def test_old_format() -> None:
    files, aggregations, sections, dashboard_sections, dashboard_aggregations = read_index(
        Path(__file__).parent / "data" / "index.json", "barr")
    assert files == ["./data/example_data_1.json"]
    assert sections == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km", "9.km"]
    assert list(aggregations.keys()) == ["1.round", "2.round", "rounds", "first5", "first9", "1.2km", "2.2km", "3.2km",
                                         "4.2km", "1.3km", "2.3km", "3.3km", "intervals_3", "intervals_5"]
    assert dashboard_sections == ["1.km", "2.km", "3.km", "4.km", "5.km", "6.km", "7.km", "8.km"]
    assert dashboard_aggregations == ["1.round", "2.round", "rounds"]

def test_new_format() -> None:
    files, aggregations, sections, dashboard_sections, dashboard_aggregations = read_index(
        Path(__file__).parent / "data" / "indexNew.json", "barr")
    assert files == ["./data/example_data_1.json"]
