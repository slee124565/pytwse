#!/usr/bin/env python

import argparse
import logging
import sys
from commands.im_index import ImIndex
from commands.base import BaseCommand
import os
from datetime import datetime

def cmd_im_index_execute(args):
    ''''''
    worker = ImIndex(args=args)
    worker.run()
    
class TWSE(BaseCommand):
    
    def __init__(self, *args, **kwargs):
        ''''''
        super(TWSE,self).__init__(*args, **kwargs)
        
    def get_im_index(self):
        ''''''
    
if __name__ == '__main__':
        
    #-> program parser start
    parser = argparse.ArgumentParser(
        description='TWSE Site (http://www.twse.com.tw/) Exchange Data Parser')

    subparsers = parser.add_subparsers(
        title='commands')
    
    #-> [im_index] command arguments
    im_index_parser = ImIndex.add_cmd_parser(subparsers)
    im_index_parser.set_defaults(func=cmd_im_index_execute)
    
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
    
    
    
    