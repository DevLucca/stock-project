import os
import yfinance as yf

class ticker(  ):

    def get( self, sheet ):
        self.tickers = sheet.worksheet( os.getenv( 'TICKER_PAGE' ) ).get_all_records(  )
        return self

    def group( self, categories ):
        tickers = {category:[] for category in categories}
        for ticker in self.tickers:
            try:
                tickers[str( ticker['Category'] )].append( ticker )
            except:
                pass
        self.tickers = tickers
        return self

    def search( self, category ):
        data = []
        for ticker in self.tickers[category]:
            tickerName = ticker['Ticker']
            if bool( ticker['Active'] ):
                ticker = yf.Ticker( tickerName )
                ticker = ticker.history(period="daily")
                if len( ticker.values.tolist() ) >= 1:
                    dataTicker = ticker.values.tolist(  )[0]
                    tmp = {'Ticker': tickerName, 
                           'Open': dataTicker[0],
                           'High': dataTicker[1], 
                           'Low': dataTicker[2], 
                           'Close': dataTicker[3], 
                           'Dividends': dataTicker[4], 
                           'Stock': dataTicker[5], 
                           'Splits': dataTicker[6]
                    }
                    dataTicker = tmp
                else:
                    dataTicker = {'Ticker': tickerName, 
                           'Open': 0,
                           'High': 0, 
                           'Low': 0, 
                           'Close': 0, 
                           'Dividends': 0, 
                           'Stock': 0, 
                           'Splits':0
                    }
                data.append( dataTicker )
        return data
            