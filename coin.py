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

    #basic class declaration for use in google spreadsheets
    #this is an excessive amount of variables, mostly created to test and go with ease
    #there is some API error that people online have not been able to fix, so I am attempting to deal with it
    def __init__(self, CoinName):
        self.CoinName = CoinName
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)
        self.client = gspread.authorize(self.creds)
        self.sheetname = self.client.open('CryptoBusiness').worksheet(self.CoinName)
        self.count = 0

#returns a list to get updated to a spreadsheet
    def main(self):
        time.sleep(7.2)
        self.count = self.count + 1


        self.client = gspread.authorize(self.creds)
        self.client.login()
        api_request = requests.get("https://api.coinmarketcap.com/v1/ticker/" + self.CoinName)
        api_json = json.loads(api_request.text)
        now = datetime.datetime.now()
        timestamp = str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute) + str(now.second)


        rowToInsert = [timestamp, api_json[0]['price_usd']]
        self.sheetname.insert_row(rowToInsert)
        self.count = self.count + 1

        #r shell code done here purely for testing purposes, any lines beyond in this definition can be completely ignored
        # utils = importr('utils')
        # install all packages


#calculates the initial metrics
    def advanceOptiuon(self):
        #every period calculates the appropriate statistic and prints
        #to the console and dataset
        data1 = self.sheetname.col_values(2)
        data1[:] = [item for item in data1 if item != '']
        dataframe1 = pd.DataFrame(data1)
        #print(dataframe1)
        dataframe2 = pd.DataFrame(data1[::99])
#ensures objects flow in and out of R and Python without catastrophic failures
        pandas2ri.activate()
#the final R code used, prior code can't be loaded with this functionality
        string = """statcalc <- function(x, size = 100){
                    x <- na.omit(x)
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
        newlist = statcalc.statcalc(dataframe1, len(dataframe1))
        otherlist = statcalc.statcalc(dataframe2, len(dataframe2))
        winsandlosses = float(data1[99]) - float(data1[0])
        #the basic version of the algorithm, subject to change at a later date
        rsi = float(otherlist[1])
        if rsi > 80:
            rsi = 0
        if rsi < 35:
            rsi = 1
        gains = float(data1[99])
        arima = otherlist[0]
        arimaOverall = newlist[0]
        if gains - float(arima) > 0:
            topthird = 0
        else:topthird = 1
        if gains - float(arimaOverall) > 0:
            bottomthird = 0
        else:bottomthird = 1
        midthird = (newlist[1]) / 100
        arimaIndex = (float(2/3 * bottomthird) + float(1/3 * midthird) + float(2/3 *topthird)) * 3/5


        if (rsi/2 + arimaIndex /2) > .5:
            rowtoinsert = ['', '', 'period gain: ' , str(winsandlosses), 'it is recommended to: buy', 1 , 'rsi index is: ' + str(rsi), 'arima index is: ' + str(arimaIndex)]
        else:rowtoinsert = ['', '', 'period gain: ' , str(winsandlosses), 'it is recommended to: sell', 0 , 'rsi index is: ' + str(rsi), 'arima index is: ' + str(arimaIndex)]
        self.sheetname.insert_row(rowtoinsert)

#counts up and returns how well the algorithm performed
    def tally(self):
        #performs the same tally done in R, but in real time
        #see the Rtally code for a clearer expanation
        aggressiveresult = 0
        result = 0
        total = 0
        s = Stack()
        j = Stack()
        values = self.sheetname.col_values(4)
        reccs = self.sheetname.col_values(6)
        alpha = values
        beta = reccs
        values[:] = [item for item in values if item != '']
        reccs[:] = [item for item in reccs if item != '']

        beta.pop()
        alpha.reverse()
        beta.reverse()
        alpha.pop()

        for x in alpha:
            s.push(x)
        for n in beta:
            j.push(n)
        while(not s.isEmpty()):
            if not j.isEmpty():
                total = total + float(s.peek())
                if int(j.peek()) == 0:
                    aggressiveresult = aggressiveresult + 2* float(s.peek())
                if int(j.peek()) == 1:
                    result = result + float(s.peek())
                    aggressiveresult = aggressiveresult - float(s.peek())
                j.pop()
            s.pop()
        string = 'Without the algorithm the G/L is: ' + str(total) + " " + 'Compared to with the algorithm at :' + str(result) + 'Aggressively trading: ' + str(aggressiveresult)
        rowtoinsert = ['','','','','','','','', '', total, result, aggressiveresult]
        self.sheetname.insert_row(rowtoinsert)
        return string



































