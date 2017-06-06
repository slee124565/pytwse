#!/usr/bin/env python

import argparse
import logging
import sys

logger = logging.getLogger(__name__)

class TWSE(object):
    
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='TWSE Site (http://www.twse.com.tw/) Parser',
            usage='''twse <command> [<args>]
            
The most commonly use twse commands are:
    stock_list        List all stock id and name from TWSE
    stock_update      Download stock trading data from TWSE
'''
            )
        parser.add_argument('command',
                           help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            logger.error('Unrecognized command %s' % args.command)
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()
        
    def stock_list(self):
        parser = argparse.ArgumentParser(
            description='List all stock id and name from TWSE'
            )
        logger.debug('stock_list cmd execution')
        print('stock_list cmd execution')
    
    def stock_update(self):
        parser = argparse.ArgumentParser(
            description='Download stock trading data from TWSE'
            )
        parser.add_argument('stock_id')
        parser.add_argument('period')
        args = parser.parse_args(sys.argv[2:])
        print('stop_update execution with stock %s and period %s' % (
            args.stock_id,args.period
            ))
    
if __name__ == '__main__':
    
    TWSE()
    