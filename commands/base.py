
import argparse
import logging
import os

class BaseCommand(object):
    
    
    @classmethod
    def get_base_args_parser(cls):
        base_parser = argparse.ArgumentParser(add_help=False)
        base_parser.add_argument(
            '--develop',
            action='store_true',
            help='set develop mode',
            default=False)
        base_parser.add_argument(
            '--debug',
            action='store_true',
            help='set logging level to DEBUG',
            default=False)
        base_parser.add_argument(
            '--cached',
            action='store_true',
            help='read from previous download',
            default=False)
        return base_parser
 

    def __init__(self, args, logger=None):
        ''''''
        
        self.args = args
        self.logger = logger or logging.getLogger(__name__)

        cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache_data')
        if not os.path.exists(cache_path):
            self.logger.debug('mkdir %s' % cache_path)
            os.mkdir(cache_path)
        setattr(args,'cache_path',cache_path)
    