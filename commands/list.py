
from base import BaseCommand

class List(object):
    ''''''
    
    def __init__(self,args=None,logger=None):
        BaseCommand.__init__(self, args=args, logger=logger)
    
    def run(self):
        ''''''
        self.logger.debug('list run with args: %s' % self.args)