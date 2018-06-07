import pandas as pd

from Util import Util


class DividendsBuyBacks(object):
    util = Util()
    def __init__(self):
        pass

        # questions:
        # how does cash buy back figure into retained earnings?

    def calcDividendBuyBacks(self, incomeStmtData, balanceSheetData, cashFlowData):
        print "--------------- Dividend Buybacks --------------------------------------------"

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
                                  incomeStmtData.loc[:, "cashdividendspershare"],
                                  cashFlowData.loc[:, "paymentofdividends"],
                                  cashFlowData.loc[:, 'repurchaseofcommonequity']], axis=1)

        retainedData = self.util.dropNaInAllColumns(retainedData)



        print "\nReturn as percent of income"
        print "Year            Div     StockBuyBack    Total %"
        for index, row in retainedData.iterrows():
            print "{}         {:5,.2f}%     {:5,.2f}%          {:5,.2f}%     ".format(index,
                                                                                      ((abs(row[
                                                                                                'paymentofdividends']) * 100) /
                                                                                       row['netincometocommon']),
                                                                                      (abs(row[
                                                                                               'repurchaseofcommonequity'] * 100)) /
                                                                                      row['netincometocommon'],
                                                                                      (abs(row[
                                                                                               'paymentofdividends'] * 100)) /
                                                                                      row['netincometocommon'] +
                                                                                      (abs(row[
                                                                                               'repurchaseofcommonequity'] * 100)) /
                                                                                      row['netincometocommon'])

        print "\nYear       Dividend per share"
        for index, row in retainedData.iterrows():
            print "{}         ${:0,.2f}".format(index, row['cashdividendspershare'])
        print "Total Dividend payout of ${:0,.2f}".format(retainedData['cashdividendspershare'].sum())
        payoutRatio = retainedData.loc[:,'cashdividendspershare'].sum() / retainedData.loc[:,'dilutedeps'].sum()
        print payoutRatio
        print "Total Dividend payout as percent of earnings is {:0,.2f}%".format(payoutRatio*100)
        print "Total Retained ratio is {:0,.2f}%".format(float(1.0 - payoutRatio) * 100)

        print "------------------------------------------------------------------------------\n"
