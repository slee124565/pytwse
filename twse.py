#!/usr/bin/env python

import logging
logger = logging.getLogger(__name__)

def stock_update_handler(args):
    logger.debug('cmd stock_update for stock %s with period %s' % (
                                                            args.stock,
                                                            args.period))

def stock_list_handler(args):
    print('stock_list_handler')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='TWSE Site Parser',
        epilog="""\
NOTE: no security measures are implemented
""")

    subparsers = parser.add_subparsers(title='subcommands')
    
    #-> create subcommand stock_update
    parser_update = subparsers.add_parser('stock_update',
                                          help='update stock exchange data from TWSE')
    parser_update.add_argument('-s','--stock',
                               type=int,
                               help='stock id')
    parser_update.add_argument('-p','--period',
                               help='duration period to update, format: 1y, 2m')
    parser_update.set_defaults(func=stock_update_handler)
    
    
    #-> create subcommand stock_list
    parser_slist = subparsers.add_parser('stock_list',
                                         help='list all stock id and name from TWSE')
    parser_slist.set_defaults(func=stock_list_handler)
    
    args = parser.parse_args()
    args.func(args)