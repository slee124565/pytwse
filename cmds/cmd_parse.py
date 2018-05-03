
import sys
import pandas as pd
from csvstore import CSVStore as stockstore
import logging
from cmd_base import CMDBase

logger = logging.getLogger(__name__)


class CMDParse(CMDBase):

    arg_group_by = 'groupby'

    @classmethod
    def sub_cmd_parse_group(cls, args):
        stock_no = getattr(args, cls.arg_stock_no)
        groupby = getattr(args, cls.arg_group_by)
        stock_df = stockstore.store_get_dataframe(stock_no)
        if stock_df is None:
            logger.warning('{} sub_cmd_parse_group stock {} without existing data'.format(
                cls.__name__, stock_no))
        else:
            report_serial = stock_df.groupby(by=pd.Grouper(freq=groupby)).size()
            sys.stdout.write('stock {} groupby {} report:\n'.format(stock_no, groupby))
            for idx, row in report_serial.iteritems():
                sys.stdout.write('{}: {}\n'.format(idx.date(), row))
                # logger.info('{}, {}'.format(idx, row))
        pass

    @classmethod
    def add_parser_arg_groupby(cls, parser):
        parser.add_argument(
            cls.arg_group_by,
            choices=['M', 'A'],
            type=lambda c: c.upper(),
            nargs='?',
            help='dataframe group freq. Yearly(A) or Monthly(M), default:%(default)s',
            default='M'
        )

    @classmethod
    def get_cmd_parser(cls, base_parser, subparsers):
        cmd_parser = subparsers.add_parser(
            'parse',
            description=__doc__,
            help='parse local stock csvstore and print report',
            parents=[base_parser])

        scmd_subparsers = cmd_parser.add_subparsers(title='sub-command')

        # parse gropu
        scmd_parser = scmd_subparsers.add_parser(
            'group',
            help='print stock yearly|monthly group report',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        cls.add_parser_arg_groupby(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_parse_group)

        return cmd_parser
