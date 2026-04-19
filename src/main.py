import argparse
import json
import os
from pathlib import Path
from typing import Any

import toml

from src.core.functions import read, filter_, calculate_aggregations, sort_sections, sort_aggregations, read_index
from src.core.data_module import data
from src.core.menu_funcs import get_date, get_dates, get_section, get_aggregation, get_grades, get_compare, \
    get_dashboard, get_top


def prepare_data(files: list[str], aggregations: dict[str, list[str]], sections: list[str], from_: str, to_: str
                 ) -> dict[str, Any]:
    new_data = read(data, files)
    new_data = filter_(new_data, from_=from_, to_=to_)
    aggregations_: list[str] = list(aggregations.keys())
    new_data = calculate_aggregations(new_data, aggregations)
    new_data = sort_sections(new_data, sections)
    return sort_aggregations(new_data, aggregations_)

def read_from_config() -> tuple[list[str], dict[str, list[str]], list[str], list[str], list[str]]:
    config = toml.load("./src/config.toml")
    index_file = config['indexLocation']
    data_type = config['defaultType']
    folder = os.path.dirname(os.path.realpath(__file__))
    files, aggregations, sections, dashboard_sections, dashboard_aggregations = read_index(Path(folder, index_file), data_type)
    return files, aggregations, sections, dashboard_sections, dashboard_aggregations

def main() -> None:
    files, aggregations, sections, dashboard_sections, dashboard_aggregations = read_from_config()

    parser = argparse.ArgumentParser(prog='simple_example')
    sub_parsers = parser.add_subparsers(help='sub-command help')
    # date command
    parser_date = sub_parsers.add_parser('date', help='date sub-command')
    parser_date.add_argument("date", help='date argument')
    parser_date.set_defaults(func=get_date)
    # dates command
    parser_dates = sub_parsers.add_parser('dates', help='dates sub-command')
    parser_dates.set_defaults(func=get_dates)
    # section command
    parser_section = sub_parsers.add_parser('section', help='section sub-command')
    parser_section.add_argument("section", help='section argument')
    parser_section.set_defaults(func=get_section)
    # aggregation command
    parser_aggregation = sub_parsers.add_parser('aggregation', help='aggregation sub-command')
    parser_aggregation.add_argument("aggregation", help='aggregation argument')
    parser_aggregation.set_defaults(func=get_aggregation)
    # grades command
    parser_grades = sub_parsers.add_parser('grades', help='grades sub-command')
    parser_grades.add_argument("--aggregation", help='aggregation argument', default=None)
    parser_grades.add_argument("--section", help='section argument', default=None)
    parser_grades.set_defaults(func=get_grades)
    # compare command
    parser_compare = sub_parsers.add_parser('compare', help='compare sub-command')
    parser_compare.add_argument("compare", help='compare argument (dates)')
    parser_compare.set_defaults(func=get_compare)
    # dashboard command
    parser_dashboard = sub_parsers.add_parser('dashboard', help='dashboard sub-command')
    parser_dashboard.set_defaults(func=get_dashboard)
    # top command
    parser_top = sub_parsers.add_parser('top', help='top sub-command')
    parser_top.add_argument("top", help='top argument (int)')
    parser_top.set_defaults(func=get_top)
    # month command
    # parser_month = sub_parsers.add_parser('month', help='top sub-command')
    # parser_month.add_argument("month", help='month argument (YYYY-MM-DD)')
    # parser_month.set_defaults(func=get_month)
    # ------------- global arguments ---
    parser.add_argument("--mark", default=None, help="mark argument (date)")
    parser.add_argument("--start", default="", help="start argument (date)")
    parser.add_argument("--end", default="", help="end argument (date)")
    # -------------
    args = parser.parse_args()
    new_data = prepare_data(files, aggregations, sections, args.start, args.end)
    args.func(data=new_data, arguments=args, sections=dashboard_sections, aggregations=dashboard_aggregations)

if __name__ == "__main__":
    main()
