import pandas as pd
from Globals import DEBUG

class HandleStockSplit(object) :
    def __init__(self):
        pass

    def adjustStockSplits(self, dataFrame):
        split_factor = 1
        adj_split_close = pd.Series(data=dataFrame.loc[:, 'close'], index=dataFrame.index)
        adj_split_close.name = "adj_split_close"
        if DEBUG == True:
            print "Year                       Close      Split Ratio   SplitAdjClose       "
        for index, row in dataFrame.iterrows():
            adj_split_close.loc[index] = split_factor * row.loc['close']
            split_factor = split_factor * row['split_ratio']
            if DEBUG == True:
                print "{}         ${:0,.2f}      {:0,.4f}      ${:0,.2f}".format(index, row.loc['close'], row.loc['split_ratio'], adj_split_close.loc[index])

        dataFrame.loc[:, adj_split_close.name] = adj_split_close
        return dataFrame
    

