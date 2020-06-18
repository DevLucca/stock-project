"""
    AUTOR := <Lucca Leme Marques at devlucca@gmail.com>
    Copyrights © 2020 | Lucca Leme Marques
"""
######### IMPORTS #########
import os
import time
import json
import dotenv
import gspread
import datetime
import libs.stock as stock
from ast import literal_eval
from distutils.util import strtobool
from oauth2client.service_account import ServiceAccountCredentials

########### ENV ###########
dotenv.load_dotenv(  )
os.chdir('./')
oauth_creds = json.loads( os.getenv( 'SPREADSHEET_OAUTH') )
DEBUG = bool(strtobool(os.getenv( 'ENV_DEBUG' )))
    # GOOGLE SPREADSHEETS AUTH #############
SCOPE = literal_eval( os.getenv( 'SCOPE' ) )
credential = ServiceAccountCredentials.from_json_keyfile_dict( oauth_creds, SCOPE )
GSclient = gspread.authorize( credential )

########### MAIN ###########
def main(  ):
    while True:
        if 10 <= datetime.datetime.now(  ).hour < 18:
            stock.stocker( GSclient )
            time.sleep(60)
            print('============================================')
        else:
            stopTime = 3600 * 10
            print( f'Market closed! Search Stopped for {stopTime} seconds / {int( stopTime/3600 )} hours.' )
            time.sleep( stopTime )
            print('============================================')

if __name__ == '__main__':
    try:
        print( 'Running!' )
        main(  )
    except Exception as e:
        print( f'Error: {e}' )