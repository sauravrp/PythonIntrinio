from Util import Util
import pandas as pd

class GreenblattROIC(object):
    util = Util()

    def __init__(self):
        pass

    def calculateGreenblattROIC(self, calculationsData, incomeStatementData, balanceSheetData):
        print "\n------------------------ ROIC based on Greenblatt --------------------------------------------"
        print "Invested Capital = NWC + NETPPE - Cash balance"

        investedCapital = calculationsData.loc[:, 'nwc'] + balanceSheetData.loc[:, 'netppe'] + (
                    balanceSheetData.loc[:, 'cashandequivalents'] - (0.01 * incomeStatementData["totalrevenue"]))
        investedCapital.name = "investedcapital"

        roic = calculationsData.loc[:, 'ebit'] / investedCapital * 100
        roic.name = "roic"


        combinedData = pd.concat([calculationsData.loc[:, 'ebit'],
                                  investedCapital,
                                  incomeStatementData.loc[:, 'netincometocommon'],
                                  roic], axis=1)

        combinedData = self.util.dropNaInAllColumns(combinedData)


        print "Year                 EBIT                    NetIncome             InvestedCapital             ROIC"
        for index, row in combinedData.iterrows():
            print "{}         ${:20,.2f}      ${:20,.2f}    ${:20,.2f}      {:5,.2f}%".format(index,
                                                                                 row.loc['ebit'],
                                                                                 row.loc['netincometocommon'],
                                                                                 row.loc['investedcapital'],
                                                                                 row.loc['roic'])

        print "Stats on ROIC"
        self.util.average_multiyear_stats(combinedData.loc[:, "roic"])

        diffCapitalInvested = self.util.calculateDelta(combinedData['investedcapital'])
        diffEBIT = self.util.calculateDelta(calculationsData.loc[:, 'ebit'])
        print "\nTotal EBIT {} years was ${:0,.2f}".format(len(combinedData.loc[:, 'ebit'].index),
                                                                    combinedData.loc[:, 'ebit'].sum())
        print "Capital Invested grew by ${:0,.2f}, EBIT grew by ${:0,.2f}".format(diffCapitalInvested, diffEBIT)
        print "Return on Incremental Capital Investments (EBIT) is %.2f%%" % (diffEBIT/diffCapitalInvested * 100)

        diffIncome = self.util.calculateDelta(combinedData.loc[:, 'netincometocommon'])
        incrementCapitalROIC = diffIncome / diffCapitalInvested
        print "\nTotal Net Income over {} years was ${:0,.2f}".format(len(combinedData.loc[:, 'ebit'].index),
                                                                    combinedData.loc[:, 'netincometocommon'].sum())
        print "Capital Invested grew by ${:0,.2f}, Net Income grew by ${:0,.2f}".format(diffCapitalInvested, diffIncome)
        print "Return on Incremental Capital Investments (Net Income) is %.2f%%" % (incrementCapitalROIC * 100)

        reinvestmentRate = (diffCapitalInvested / combinedData['netincometocommon'].sum())

        # Reinvestment Rate = Difference in Retained Earnings/Total Earnings
        print "Reinvestment rate is {:0,.2f}%".format(reinvestmentRate * 100)
        # value compounding rate of the company
        print "Value Compounding rate of the company is {:0,.2f}%".format(reinvestmentRate * incrementCapitalROIC * 100)

        print "---------------------------------------------------------------------------------------\n"

    # https://amigobulls.com/articles/simplifying-return-on-invested-capital
    # Invested Capital = Short-term debt + Long term debt + Shareholders equity - Cash balance
    def calculateGreenblattROIC2(self, calculationsData, incomeStatementData, balanceSheetData):
        print "\n------------------------ ROIC based on Greenblatt adjusted --------------------------------------------"
        #print "Invested Capital = Short-term debt + Long term debt + Shareholders equity - Cash balance"
        # investedCapital = balanceSheetData.loc[:, 'shorttermdebt'] \
        #                   + balanceSheetData.loc[:, 'longtermdebt'] \
        #                   + balanceSheetData.loc[:, 'commonequity']\
        #                   + (balanceSheetData.loc[:, 'cashandequivalents'] - (0.01 * incomeStatementData["totalrevenue"]))

        print "Invested Capital = Total Assets"

        investedCapital = balanceSheetData.loc[:, 'totalassets']
        investedCapital.name = "investedcapital"

        roic = calculationsData.loc[:, 'ebit'] / investedCapital * 100
        roic.name = "roic"


        combinedData = pd.concat([calculationsData.loc[:, 'ebit'],
                                  investedCapital,
                                  incomeStatementData.loc[:, 'netincometocommon'],
                                  roic], axis=1)

        combinedData = self.util.dropNaInAllColumns(combinedData)


        print "Year                 EBIT                    NetIncome             InvestedCapital             ROIC"
        for index, row in combinedData.iterrows():
            print "{}         ${:20,.2f}      ${:20,.2f}    ${:20,.2f}      {:5,.2f}%".format(index,
                                                                                 row.loc['ebit'],
                                                                                 row.loc['netincometocommon'],
                                                                                 row.loc['investedcapital'],
                                                                                 row.loc['roic'])

        print "Stats on ROIC"
        self.util.average_multiyear_stats(combinedData.loc[:, "roic"])

        diffCapitalInvested = self.util.calculateDelta(combinedData['investedcapital'])
        diffEBIT = self.util.calculateDelta(calculationsData.loc[:, 'ebit'])
        print "\nTotal EBIT {} years was ${:0,.2f}".format(len(combinedData.loc[:, 'ebit'].index),
                                                                    combinedData.loc[:, 'ebit'].sum())
        print "Capital Invested grew by ${:0,.2f}, EBIT grew by ${:0,.2f}".format(diffCapitalInvested, diffEBIT)
        print "Return on Incremental Capital Investments (EBIT) is %.2f%%" % (diffEBIT/diffCapitalInvested * 100)

        diffIncome = self.util.calculateDelta(combinedData.loc[:, 'netincometocommon'])
        incrementCapitalROIC = diffIncome / diffCapitalInvested
        print "\nTotal Net Income over {} years was ${:0,.2f}".format(len(combinedData.loc[:, 'ebit'].index),
                                                                    combinedData.loc[:, 'netincometocommon'].sum())
        print "Capital Invested grew by ${:0,.2f}, Net Income grew by ${:0,.2f}".format(diffCapitalInvested, diffIncome)
        print "Return on Incremental Capital Investments (Net Income) is %.2f%%" % (incrementCapitalROIC * 100)

        reinvestmentRate = (diffCapitalInvested / combinedData['netincometocommon'].sum())

        # Reinvestment Rate = Difference in Retained Earnings/Total Earnings
        print "Reinvestment rate is {:0,.2f}%".format(reinvestmentRate * 100)
        # value compounding rate of the company
        print "Value Compounding rate of the company is {:0,.2f}%".format(reinvestmentRate * incrementCapitalROIC * 100)

        print "---------------------------------------------------------------------------------------\n"
