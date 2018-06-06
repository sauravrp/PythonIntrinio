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

    def pct_change_stats(self, title, series):
        print "\n-----------------------{}-------------------------".format(title)
        print "             Value              (%) Change"
        for index, value in series.iteritems():
            print "{}         {:,.2f}           {:,.2f}%".format(index, value,  series.pct_change()[index]*100)

        print "\n{} year average % growth = {:,.2f}%".format(len(series.pct_change().dropna().index), series.pct_change().mean()*100)
        if len(series) >= 5:
            print "{} year average % growth = {:,.2f}%".format(5, series.pct_change().tail(5).mean() * 100)
        print "last year average % growth = {:,.2f}%".format(series.pct_change().tail(1).iloc[0] * 100)

        cagr_growth_rate = self.CAGR(series.dropna().iloc[0],
                                     series.dropna().iloc[::-1].iloc[0],
                                    len(series.dropna().index))

        print "CAGR Growth Rate over {} years is {:0,.2f}%".format(len(series.dropna().index), cagr_growth_rate * 100)
        print "-------------------------------------------------------------\n"

    def average_stats(self, title, series):
        print "\n-----------------------{}-------------------------".format(title)
        print "              Value                "
        for index, value in series.iteritems():
            print "{}         {:,.2f}".format(index, value)

        self.average_multiyear_stats(series)
        print "-------------------------------------------------------------\n"

    def average_multiyear_stats(self, series):
        print "\n{} year average = {:,.2f}".format(len(series.index) - 1, series.mean())
        if len(series) >= 5:
            print "{} year average = {:,.2f}".format(5, series.tail(5).mean() )
        print "last year value = {:,.2f}".format(series.tail(1).iloc[0])
