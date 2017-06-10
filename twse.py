#!/usr/bin/env python

import argparse
import logging
import sys

logger = logging.getLogger(__name__)

class TWSE(object):
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        parser = argparse.ArgumentParser(
            description='TWSE Site (http://www.twse.com.tw/) Parser',
            usage='''twse <command> [<args>]
            
The most commonly use twse commands are:
    list                List all stock market companies id and name from TWSE
    update <id> <3y>    Download last 3 years market trading exchange daily data for company <id> from TWSE
'''
            )
        parser.add_argument('command',
                           help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            self.logger.error('Unrecognized command %s' % args.command)
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()
        
    def list(self):
        parser = argparse.ArgumentParser(
            description='List all stock id and name from TWSE'
            )
        parser.add_argument('--stock',
                            action='store_true',
                            help='Stock market',
                            default=False)
        parser.add_argument('--otc',
                            action='store_true',
                            help='OTC market',
                            default=False)
        args = parser.parse_args(sys.argv[2:])
        self.logger.info('list market info: stock %s, otc %s' % (args.stock,args.otc))
    
    def update(self):
        parser = argparse.ArgumentParser(
            description='Download stock trading data from TWSE'
            )
        parser.add_argument('id', help='company id')
        parser.add_argument('period', help='fetch data period: 3m or 3y; m for month, y for year')
        args = parser.parse_args(sys.argv[2:])
        self.logger.info('update market trading exchange data for id %s and period %s' % (
            args.id,args.period
            ))
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    TWSE()
    