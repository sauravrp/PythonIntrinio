import pandas as pd
from Globals import DEBUG, THIS_YEAR
from Util import Util


class SharePrice(object) :
    util = Util()

    def __init__(self):
        pass

    def adjustStockSplits(self, dataFrame):
        split_factor = 1
        adj_split_close = pd.Series(data=dataFrame.loc[:, 'close'], index=dataFrame.index)
        adj_split_close.name = "adj_split_close"
        if DEBUG == True:
            print "Year               Close      Split Ratio   SplitAdjClose       "
        for index, row in dataFrame.iterrows():
            adj_split_close.loc[index] = split_factor * row.loc['close']
            split_factor = split_factor * row['split_ratio']
            if DEBUG == True:
                print "{}         ${:0,.2f}      {:0,.4f}      ${:0,.2f}".format(index, row.loc['close'],
                                                                                 row.loc['split_ratio'],
                                                                                 adj_split_close.loc[index])

        # make custom index only out of year instead of year -- mm -- day
        custom_index = []
        i = 1
        for date in adj_split_close.index[::-1]:
            if (type(date) == pd.Timestamp):
                custom_index.append(date.year)
            else :
                custom_index.append(THIS_YEAR - len(adj_split_close.index) + i)
                i+=1

        # create new series with new year only index
        newYearlySeries = pd.Series(data=adj_split_close.iloc[::-1].values, index=custom_index)
        newYearlySeries.name = "adj_split_close"
         #print newYearlySeries
        return pd.DataFrame(data={newYearlySeries.name : newYearlySeries.values }, index=newYearlySeries.index)

    # def calcSharePriceGrowth(self, yearlyPrices, incomeStmtData):
    #
    #     # combine this data
    #     combinedData = pd.concat([yearlyPrices['adj_split_close'],
    #                               incomeStmtData.loc[:, 'cashdividendspershare']],
    #                                axis=1)
    #     combinedData = self.util.dropNaInAllColumns(combinedData)
    #
    #     # get the latest
    #     first_price = combinedData.loc[:, 'adj_split_close'].head(1)
    #     last_price = combinedData.loc[:, "adj_split_close"].iloc[::-1].head(1)
    #     print combinedData
    #     share_price_growth_rate = self.util.CAGR(first_price.iloc[0],
    #                                             last_price.iloc[0],
    #                                              len(combinedData.loc[:, 'adj_split_close'].index))
    #
    #     totalDividend = combinedData.loc[:, 'cashdividendspershare'].sum()
    #
    #     with_div_share_price_growth_rate = self.util.CAGR(first_price.iloc[0],
    #                                              last_price.iloc[0] + totalDividend,
    #                                              len(combinedData.loc[:, 'adj_split_close'].index))
    #
    #     print "Share Price grew from ${:0,.2f} in {} to ${:0,.2f} in {}".format(first_price.iloc[0],
    #                                                                             first_price.index[0],
    #                                                                             last_price.iloc[0],
    #                                                                             last_price.index[0])
    #     print "Share Price Growth Rate is {:0,.2f}% over {:0,d} years".format(share_price_growth_rate * 100,
    #                                                                           len(combinedData.loc[:, 'adj_split_close'].index))
    #
    #
    #     print "Total Dividend paid out was ${:0,.2f}".format(totalDividend)
    #     print "With Dividend, Share Price return was from ${:0,.2f} in {} to ${:0,.2f} in {}".format(first_price.iloc[0],
    #                                                                         first_price.index[0],
    #                                                                         last_price.iloc[0] + combinedData.loc[:, 'cashdividendspershare'].sum(),
    #                                                                         last_price.index[0])
    #
    #     print "With Dividend, Share Price Growth Rate is {:0,.2f}% over {:0,d} years".format(with_div_share_price_growth_rate * 100,
    #                                                                       len(combinedData.loc[:,
    #                                                                           'adj_split_close'].index))
