
import logging

class List(object):
    ''''''
    
    def __init__(self,args=None,logger=None):
        self.args = args
        self.logger = logger or logging.getLogger(__name__)
    
    def run(self):
        ''''''
        self.logger.info('list run with args: %s' % self.args)