
from base import BaseCommand

class Update(BaseCommand):
    ''''''
    
    def __init__(self,args=None,logger=None):
        BaseCommand.__init__(self, args=args, logger=logger)

    def run(self):
        ''''''
        self.logger.debug('update run with args: %s' % self.args)    