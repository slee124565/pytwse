

from datetime import date
from dateutil.relativedelta import relativedelta
from time import sleep

from twse import TWSE
from csvstore import CSVStore as stockstore

import logging
from cmd_base import CMDBase

logger = logging.getLogger(__name__)


class CMDUpdate(CMDBase):
    arg_year_month = 'year_month'
    arg_years_since = 'years_since'

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
            twse_json = TWSE.fetch_json(stock_no, t_date)
            if twse_json is None:
                logger.warning('twse.fetch_json {} {} fail'.format(stock_no, t_date))
            else:
                logger.debug('twse.fetch_json {} {} success'.format(stock_no, t_date))
                twse_data = twse_json.get('data')

                # save twse_data
                stockstore.save_twse_data(stock_no, twse_data)
                logger.info('stock {} data {} saved'.format(stock_no, t_date.strftime('%Y-%m')))
                sleep(0.3)
            t_date += relativedelta(months=1)
        logger.info('==')
        logger.info('')

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
    def add_parser_arg_years_since(cls, parser):
        parser.add_argument(
            cls.arg_years_since,
            type=int,
            help='years since for stock to fetch',
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
            help='update local stock csv file',
            parents=[base_parser])

        scmd_subparsers = cmd_parser.add_subparsers(title='sub-command')

        # update newly
        scmd_parser = scmd_subparsers.add_parser(
            'newly',
            help='create a new local stock csv file',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        cls.add_parser_arg_years_since(scmd_parser)
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
