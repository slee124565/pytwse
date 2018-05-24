

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
    YEAR_SINCE = 3

    @classmethod
    def sub_cmd_month(cls, args):
        # stock_no and years_since
        stock_no = getattr(args, cls.arg_stock_no)
        date_ym = getattr(args, cls.arg_year_month)
        if date_ym is None:
            tdate = date.today()
        else:
            tdate = datetime.strptime('{}15'.format(date_ym), cls.DATE_FORMAT).date()

        logger.debug('{} sub_cmd_month with stock {} and date {}'.format(cls.__name__, stock_no, tdate))

        #  fetch stock csv update forced
        TWSE.fetch_json(stock_no, tdate, False)

        #  get stock csv data
        stock_csv = TWSE.get_stock_csv(stock_no, tdate, with_header=True)

        #  update store
        stockstore.store_update_with_csv(stock_no, stock_csv)

    @classmethod
    def sub_cmd_store(cls, args):
        stock_no = getattr(args, cls.arg_stock_no)
        years_since = getattr(args, cls.arg_years_since)

        stock_df = stockstore.store_get_dataframe(stock_no)
        if stock_df is not None:
            date_since = stock_df.index[-1].date()
        else:
            date_since = date.today() + relativedelta(years=-years_since)

        logger.debug('sub_cmd_stock {} last date {}'.format(stock_no, date_since))
        t_date = date_since
        t_today = date.today()

        updates = []
        while int(t_date.strftime('%Y%m')) <= int(t_today.strftime('%Y%m')):
            TWSE.fetch_json(stock_no=stock_no, tdate=t_date, load_from_cached=False)
            stock_csv = TWSE.get_stock_csv(stock_no, t_date, with_header=False)
            if stock_csv is not None:
                updates.append(stock_csv)

            delay = int(random.random()*10) % 3 + 0.5
            sleep(delay)
            t_date += relativedelta(months=1)

        if len(updates) > 0:
            updates.insert(0, ','.join(TWSE.DATA_FIELDS))
            # logger.info('updates:\n{}'.format(str(updates)))
            stockstore.store_update_with_csv(stock_no, '\n'.join(n for n in updates))
        else:
            logger.warning('{} sub_cmd_store fail, no stock_csv downloaded'.format(cls.__name__))

    @classmethod
    def sub_cmd_out_of_date(cls, args):
        stock_no = getattr(args, cls.arg_stock_no)
        years_since = getattr(args, cls.arg_years_since)
        date_before = date.today() + relativedelta(years=-years_since)
        logger.debug('{} sub_cmd_out_of_date stock {} date before {}'.format(
            cls.__name__, stock_no, date_before))

        stock_df = stockstore.store_get_dataframe(stock_no)
        if stock_df:
            shape_origin = stock_df.shape
            stock_df = stock_df[date_before:]
            shape_current = stock_df.shape
            stockstore.store_save_dataframe(stock_no, stock_df)
            logger.info('{} sub_cmd_out_of_date from {} to {}'.format(
                cls.__name__, shape_origin, shape_current))
        else:
            logger.error('{} sub_cmd_out_of_date fail'.format(cls.__name__))

    @classmethod
    def add_parser_arg_years_since(cls, parser):
        parser.add_argument(
            cls.arg_years_since,
            type=int,
            nargs='?',
            help='years since for stock to fetch, default:%(default)s',
            default=cls.YEAR_SINCE
        )

    @classmethod
    def add_parser_arg_ym(cls, parser):
        parser.add_argument(
            cls.arg_year_month,
            type=int,
            nargs='?',
            help='yyyyMM',
            default=None
        )

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

        # update stock
        scmd_parser = scmd_subparsers.add_parser(
            'store',
            help='update local stock csvstore file from last month to this month',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        cls.add_parser_arg_years_since(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_store)

        # update remove-old
        scmd_parser = scmd_subparsers.add_parser(
            'out-of-date',
            help='remove local stock csvstore file for those row data out-of-date',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        cls.add_parser_arg_years_since(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_out_of_date)

        return cmd_parser
