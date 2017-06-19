#!/usr/bin/env python

import argparse
import logging
import sys
from commands.list import List
from commands.update import Update

logger = logging.getLogger(__name__)

class TWSE(object):
    
    def __init__(self,args=None,logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.args = args

        if not hasattr(self, args.command):
            self.logger.error('Unrecognized command %s' % args.command)
            sys.exit(1)
        else:
            self.worker = getattr(self, self.args.command)()
                
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
        cmd_args = parser.parse_args(self.args.cmd_args)
        self.logger.debug('list command with args %s' % cmd_args)
        return List(args=self.args,logger=self.logger)
    
    def update(self):
        parser = argparse.ArgumentParser(
            description='Download stock trading data from TWSE'
            )
        parser.add_argument('id', help='company id')
        parser.add_argument('period', help='fetch data period: 3m or 3y; m for month, y for year')
        cmd_args = parser.parse_args(self.args.cmd_args)
        self.logger.debug('list command with args %s' % cmd_args)
        return Update(args=self.args,logger=self.logger)
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description='TWSE Site (http://www.twse.com.tw/) Stock Data Parser',
        usage='''twse <command> [<args>]
            
The most commonly use twse commands are:
    list <args>      List stock market id and name from TWSE
    update <args>    Update stock data for local storage from TWSE
''')

    parser.add_argument(
        'command',
        help='command to execute')

    parser.add_argument(
        '--develop',
        action='store_true',
        help='set develop mode',
        default=False)

    parser.add_argument(
        '--debug',
        action='store_true',
        help='print debug message',
        default=False)
    
    parser.add_argument(
        'cmd_args', 
        nargs=argparse.REMAINDER)
    
    args = parser.parse_args()
    
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='[%(levelname)s]: %(message)s',
        level=log_level)

    twse = TWSE(args=args)
    twse.worker.run()
    