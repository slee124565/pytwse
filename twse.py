#!/usr/bin/env python

import argparse
import logging
import sys
from commands.list import List
from commands.update import Update
import os

def _list(args):
    ''''''
    worker = List(args=args)
    worker.run()
    
def _update(args):
    ''''''
    worker = Update(args=args)
    worker.run()
    
if __name__ == '__main__':
    
    #-> base parser
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
    
    #-> program parser start
    parser = argparse.ArgumentParser(
        description='TWSE Site (http://www.twse.com.tw/) Stock Data Parser')

    subparsers = parser.add_subparsers(
        title='commands')
    
    #-> [list] command arguments
    list_parser = subparsers.add_parser(
        'list',
        help='list twse company id',
        parents=[base_parser])
    list_parser.add_argument('target',
                             choices=['stock','otc','all'],
                             help='target twse market')
    list_parser.add_argument(
        '--cached',
        action='store_true',
        help='read from previous download',
        default=False)
    list_parser.set_defaults(func=_list)

    #-> [update] command arguments
    update_parser = subparsers.add_parser(
        'update',
        help='update twse exchange data',
        parents=[base_parser])
    ex_group = update_parser.add_mutually_exclusive_group()
    ex_group.add_argument('--period', 
                        help='update period: (<n>d | <n>w | <n>m | <n>y)')
    ex_group.add_argument('--until_now',
                        action='store_true',
                        help='update since last time updated to now',
                        default=False)
    update_parser.add_argument('--interval',
                        help="1d, 1wk, or 1mo, default: %(default)s",
                        default='1d')
    update_parser.add_argument('target',
                               help="target twse market (stock only now) or company id")
    update_parser.set_defaults(func=_update)
    
    
    args = parser.parse_args()
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(
        format='[%(levelname)s]: %(message)s',
        level=log_level)

    output = os.path.join(os.path.dirname(__file__),'data')
    if not os.path.exists(output):
        os.mkdir(output)
    setattr(args,'data_path',output)
    
    args.func(args)
    
    
    
    