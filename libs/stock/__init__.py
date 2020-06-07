from .cron import cron

class stocker(  ):
    def __init__( self, GSclient ):
        self.GSclient = GSclient
        cron( self.GSclient )