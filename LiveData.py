import intrinio
import os
from CacheData import CacheData
from Globals import PRICES_PULL_START_DATE

class LiveData(object) :

    cacheData = CacheData()

    def __init__(self):
       pass

    def getData(self, ticker):
        data = {}

        dataTag = "yearlyprices"
        if not os.path.exists(self.cacheData.filename(ticker, dataTag)):
            print "getting %s data for %s" % (dataTag, ticker)
            data[dataTag] = intrinio.prices(ticker, start_date=PRICES_PULL_START_DATE, frequency="yearly")
            self.cacheData.save(data[dataTag], ticker, dataTag)
        else:
            data[dataTag] = self.cacheData.open(ticker, dataTag)

        dataTag = "income_statement"
        if not os.path.exists(self.cacheData.filename(ticker, dataTag)):
            print "getting %s data for %s" % (dataTag, ticker)
            data[dataTag] = intrinio.financials(ticker, "FY", dataTag)
            self.cacheData.save( data[dataTag], ticker, dataTag)
        else:
            data[dataTag] = self.cacheData.open(ticker, dataTag)

        dataTag = "balance_sheet"
        if not os.path.exists(self.cacheData.filename(ticker, dataTag)):
            print "getting %s data for %s" % (dataTag, ticker)
            data[dataTag] = intrinio.financials(ticker, "FY", dataTag)
            self.cacheData.save( data[dataTag], ticker, dataTag)
        else:
            data[dataTag] = self.cacheData.open(ticker, dataTag)

        dataTag = "cash_flow_statement"
        if not os.path.exists(self.cacheData.filename(ticker, dataTag)):
            print "getting %s data for %s" % (dataTag, ticker)
            data[dataTag] = intrinio.financials(ticker, "FY", dataTag)
            self.cacheData.save(data[dataTag], ticker, dataTag)
        else:
            data[dataTag] = self.cacheData.open(ticker, dataTag)

        dataTag = "calculations"
        if not os.path.exists(self.cacheData.filename(ticker, dataTag)):
            print "getting %s data for %s" % (dataTag, ticker)
            data[dataTag] = intrinio.financials(ticker, "FY", dataTag)
            self.cacheData.save( data[dataTag], ticker, dataTag)
        else:
            data[dataTag] = self.cacheData.open(ticker, dataTag)

        return data
