
import logging
from cmd_base import CMDBase

logger = logging.getLogger(__name__)


class CMDUpdate(CMDBase):
    arg_year_month = 'year_month'

    @classmethod
    def sub_cmd_newly(cls, args):
        pass

    @classmethod
    def sub_cmd_month(cls, args):
        pass

    @classmethod
    def sub_cmd_last_to_now(cls, args):
        pass

    @classmethod
    def sub_cmd_remove_out_of_date(cls, args):
        pass

    @classmethod
    def add_parser_arg_ym(cls, parser):
        parser.add_argument(
            cls.arg_year_month,
            type=int,
            help='yyyyMM')

    @classmethod
    def get_cmd_parser(cls, base_parser, subparsers):
        cmd_parser = subparsers.add_parser(
            'update',
            description=__doc__,
            help='update local stock csv file',
            parents=[base_parser])

        scmd_subparsers = cmd_parser.add_subparsers(title='sub-command')

        # update newly
        scmd_parser = scmd_subparsers.add_parser(
            'newly',
            help='create a new local stock csv file',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_newly)

        # update month
        scmd_parser = scmd_subparsers.add_parser(
            'month',
            help='update local stock csv file for specifi month',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        cls.add_parser_arg_ym(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_month)

        # update last-to-now
        scmd_parser = scmd_subparsers.add_parser(
            'last-to-now',
            help='update local stock csv file from last month to this month',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_last_to_now)

        # update remove-old
        scmd_parser = scmd_subparsers.add_parser(
            'remove-out-of-date',
            help='remove local stock csv file for those row data out-of-date',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_remove_out_of_date)

        return cmd_parser
