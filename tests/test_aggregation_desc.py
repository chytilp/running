import pytest

from src.model.aggregation_desc import AggregationDesc, Filter

@pytest.mark.parametrize(
    "reducer, expected",
    (
        pytest.param("len", 3, id="len"),
        pytest.param("sum", 6, id="sum"),
    )
)
def test_aggregation_desc_wout_filters(reducer: str, expected: int) -> None:
    agg_desc = AggregationDesc(
        reducer=reducer,
    )
    values = [1, 2, 3]
    values = agg_desc.apply_filters(values)
    result: int = agg_desc.apply_reducer(values)
    assert result == expected


@pytest.mark.parametrize(
    "filters, reducer, expected",
    (
        pytest.param([Filter("==", 1),], "len", 1, id="(==,len)"),
        pytest.param([Filter("!=", 1),], "len", 9, id="(!=,len)"),
        pytest.param([Filter(">", 3),], "len", 7, id="(>,len)"),
        pytest.param([Filter(">=", 3),], "len", 8, id="(>=,len)"),
        pytest.param([Filter("<", 5),], "len", 4, id="(<,len)"),
        pytest.param([Filter("<=", 5),], "len", 5, id="(<=,len)"),

        pytest.param([Filter("==", 1),], "sum", 1, id="(==,sum)"),
        pytest.param([Filter("!=", 1),], "sum", 54, id="(!=,sum)"),
        pytest.param([Filter(">", 3),], "sum", 49, id="(>,sum)"),
        pytest.param([Filter(">=", 3),], "sum", 52, id="(>=,sum)"),
        pytest.param([Filter("<", 5),], "sum", 10, id="(<,sum)"),
        pytest.param([Filter("<=", 5),], "sum", 15, id="(<=,sum)"),

        pytest.param([Filter("==", 1),], "min", 1, id="(==,min)"),
        pytest.param([Filter("!=", 1),], "min", 2, id="(!=,min)"),
        pytest.param([Filter(">", 3),], "min", 4, id="(>,min)"),
        pytest.param([Filter(">=", 3),], "min", 3, id="(>=,min)"),
        pytest.param([Filter("<", 5),], "min", 1, id="(<,min)"),
        pytest.param([Filter("<=", 5),], "min", 1, id="(<=,min)"),

        pytest.param([Filter("==", 1), ], "max", 1, id="(==,max)"),
        pytest.param([Filter("!=", 1), ], "max", 10, id="(!=,max)"),
        pytest.param([Filter(">", 3), ], "max", 10, id="(>,max)"),
        pytest.param([Filter(">=", 3), ], "max", 10, id="(>=,max)"),
        pytest.param([Filter("<", 5), ], "max", 4, id="(<,max)"),
        pytest.param([Filter("<=", 5), ], "max", 5, id="(<=,max)"),

        pytest.param([Filter("==", 1), ], "avg", 1, id="(==,avg)"),
        pytest.param([Filter("!=", 1), ], "avg", 6, id="(!=,avg)"),
        pytest.param([Filter(">", 3), ], "avg", 7, id="(>,avg)"),
        pytest.param([Filter(">=", 3), ], "avg", 7, id="(>=,avg)"),
        pytest.param([Filter("<", 5), ], "avg", 3, id="(<,avg)"),
        pytest.param([Filter("<=", 5), ], "avg", 3, id="(<=,avg)"),
    )
)
def test_aggregation_desc_with_filters(filters: list[Filter], reducer: str, expected: int) -> None:
    values: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    agg_desc = AggregationDesc(
        reducer=reducer,
        filters=filters
    )
    values = agg_desc.apply_filters(values)
    result: int = agg_desc.apply_reducer(values)
    assert result == expected
