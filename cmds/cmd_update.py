

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from time import sleep

from twse import TWSE
from csvstore import CSVStore as stockstore

import logging
from cmd_base import CMDBase
import random

logger = logging.getLogger(__name__)


class CMDUpdate(CMDBase):
    arg_year_month = 'year_month'
    arg_years_since = 'years_since'
    DATE_FORMAT = '%Y%m%d'

    @classmethod
    def sub_cmd_month(cls, args):
        # stock_no and years_since
        stock_no = getattr(args, cls.arg_stock_no)
        date_ym = getattr(args, cls.arg_year_month)
        tdate = datetime.strptime('{}15'.format(date_ym), cls.DATE_FORMAT).date()

        #  fetch stock csv
        stock_csv = TWSE.get_stock_csv(stock_no, tdate, with_header=True)

        #  update store
        stockstore.update_stock_store(stock_no, stock_csv)

    @classmethod
    def sub_cmd_newly(cls, args):
        # stock_no and years_since
        stock_no = getattr(args, cls.arg_stock_no)
        years_since = getattr(args, cls.arg_years_since)

        # date_since, date_end
        date_end = date.today()
        date_since = date_end + relativedelta(years=-years_since)
        t_date = date_since

        while t_date < date_end:
            # twse_data
            # twse_json = TWSE.fetch_json(stock_no, t_date, load_from_cached=False)
            stock_csv = TWSE.get_stock_csv(stock_no, t_date)
            if stock_csv is None:
                logger.warning('{} get_stock_csv {} {} fail'.format(cls, stock_no, t_date))
            else:
                # save twse_data
                stockstore.update_stock_store(stock_no, stock_csv)
                sleep(int(random.random()*10) % 3 + 0.5)
            t_date += relativedelta(months=1)
        logger.info('==')
        logger.info('')

    @classmethod
    def sub_cmd_last_to_now(cls, args):
        pass

    @classmethod
    def sub_cmd_remove_out_of_date(cls, args):
        pass

    @classmethod
    def add_parser_arg_years_since(cls, parser):
        parser.add_argument(
            cls.arg_years_since,
            type=int,
            nargs='?',
            help='years since for stock to fetch, default:%(default)s',
            default=3
        )

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
            help='update local stock csvstore file',
            parents=[base_parser])

        scmd_subparsers = cmd_parser.add_subparsers(title='sub-command')

        # update month
        scmd_parser = scmd_subparsers.add_parser(
            'month',
            help='update local stock csvstore file for specifi month',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        cls.add_parser_arg_ym(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_month)

        # update last-to-now
        scmd_parser = scmd_subparsers.add_parser(
            'last-to-now',
            help='update local stock csvstore file from last month to this month',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_last_to_now)

        # update newly
        scmd_parser = scmd_subparsers.add_parser(
            'newly',
            help='create a new local stock csvstore file',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        cls.add_parser_arg_years_since(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_newly)

        # update remove-old
        scmd_parser = scmd_subparsers.add_parser(
            'remove-out-of-date',
            help='remove local stock csvstore file for those row data out-of-date',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_remove_out_of_date)

        return cmd_parser
