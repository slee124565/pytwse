
import argparse
import logging
import os

class BaseCommand(object):
    
    
    @classmethod
    def add_parser_argument(cls,parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            help='set logging level to DEBUG',
            default=False)
        parser.add_argument(
            '--cached',
            action='store_true',
            help='read from previous download',
            default=False)

    @classmethod
    def get_cache_path(cls):
        cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache_data')
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        return cache_path

    def __init__(self, args, logger=None):
        ''''''
        
        self.args = args
        self.logger = logger or logging.getLogger(__name__)

        setattr(args,'cache_path',BaseCommand.get_cache_path())
    