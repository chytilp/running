from dataclasses import dataclass
from typing import Any


@dataclass
class IndexData:
    version: int
    files: list[str]
    aggregations: dict[str, Any]
    sections: list[str]
    dashboard_sections: list[str]
    dashboard_aggregations: list[str]
