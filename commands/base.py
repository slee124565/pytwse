import logging

class BaseCommand(object):
    ''''''
    
    def __init__(self,args=None,logger=None):
        self.args = args
        self.logger = logger or logging.getLogger(__name__)

    def run(self):
        raise Exception('abstract interface')