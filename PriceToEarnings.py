import pandas as pd
from Globals import DEBUG
from Util import Util

class PriceToEarnings(object):
    def __init__(self):
        pass

    def calcPE_Ratios(self, calculatedData):
        # combine this data
      print "------------ Price To Earnings-------------------"
      print calculatedData.loc[:, 'pricetoearnings']
      print "Averge price to earnigns ratio is {:,.2f}".format(calculatedData.loc[:,'pricetoearnings'].mean())

