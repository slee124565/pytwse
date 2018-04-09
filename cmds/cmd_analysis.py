
import logging
from cmd_base import CMDBase

logger = logging.getLogger(__name__)


class CMDAnalysis(CMDBase):

    @classmethod
    def sub_cmd_detail(cls, args):
        pass

    @classmethod
    def get_cmd_parser(cls, base_parser, subparsers):
        cmd_parser = subparsers.add_parser(
            'analysis',
            description=__doc__,
            help='analysis local stock csv file and print a report',
            parents=[base_parser])

        scmd_subparsers = cmd_parser.add_subparsers(title='sub-command')

        # analysis detail
        scmd_parser = scmd_subparsers.add_parser(
            'detail',
            help='detail analysis report',
            parents=[base_parser])
        cls.add_parser_arg_stock_no(scmd_parser)
        scmd_parser.set_defaults(func=cls.sub_cmd_detail)

        return cmd_parser
