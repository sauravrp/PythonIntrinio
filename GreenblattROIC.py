from Util import Util
import pandas as pd

class GreenblattROIC(object):
    util = Util()

    def __init__(self):
        pass

    def calculateGreenblattROIC(self, calculationsData, incomeStatementData, balanceSheetData):
        print "\n------------------------ ROIC based on Greenblatt --------------------------------------------"

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

        self.util.average_multiyear_stats(combinedData.loc[:, "roic"])

        diffCapitalInvested = self.util.calculateDelta(combinedData['investedcapital'])
        diffEBIT = self.util.calculateDelta(calculationsData.loc[:, 'ebit'])
        print "\nCapital Invested grew by ${:0,.2f}, EBIT grew by ${:0,.2f}".format(diffCapitalInvested, diffEBIT)
        print "Return on Incremental Capital Investments (EBIT) is %.2f%%" % (diffEBIT/diffCapitalInvested * 100)

        diffIncome = self.util.calculateDelta(combinedData.loc[:, 'netincometocommon'])
        incrementCapitalROIC = diffIncome / diffCapitalInvested
        print "\nCapital Invested grew by ${:0,.2f}, Net Income grew by ${:0,.2f}".format(diffCapitalInvested, diffIncome)
        print "Return on Incremental Capital Investments (Net Income) is %.2f%%" % (incrementCapitalROIC * 100)

        reinvestmentRate = (diffCapitalInvested / combinedData['netincometocommon'].sum())

        # Reinvestment Rate = Difference in Retained Earnings/Total Earnings
        print "Reinvestment rate is {:0,.2f}%".format(reinvestmentRate * 100)
        # value compounding rate of the company
        print "Value Compounding rate of the company is {:0,.2f}%".format(reinvestmentRate * incrementCapitalROIC * 100)

        print "---------------------------------------------------------------------------------------\n"
