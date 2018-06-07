
import pandas as pd
import intrinio
import sys

from Globals import TICKER, TEN_YEAR_TREASURY, DISCOUNT_RATE, STANDARD_PERIOD_PV
from PlotData import PlotData
from LiveData import LiveData
from Util import Util
from RetainedEarningsROIC import RetainedEarningsROIC
from GreenblattROIC import GreenblattROIC
from DividendsBuyBacks import DividendsBuyBacks
from SharePrice import SharePrice
from IntrinsicValueCalc import IntrinsicValueCalc


#configurations
intrinio.client.username = 'f51ed99033fc52e3f1743b39c8d43ca6'
intrinio.client.password = '3627e1bb4272a0d014cb8400b587e642'

liveData = LiveData()
plotData = PlotData(4)
retainedEarningsROIC = RetainedEarningsROIC()
greenblattROIC = GreenblattROIC()
dividendsBuyBacks = DividendsBuyBacks()
sharePrice = SharePrice()
intrinsicValueCalc = IntrinsicValueCalc()
util = Util()

def plotGraph(data, col, title, xlabel, ylabel) :
    plotData.plot(data.loc[:, col], title, xlabel, ylabel)

print "------------------- Analysis of {} ---------------------".format(TICKER)

data = liveData.getData(TICKER)
incomeStmtData = data["income_statement"]
balanceSheetData = data["balance_sheet"]
cashFlowData = data["cash_flow_statement"]
calculationsData = data["calculations"]
yearlyPrices = data["yearlyprices"]

yearlyPrices = sharePrice.adjustStockSplits(yearlyPrices)


# clean up data
# if col doesn't exits, fill with 0;0
util.checkAndFillColumn(incomeStmtData, 'cashdividendspershare', 0.0)
util.checkAndFillColumn(cashFlowData, 'paymentofdividends', 0.0)

# ok with 0's here
incomeStmtData.loc[:, 'cashdividendspershare'] = incomeStmtData.loc[:, 'cashdividendspershare'].fillna(0)
cashFlowData.loc[:, 'paymentofdividends'] = cashFlowData.loc[:, 'paymentofdividends'].fillna(0)
cashFlowData.loc[:, 'repurchaseofcommonequity'] = cashFlowData.loc[:, 'repurchaseofcommonequity'].fillna(0)


# ROIC calculations
if 'nwc' in calculationsData.columns:
    greenblattROIC.calculateGreenblattROIC(calculationsData, incomeStmtData, balanceSheetData)
retainedEarningsROIC.calcIncrementalCapitalROIC(incomeStmtData, balanceSheetData, cashFlowData)
# dividend calculations
dividendsBuyBacks.calcDividendBuyBacks(incomeStmtData, balanceSheetData, cashFlowData)


#
# Prioriy of growth rates:
# ROIC (most important)
# 1. Equity growth
# 2. EPS growth
# 3. Sales (or gross profit) growth
# 4. Cash flow growth

# Equity Growth
util.pct_change_stats("Book Value", balanceSheetData.loc[:, 'totalcommonequity'])
util.pct_change_stats("Book Value Per Share", calculationsData.loc[:, 'bookvaluepershare'])

# EPS growth
util.pct_change_stats("Net Income Available to common",  incomeStmtData.loc[:, 'netincometocommon'])
util.pct_change_stats("Diluted EPS", incomeStmtData.loc[:,'dilutedeps'])

# Sales Growth
util.pct_change_stats("Total Revenue", incomeStmtData.loc[:, 'totalrevenue'])

# Cash Flow Growth
util.pct_change_stats("Free Cash Flow", calculationsData.loc[:, 'freecashflow'])

util.average_stats("ROE", calculationsData.loc[:, "roe"] * 100)
util.average_stats("ROA", calculationsData.loc[:, "roa"] * 100)
util.average_stats("P/E ratio", calculationsData.loc[:, 'pricetoearnings'])
util.average_stats("P/B ratio", calculationsData.loc[:, 'pricetobook'])

# Share price Count
util.pct_change_stats("Weighted Average Diluted Share Outstanding", incomeStmtData.loc[:, 'weightedavedilutedsharesos'])
# Share Price stats
util.pct_change_stats("Share Price", yearlyPrices.loc[:, 'adj_split_close'])

# Share Price with dividends
combinedData = pd.concat([yearlyPrices['adj_split_close'],
                          incomeStmtData.loc[:, 'cashdividendspershare']],
                         axis=1)
combinedData.loc[:, 'cashdividendpershare'] = combinedData.loc[:,'cashdividendspershare'].fillna(0)
combinedData = util.dropNaInAllColumns(combinedData)
util.pct_change_stats("Share Price with dividend", combinedData.loc[:, 'adj_split_close'] + combinedData.loc[:, 'cashdividendspershare'])



last_eps = incomeStmtData.loc[:, "dilutedeps"].iloc[::-1].head(1)
last_bvps = calculationsData.loc[:, "bookvaluepershare"].iloc[::-1].head(1)
last_price = yearlyPrices.loc[:, 'adj_split_close'].tail(1)
print "last_price: $%.2f" % (last_price.iloc[0])
print "last_eps: $%.2f" % (last_eps.iloc[0])
print "last book value per share: $%.2f" % (last_bvps.iloc[0])

print "\nLong term treasury is %s%%" % (str(TEN_YEAR_TREASURY))
print "Paying $%.2f a share results in %.2f%% return" % (last_price.iloc[0], float(last_eps.iloc[0]/last_price.iloc[0]) * 100)


intrinsicValueCalc.calcValueBasedOnEPS(last_eps.iloc[0])
# intrinsicValueCalc.calcValueBasedOnBookValueGrowth(last_price.iloc[0], last_bvps.iloc[0], combinedData.loc[:, 'cashdividendpershare'])


#plotGraph(incomeStatementData, ["dilutedeps", "basiceps"], "EPS", "$", "Years")

# plot annual growth rate of earnings per share
#plotData.plot(calculationsData.loc[:, ['epsgrowth']],  "EPS Growth", "%", "Years")

# plot book value per share
#plotGraph(calculationsData, ['bookvaluepershare'], "Book Value Per Share", "$", "Years")

#plot return on equity
#plotData.plot(calculationsData.loc[:, ['roe']] * 100,  "Return on Equity", "%", "Years")
#plotData.show()

sys.exit()




# things to do
# model equity growth per roe (buffetology)
# refer to pat dorsey book for capex, freecash flow items, (general scan)
# calculate fcf, owner carnings
# maintcapex, growth in capex (bruce greenwald)
# capex % of sales (refer bruce greenwald)
# how about price to book ratios? -> done

# references
# intrinio docs
# data feed tags http://docs.intrinio.com/tags/intrinio-public#industrial
# http://docs.intrinio.com/?javascript--api#company-news
# quantopian dataframe and series tutorial https://www.quantopian.com/lectures/introduction-to-pandas
# running the five largest firms with no equity capital


