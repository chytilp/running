from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RouteModel:
    name: str
    description: str


@dataclass
class TrainingsModel:
    dates: list[str] = field(default_factory=list)

@dataclass
class SectionModel:
    name: str
    value: int
    order: int
    grade: int
    lost: int
    time_convertible: bool

    @staticmethod
    def from_dict(name: str, data: dict[str, Any]) -> SectionModel:
        return SectionModel(
            name=name,
            **data
        )


@dataclass
class TrainingModel:
    date: str
    note: str | None
    sections: list[SectionModel]
    aggregations: list[SectionModel]


@dataclass
class SectionsModel:
    # various dates(trainings) , same section
    date_sections: dict[str, SectionModel]
    mark_date: str | None


@dataclass
class GradeModel:
    grade: int
    from_: int
    to_: int
    time_convertible: bool

@dataclass
class CellIdentModel:
    date: str
    section: str
    is_section: bool


@dataclass
class DashboardModel:
    data: dict[CellIdentModel, SectionModel] = field(default_factory=dict)
    sections: list[str] = field(default_factory=list)
    aggregations: list[str] = field(default_factory=list)


@dataclass
class CompareModel:
    data_1: TrainingModel
    date_2: TrainingsModel
