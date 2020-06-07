import os
import json
import time
import threading
from .ticker import ticker
from datetime import datetime, timedelta

class cron(  ):
    def __init__( self, GSclient ):
        self.GSclient = GSclient
        self.sheet    = self.GSclient.open( os.getenv( 'SHEETNAME' ) )
        self.cronLog  = json.load( open( os.path.join( os.getcwd(  ), 'runlog.json' ), 'r') )
        categories    = self.__getCron(  )

        self.__adjustRunLog( categories )

        self.ticker = ticker(  )
        self.ticker.get( self.sheet ).group( list( self.cronLog.keys(  ) ) )

        for category in categories:
            self.__cronControll( category )

    def __getCron( self ):
        """
        Retorna os niveis de categoria na planilha.
            * Retorna json
        """
        return self.sheet.worksheet( os.getenv( 'CRON_PAGE' ) ).get_all_records(  )

    def __adjustRunLog( self, categories ):
        """
        Ajusta o arquivo runlog.json, lendo as configuracoes de log na planilha.
        """
        for category in categories:
            if str( category['Category'] ) not in list( self.cronLog.keys(  ) ):
                print('Category not in list, adding.', category)
                self.cronLog[str( category['Category'] )] = {
                    'lastRun': None,
                    'isRunning': False
                }

        for logCategory in list( self.cronLog.keys(  ) ):
            if int( logCategory ) not in [category['Category'] for category in categories]:
                print( f"Cron not in spreadsheet, removing from category. CategoryID: {logCategory}" )
                del self.cronLog[logCategory]
        self.__saveRunLog(  )
        return
        
    def __cronControll( self, category ):
        """
        Controla a execucao dos robos.
        """

        if not self.cronLog[str( category['Category'] )]['isRunning']:
            print( f"Job not running. Starting CategoryID: {category['Category']}" )
            if self.cronLog[str( category['Category'] )]['lastRun'] is None:
                print( f"First job run. Stating CategoryID: {category['Category']}" )
                thr = threading.Thread( target=self.__run, kwargs=category )
                thr.start(  )
            else:
                last_run = datetime.strptime( self.cronLog[str( category['Category'] )]['lastRun'], '%Y-%m-%d %H:%M:%S.%f' )
                now_delta = datetime.now(  ) - timedelta( minutes=float( str( category['Time'] ).replace( ',','.' ) ) )
                if last_run <= now_delta:
                    thr = threading.Thread( target=self.__run, kwargs=category )
                    thr.start(  )
                    print( 'Started Sucessfuly...' )
                else:
                    print( 'Job didn\'t start. Last run bigger than time delta.' )
        else:
            print( f"Job already running... CategoryID: {category['Category']}" )
        return

    def __run( self, Category, Description, Time ):
        """
        Executa os robos.
        """
        self.cronLog[str( Category )]['isRunning'] = True

        ###########
        self.ticker.search( str( Category ) )
        ###########

        self.cronLog[str( Category )]['lastRun'] = str( datetime.now(  ) )
        self.cronLog[str( Category )]['isRunning'] = False
        self.__saveRunLog(  )
        return

    def __saveRunLog( self ):
        """
        Salva o arquivo runlog.json
        """
        with open( os.path.join( os.getcwd(  ), 'runlog.json' ), 'w') as f:
            json.dump( self.cronLog, f, ensure_ascii=False )
            f.close(  )
        return
