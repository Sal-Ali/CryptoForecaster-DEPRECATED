import requests
from oauth2client.service_account import ServiceAccountCredentials
import rpy2 as R
import datetime
import json
import time
import gspread
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects


class coin:

    def __init__(self, CoinName, apiNumber, sheetName):
        self.CoinName = CoinName
        self.apiNumber = apiNumber
        self.sheetName = sheetName

#returns a list to get updated to a spreadsheet
    def basicInfo(self):
        delay = 60
        rowprevious = []
        api_request = requests.get("https://api.coinmarketcap.com/v1/ticker/" + self.CoinName)
        api_json = json.loads(api_request.text)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        sheetname = client.open('CryptoBusiness').sheet1
        now = datetime.datetime.now()
        timestamp = str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute)
        rowToInsert = [api_json[0]['name'], api_json[0]['price_usd'], timestamp, 'G/L']
        rowprevious = rowToInsert
        print(rowToInsert)
        utils = importr('utils')
        # install all packages
        import rpy2.robjects as robjects
        ts = robjects.r('ts')
       # utils.install_packages('forecast')
        forecast = importr('stats')
        data = ts(sheetname.col_values(2))
        forecast.arima(data)
        #print(data)






#returns the RSI
#self training constant
#ARIMA model
#function to make buy/sell recc per 6h




















