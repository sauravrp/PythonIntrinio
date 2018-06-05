import pandas as pd

from Util import Util

class RetainedEarningsROIC(object):
    util = Util()
    def __init__(self):
       pass

    # questions:
    # how does cash buy back figure into retained earnings?
    def calcIncrementalCapitalROIC(self, incomeStmtData, balanceSheetData, cashFlowData, last_price):
        print "--------------- Incremental Capital ROIC based on Retained Earnings --------------------------------------------"

        # Calculate Retained earnings per share
        retainedearningspershare = balanceSheetData.loc[:, "retainedearnings"] / incomeStmtData.loc[:,
                                                                                 "weightedavedilutedsharesos"]
        retainedearningspershare.name = "retainedearningspershare"

        # Calculate earnings per share
        # calculatedearningspershare = incomeStmtData.loc[:, "netincometocommon"] / incomeStmtData.loc[:,
        #                                                                        "weightedavedilutedsharesos"]
        # calculatedearningspershare.name = "calculated diluted earnings per share"
        # print calculatedearningspershare, incomeStmtData.loc[:, 'dilutedeps']


        retainedData = pd.concat([incomeStmtData.loc[:, 'netincometocommon'],
                                  balanceSheetData.loc[:, 'retainedearnings'],
                                  incomeStmtData.loc[:, 'dilutedeps'],
                                  incomeStmtData.loc[:, 'weightedavedilutedsharesos'],
                                  retainedearningspershare,
                                  incomeStmtData["cashdividendspershare"],
                                  cashFlowData["paymentofdividends"],
                                  cashFlowData['repurchaseofcommonequity']], axis=1)

        retainedData = self.util.dropNaInAllColumns(retainedData)

        print "Year           Net Income (Common)           Retained Earnings      Dividends                     StockBuyBack"
        for index, row in retainedData.iterrows():
            print "{}         ${:20,.2f}      ${:20,.2f}      ${:20,.2f}      ${:20,.2f}".format(index,
                                                                                                 row[
                                                                                                     'netincometocommon'],
                                                                                                 row[
                                                                                                     'retainedearnings'],
                                                                                                 abs(row[
                                                                                                         'paymentofdividends']),
                                                                                                 abs(row[
                                                                                                         'repurchaseofcommonequity']))

        print "\nOver {} years,  Total Net Income = ${:5,.2f}, Total Dividend = ${:5,.2f}, Total Stock BuyBack = ${:5,.2f} \n".format(
            len(retainedData.index),
            retainedData['netincometocommon'].sum(),
            abs(retainedData['paymentofdividends'].sum()),
            abs(retainedData['repurchaseofcommonequity'].sum()))

        diffRE = self.util.calculateDelta(retainedData['retainedearnings'])

        diffIncome = self.util.calculateDelta(retainedData['netincometocommon'])

        diffEPS = self.util.calculateDelta(retainedData['dilutedeps'])

        diffREpershare = self.util.calculateDelta(retainedData['retainedearningspershare'])

        incrementCapitalROIC = (diffIncome / diffRE)

        reinvestmentRate = (diffRE / retainedData['netincometocommon'].sum())

        print "Capital Investments (Retained earnings) grew by ${:0,.2f} and net income grew by ${:0,.2f}".format(diffRE, diffIncome)
        print "Return on Incremental Capital Investments (Net Income) is %.2f%%" % (incrementCapitalROIC * 100)

        # Reinvestment Rate = Difference in Retained Earnings/Total Earnings
        print "Reinvestment rate is {:0,.2f}%".format(reinvestmentRate * 100)
        # value compounding rate of the company
        print "Value Compounding rate of the company is {:0,.2f}%".format(reinvestmentRate * incrementCapitalROIC * 100)

        print "\nRetained earnings per share grew by ${:0,.2f}".format(diffREpershare)
        print "Diluted earnings per share grew by ${:0,.2f} ".format(diffEPS)
        print "Rate of return on retained earnings per share is %.2f%%\n" % (
                float(diffEPS / diffREpershare) * 100)
        print "------------------------------------------------------------------------------\n"
