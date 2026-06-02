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

    def __hash__(self) -> int:
        return hash(self.date + "," + self.section)

    def __eq__(self, other: Any) -> bool:
        return hash(self) == hash(other)

    def __lt__(self, other: Any):
        return f"{self.date},{str(self.is_section)},{self.section}" <= f"{other.date},{str(other.is_section)},{other.section}"

@dataclass
class DashboardModel:
    data: dict[CellIdentModel, SectionModel] = field(default_factory=dict)
    sections: list[str] = field(default_factory=list)
    aggregations: list[str] = field(default_factory=list)


@dataclass
class CompareModel:
    data_1: TrainingModel
    data_2: TrainingModel
