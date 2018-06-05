from Util import Util
import pandas as pd

class GreenblattROIC(object):
    util = Util()

    def __init__(self):
        pass

    def calculateGreenblattROIC(self, calculationsData, incomeStatementData, balanceSheetData):
        print "------------------------ ROIC based on Greenblatt --------------------------------------------"

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
                                                                                 row['ebit'],
                                                                                 row['netincometocommon'],
                                                                                 row['investedcapital'],
                                                                                 row['roic'])

        print "Average ROIC: %.2f%%" % (combinedData.loc[:, "roic"].mean())

        income_growth_rate = self.util.CAGR(combinedData.loc[:, 'netincometocommon'].iloc[0],
                                            combinedData.loc[:, "netincometocommon"].iloc[::-1].iloc[0],
                                            len(combinedData.loc[:, 'netincometocommon'].index))

        print "Income Growth Rate is {:0,.2f}%".format(income_growth_rate * 100)

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
