import numpy as np
import pandas as pd

class Util(object):
    def __init__(self):
        pass

    # pass in series
    def calculateDelta(self, dataSeries):
        delta = float(dataSeries.iloc[::-1].head(1)) - float(
            dataSeries.iloc[0::].head(1))
        return delta

    # drops NA rows
    def dropNaRows(self, dataFrame, column):
        dataFrame = dataFrame[np.isfinite(dataFrame[column])]
        return dataFrame

        # drops NA rows

    def dropNaInAllColumns(self, dataFrame):
        for column in dataFrame:
            dataFrame = self.dropNaRows(dataFrame, column)
        return dataFrame

    # if no column exists, fills it up with zero
    def checkAndFillColumn(self, dataFrame, column, value):
        if column not in dataFrame.columns:
            genData = []
            for i in range(0, len(dataFrame.index)):
                genData.append(value)
            seriesData = pd.Series(data=genData, index=dataFrame.index, name=column)
            dataFrame.loc[:, column] = seriesData

    # https://feliperego.github.io/blog/2016/08/10/CAGR-Function-In-Python
    def CAGR(self, first, last, periods):
        periods = float(periods)
        return (last / first) ** (1 / periods) - 1
