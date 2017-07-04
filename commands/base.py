
import argparse
import logging
import os

class BaseCommand(object):
    
    cache_path = './cache_data'
    
    @classmethod
    def _get_cache_path(cls):
        cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache_data')
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        return cache_path

    def __init__(self, **args):
        ''''''

        if args.get('logger'):
            self.logger = args.get('logger')
        else:
            log_level = logging.DEBUG
            log_format = '%(asctime)s [%(levelname)s]: %(message)s'
            log_datefmt = '%H:%M:%S.%f'
            logging.basicConfig(format=log_format,level=log_level,datefmt=log_datefmt)
            self.logger = logging.getLogger(__name__)
        
        if args.get('cache_path'):
            if os.path.exists(args.get('cache_path')):
                self.cache_path = args.get('cache_path')
            else:
                self.logger.warning('%s cache_path % not exist' % (
                    self.__class__.__name__,args.get('cache_path')))
        else:
            self.cache_path = BaseCommand._get_cache_path()       

        
    def run(self):
        raise Exception('%s interface method <run> not implemented' %
                        self.__class__.__name__)
    