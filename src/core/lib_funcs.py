from typing import Any

from src.config import Config, get_config
from src.core.data_module import get
from src.core.functions import prepare_data
from src.core.index import read_index_routes, read_index
from src.model.printing import RouteModel, TrainingsModel, TrainingModel, SectionsModel, SectionModel


def _prepare_data(route: RouteModel, from_: str, to_: str) -> dict[str, Any]:
    config = get_config()
    index_data = read_index(index_file=config.get_index_file_path(), route=route, version=2)
    return prepare_data(index_data=index_data, from_=from_, to_=to_)


def get_routes() -> list[RouteModel]:
    config = get_config()
    print(f"index file path: {config.get_index_file_path()}")
    routes = read_index_routes(config.get_index_file_path())
    return routes


def get_dates(route: RouteModel) -> TrainingsModel:
    data: dict[str, Any] = _prepare_data(route=route, from_="", to_="")
    dates: list[str] = [date for date in data["trainings"].keys()]
    return TrainingsModel(dates=dates)


def get_date(route: RouteModel, date: str) -> TrainingModel:
    data: dict[str, Any] = _prepare_data(route=route, from_="", to_="")
    date_data = get(data, ["trainings", date])
    sections: list[SectionModel] = []
    for section, section_data in date_data["sections"].items():
        sections.append(SectionModel.from_dict(section, section_data))

    aggregations: list[SectionModel] = []
    for agg, agg_data in date_data["aggregations"].items():
        aggregations.append(SectionModel.from_dict(agg, agg_data))

    return TrainingModel(date=date, note=date_data.get("note"), sections=sections, aggregations=aggregations)


def get_section(route: RouteModel, section: str, from_: str = "", to_: str = "", mark_date: str = "") -> SectionsModel:
    data: dict[str, Any] = _prepare_data(route=route, from_=from_, to_=to_)
    section = section.lower()
    data = get(data, ["trainings", "*", "sections", section])
    data = dict(sorted(data.items(), key=lambda item: item[1]["order"]))
    return SectionsModel()


def get_aggregation(route: RouteModel, aggregation: str) -> SectionsModel:
    return SectionsModel()