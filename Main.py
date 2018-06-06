
import pandas as pd
import intrinio

from Globals import TICKER, TEN_YEAR_TREASURY
from PlotData import PlotData
from LiveData import LiveData
from Util import Util
from RetainedEarningsROIC import RetainedEarningsROIC
from GreenblattROIC import GreenblattROIC
from DividendsBuyBacks import DividendsBuyBacks
from SharePrice import SharePrice
from PriceToEarnings import PriceToEarnings

#configurations
intrinio.client.username = 'f51ed99033fc52e3f1743b39c8d43ca6'
intrinio.client.password = '3627e1bb4272a0d014cb8400b587e642'

liveData = LiveData()
plotData = PlotData(4)
retainedEarningsROIC = RetainedEarningsROIC()
greenblattROIC = GreenblattROIC()
dividendsBuyBacks = DividendsBuyBacks()
sharePrice = SharePrice()
priceToEarnings = PriceToEarnings()
util = Util()

def dump(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
        print(df)

def plotGraph(data, col, title, xlabel, ylabel) :
    plotData.plot(data.loc[:, col], title, xlabel, ylabel)


def calcROE(calculationsData):
    print "--------------- ROE data -----------------------------------------------------"
    print "Year        ROE"
    for index, row in calculationsData.iterrows():
        print "%s        %.2f%%" % (index, row['roe'] * 100)

    print "Average ROE: %.2f%%" % (calculationsData.loc[:, "roe"].mean() * 100)
    print "------------------------------------------------------------------------------\n"

def calcEPS(incomeStmtData, calculationsData) :
    print "--------------- EPS data -------------------------------------------------"
    epsData = pd.concat([incomeStmtData.loc[:, 'basiceps'],
                         incomeStmtData.loc[:, 'dilutedeps'],
                         calculationsData.loc[:, 'epsgrowth'] * 100], axis=1)

    print "Year      basiceps      dilutedeps        epsgrowth"
    for index, row in epsData.iterrows():
        print "%s        $%4.2f         $%4.2f             %4.2f%%" % (
        index, row['basiceps'], row['dilutedeps'], row['epsgrowth'])


    eps_growth_rate = util.CAGR(incomeStmtData.loc[:, 'dilutedeps'].iloc[0],
              incomeStmtData.loc[:, "dilutedeps"].iloc[::-1].iloc[0],
              len(incomeStmtData.loc[:, 'dilutedeps'].index))

    print "EPS Growth Rate is {:0,.2f}%".format(eps_growth_rate*100)

    print "--------------------------------------------------------------------------"

def calcBVPS(incomeStmtData, calculationsData) :
    # Calculate Retained earnings per share
    bookvalue = calculationsData.loc[:, "bookvaluepershare"] * incomeStmtData.loc[:,
                                                                             "weightedavedilutedsharesos"]
    bookvalue.name = "bookvalue"
    cumulativeData = pd.concat([calculationsData.loc[:, 'bookvaluepershare'],
                                bookvalue,
                                incomeStmtData.loc[:, "weightedavedilutedsharesos"]], axis=1)
    cumulativeData = util.dropNaRows(cumulativeData, 'bookvalue')


    print "--------------- Book Value --------------------------------------------"
    print "Year      Book Value/Share      Book Value                         Num Shares"
    for index, row in cumulativeData.iterrows():
        print "{}       ${:0,.2f}             ${:20,.2f}            {:20,.2f}".format(index,
                                                                                       row['bookvaluepershare'],
                                                                                       row['bookvalue'],
                                                                                       row['weightedavedilutedsharesos'])

    bvps_growth_rate = util.CAGR(cumulativeData.loc[:, 'bookvaluepershare'].iloc[0],
                                 cumulativeData.loc[:, "bookvaluepershare"].iloc[::-1].iloc[0],
                                    len(cumulativeData.loc[:, 'bookvaluepershare'].index))

    bv_growth_rate = util.CAGR(cumulativeData.loc[:, 'bookvalue'].iloc[0],
                               cumulativeData.loc[:, "bookvalue"].iloc[::-1].iloc[0],
                                 len(cumulativeData.loc[:, 'bookvalue'].index))

    util.pct_change_stats("Book Value", cumulativeData, 'bookvalue')

    print "Book Value Per Share Growth Rate is {:0,.2f}%".format(bvps_growth_rate * 100)
    print "Book Value Growth Rate is {:0,.2f}%".format(bv_growth_rate * 100)

    print "------------------------------------------------------------------------------\n"




data = liveData.getData(TICKER)
incomeStmtData = data["income_statement"]
balanceSheetData = data["balance_sheet"]
cashFlowData = data["cash_flow_statement"]
calculationsData = data["calculations"]
yearlyPrices = data["yearlyprices"]

yearlyPrices = sharePrice.adjustStockSplits(yearlyPrices)

#dump(incomeStmtData)
#print incomeStmtData.keys()

# clean up data
# if col doesn't exits, fill with 0;0
util.checkAndFillColumn(incomeStmtData, 'cashdividendspershare', 0.0)
util.checkAndFillColumn(cashFlowData, 'paymentofdividends', 0.0)

# ok with 0's here
incomeStmtData.loc[:, 'cashdividendspershare'] = incomeStmtData.loc[:, 'cashdividendspershare'].fillna(0)
cashFlowData.loc[:, 'paymentofdividends'] = cashFlowData.loc[:, 'paymentofdividends'].fillna(0)
cashFlowData.loc[:, 'repurchaseofcommonequity'] = cashFlowData.loc[:, 'repurchaseofcommonequity'].fillna(0)

calcROE(calculationsData)
calcEPS(incomeStmtData, calculationsData)
calcBVPS(incomeStmtData, calculationsData)

if 'nwc' in calculationsData.columns:
    greenblattROIC.calculateGreenblattROIC(calculationsData, incomeStmtData, balanceSheetData)

retainedEarningsROIC.calcIncrementalCapitalROIC(incomeStmtData, balanceSheetData, cashFlowData)

dividendsBuyBacks.calcDividendBuyBacks(incomeStmtData, balanceSheetData, cashFlowData)

last_eps = incomeStmtData.loc[:, "dilutedeps"].iloc[::-1].head(1)
last_bvps = calculationsData.loc[:, "bookvaluepershare"].iloc[::-1].head(1)

sharePrice.calcSharePriceGrowth(yearlyPrices, incomeStmtData)

last_price = yearlyPrices.loc[:, 'adj_split_close'].head(1)
print "last_price: $%.2f" % (last_price.iloc[0])
print "last_eps: $%.2f" % (last_eps.iloc[0])
print "last book value per share: $%.2f" % (last_bvps.iloc[0])

print "Long term treasury is %s%%" % (str(TEN_YEAR_TREASURY))
print "Paying $%.2f a share results in %.2f%% return" % (last_price.iloc[0], float(last_eps.iloc[0]/last_price.iloc[0]) * 100)

priceToEarnings.calcPE_Ratios(calculationsData)


#plotGraph(incomeStatementData, ["dilutedeps", "basiceps"], "EPS", "$", "Years")

# plot annual growth rate of earnings per share
#plotData.plot(calculationsData.loc[:, ['epsgrowth']],  "EPS Growth", "%", "Years")

# plot book value per share
#plotGraph(calculationsData, ['bookvaluepershare'], "Book Value Per Share", "$", "Years")

#plot return on equity
#plotData.plot(calculationsData.loc[:, ['roe']] * 100,  "Return on Equity", "%", "Years")
#plotData.show()



# things to do
# compounded rate of price








