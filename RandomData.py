import pandas as pd

class RandomData(object) :
    def __init__(self):
        pass

    def generateRandomData(self):
        #
        # GENERATE RANDOM DATA
        pricesDataRandom = {
            'close': np.random.normal(30, 1, 5)
        }

        incomeStatementDataRandom = {
            'basiceps': [1, 1.10, 1.21, 1.33, 1.46],
            'dilutedeps': [1, 1.10, 1.21, 1.33, 1.46],
            'epsgrowth': [1, 1.10, 1.21, 1.33, 1.46]
        }

        calculationsDataRandom = {
            'bookvaluepershare': [1, 1.10, 1.21, 1.33, 1.46],
            'roe': [.20, .30, .31, .35, .40]
        }

        pricesData = pd.DataFrame(pricesDataRandom, index=pd.date_range('2016-01-01', periods=5))
        print pricesData

        incomeStatementData = pd.DataFrame(incomeStatementDataRandom, index=pd.date_range("2016-01-01", periods=5))
        print incomeStatementData

        calculationsData = pd.DataFrame(calculationsDataRandom, index=pd.date_range("2016-01-01", periods=5))
        print calculationsData

        return { "prices" : pricesData,
                 "income_statement" : incomeStatementData,
                 "calculations" : calculationsData}