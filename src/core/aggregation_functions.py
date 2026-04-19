from typing import Any, Protocol


def _sum_sections(data: dict[str, Any], training: str, sections: list[str]) -> tuple[bool, int]:
    sections_data: dict = data["trainings"][training]["sections"]
    inputs: list[int] = []
    for input_section in sections:
        if input_section not in sections_data.keys():
            return False, 0
        inputs.append(data["trainings"][training]["sections"][input_section]["value"])
    return True, sum(inputs)

def _sum_intervals(data: dict[str, Any], training: str, indexes: list[int]) -> tuple[bool, int]:
    if "intervals" not in data["trainings"][training].keys():
        return False, 0
    intervals_data: list[int] = data["trainings"][training]["intervals"]["values"]
    values: list[int] = []
    for index in indexes:
        try:
            values.append(intervals_data[index])
        except IndexError:
            return False, 0
    return True, sum(values)


class CalculateAggregationFunc(Protocol):
    def __call__(self, data: dict[str, Any], training: str, aggregation_type: str) -> dict[str, Any]:
        ...


def create_calculate_aggregation(aggregations_def: dict[str, list[str]]) -> CalculateAggregationFunc:

    def prepare_output(ok: bool, result: int) -> dict[str, Any]:
        if not ok:
            return {}
        return {"value": result, "order": -1, "lost": -1, "grade": -1}

    def calculate_aggregation(data: dict[str, Any], training: str, aggregation_type: str) -> dict[str, Any] | None:
        if aggregation_type not in aggregations_def.keys():
            return prepare_output(False, 0)

        sections = aggregations_def[aggregation_type]
        if aggregation_type.startswith("intervals"):
            indexes: list[int] = [int(sec.split("/")[1])  for sec in sections]
            ok, result = _sum_intervals(data, training, indexes)
        else:
            ok, result = _sum_sections(data, training, sections)
        return prepare_output(ok, result)

    return calculate_aggregation
