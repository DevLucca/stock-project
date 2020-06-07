import os
import yfinance as yf

class ticker(  ):

    def get( self, sheet ):
        self.tickers = sheet.worksheet( os.getenv( 'TICKER_PAGE' ) ).get_all_records(  )
        return self

    def group( self, categories ):
        tickers = {category:[] for category in categories}
        for ticker in self.tickers:
            tickers[str( ticker['Category'] )].append( ticker )
        self.tickers = tickers
        return self

    def search( self, category ):
        for ticker in self.tickers[category]:
            
            ticker = yf.Ticker(ticker['Ticker'])
            ticker = ticker.history(period="max")
            print(ticker)
            break