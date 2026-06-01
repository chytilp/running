import os
from pathlib import Path

from src.config import set_config_file
from src.core.lib_funcs import get_routes, get_dates, get_date
from src.model.printing import RouteModel, TrainingModel


def _get_new_config_path(rel_path: str) -> str:
    folder = os.path.dirname(os.path.realpath(__file__))
    return str(Path(folder, rel_path))


def test_get_routes() -> None:
    new_config_file = _get_new_config_path("./data/config.toml")
    set_config_file(new_config_file)
    routes = get_routes()
    assert len(routes) == 1
    assert routes[0].name == "barr"


def test_get_dates() -> None:
    new_config_file = _get_new_config_path("./data/config.toml")
    set_config_file(new_config_file)
    trainings = get_dates(RouteModel(name="barr", description=""))
    assert len(trainings.dates) == 3
    assert trainings.dates[0] == "2026-01-01"
    assert trainings.dates[1] == "2026-01-02"
    assert trainings.dates[2] == "2026-01-03"

def test_get_date() -> None:
    new_config_file = _get_new_config_path("./data/config.toml")
    set_config_file(new_config_file)
    training: TrainingModel = get_date(RouteModel(name="barr", description=""), "2026-01-02")
    assert training.date == "2026-01-02"
    assert len(training.sections) == 10
    assert len(training.aggregations) == 3