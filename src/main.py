import argparse

from src.config import Config, get_config
from src.core.functions import prepare_data
from src.core.index import read_index_file
from src.core.menu_funcs import (get_date, get_dates, get_section, get_aggregation, get_grades, get_compare,
                                 get_dashboard, get_top)
from src.model.index_data import IndexData


def main() -> None:
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
    parser.add_argument("--route", help="What route to use [barr,prok, tich, krus...]")
    # -------------
    args = parser.parse_args()
    config: Config = get_config()
    index_data: IndexData = read_index_file(config=config, version=2, route_name=args.route)

    new_data = prepare_data(index_data, args.start, args.end)
    args.func(data=new_data, arguments=args, dash_sections=index_data.dashboard_sections,
              dash_aggregations=index_data.dashboard_aggregations, sections=index_data.sections,
              aggregations=list(index_data.aggregations.keys()))

if __name__ == "__main__":
    main()
