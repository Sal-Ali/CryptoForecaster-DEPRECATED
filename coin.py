import requests
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import json
import time
import gspread
from rpy2.robjects.packages import importr
import pandas as pd
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
from Stack import Stack

#unused but previously important import statements

import rpy2.robjects as robjects
from statistics import mean , median
from statistics import mean , median
import numpy as np
import rpy2 as r

#########################################################################################################################
class coin:
    count = 0
    #basic class declaration for use in google spreadsheets
    def __init__(self, CoinName):
        self.CoinName = CoinName
        self.api_request = requests.get("https://api.coinmarketcap.com/v1/ticker/" + self.CoinName)
        self.api_json = json.loads(self.api_request.text)
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheetname = self.client.open('CryptoBusiness').worksheet(self.CoinName)
        self.now = datetime.datetime.now()
        self.timestamp = str(self.now.month) + '-' + str(self.now.day) + ' ' + str(self.now.hour) + ':' + str(self.now.minute)

#returns a list to get updated to a spreadsheet
    def basicInfo(self):
        time.sleep(7.2)
        self.count = self.count + 1
        rowToInsert = [self.timestamp, self.api_json[0]['price_usd']]
        self.sheetname.insert_row(rowToInsert)

        #r shell code done here purely for testing purposes, any lines beyond in this definition can be completely ignored
        utils = importr('utils')
        # install all packages

#calculates the initial metrics
    def advanceOptiuon(self):

        data1 = self.sheetname.col_values(2)
        data2 = self.sheetname.col_values(2)
        for x in data1:
            if x == 0 or  x == None:
                data1.__delitem__(x)
        dataframe1 = pd.DataFrame(data1)
        dataframe2 = pd.DataFrame(data2[::99])
#ensures objects flow in and out of R and Python without catastrophic failures
        pandas2ri.activate()
#the final R code used, prior code can't be loaded with this functionality
        string = """statcalc <- function(x, size = 100){
                    library(TTR)
                    library(stats)
                    xa <- ts(x)
                    arima <- arima(xa, c(0,0,0))
                    rsi <- RSI(xa, size - 1)[size]
                    list <- c(arima$coef, rsi)
                    return(as.matrix(list))
                    }
                    """
        statcalc = SignatureTranslatedAnonymousPackage(string, "statcalc")
        newlist = statcalc.statcalc(dataframe1, len(data1))
        otherlist = statcalc.statcalc(dataframe2, len(dataframe2))
        winsandlosses = float(data1[99]) - float(data1[0])
        #the basic version of the algorithm, subject to change at a later date
        rsi = float(otherlist[1])
        if rsi > .65:
            rsi = 1
        if rsi < .35:
            rsi = 0
        gains = float(data1[99])
        arima = otherlist[0]
        arimaOverall = newlist[0]
        if gains - float(arima) > 0:
            topthird = 0
        else:topthird = 1
        if gains - float(arimaOverall) > 0:
            bottomthird = 0
        else:bottomthird = 1
        midthird = float(newlist[1])
        arimaIndex = ((2 * bottomthird * .33 + midthird * .33 + 2 * topthird * .33) * .2)

        if (rsi/2 + arimaIndex /2) > .5:
            rowtoinsert = ['', '', 'period gain: ' , str(winsandlosses), 'it is recommended to: buy', 1 , 'rsi index is: ' + str(rsi), 'arima index is: ' + str(arimaIndex)]
        else:rowtoinsert = ['', '', 'period gain: ' , str(winsandlosses), 'it is recommended to: sell', 0 , 'rsi index is: ' + str(rsi), 'arima index is: ' + str(arimaIndex)]
        self.sheetname.insert_row(rowtoinsert)

#counts up and returns how well the algorithm performed
    def tally(self):
        counted = 0
        result = 0
        total = 0
        s = Stack()
        j = Stack()
        values = self.sheetname.col_values(4)
        reccs = self.sheetname.col_values(6)
        for x in values:
            s.push(x)
            j.push(x)
            if counted == 0:
                s.pop()
                j.pop()
                counted = 1

        reccs.reverse()
        for n in reccs:
            n = int(n)
            if s.isEmpty():
                break
            if n == 0:
                s.pop()

        while s.isEmpty() == False:
            result = result + float(s.peek())
            s.pop()

        while j.isEmpty() == False:
            total = total + float(j.peek())
            j.pop()

        string = 'Without the algorithm the G/L is: ' + str(total) + " " + 'Compared to with the algorithm at :' + str(result)
        return string































