
TICKER = "AAPL" #raw_input("Enter Ticker?")
TEN_YEAR_TREASURY = 2.902
PRICES_PULL_START_DATE = "2008-01-01" # pulled yearly here
DEBUG = True
THIS_YEAR=2018
DISCOUNT_RATE=float(15)
STANDARD_PERIOD_PV=10



#
# def calcEPS(incomeStmtData, calculationsData) :
#     print "--------------- EPS data -------------------------------------------------"
#     epsData = pd.concat([incomeStmtData.loc[:, 'basiceps'],
#                          incomeStmtData.loc[:, 'dilutedeps'],
#                          calculationsData.loc[:, 'epsgrowth'] * 100], axis=1)
#
#     print "Year      basiceps      dilutedeps        epsgrowth"
#     for index, row in epsData.iterrows():
#         print "%s        $%4.2f         $%4.2f             %4.2f%%" % (
#         index, row['basiceps'], row['dilutedeps'], row['epsgrowth'])
#
#
#     eps_growth_rate = util.CAGR(incomeStmtData.loc[:, 'dilutedeps'].iloc[0],
#               incomeStmtData.loc[:, "dilutedeps"].iloc[::-1].iloc[0],
#               len(incomeStmtData.loc[:, 'dilutedeps'].index))
#
#     print "EPS Growth Rate is {:0,.2f}%".format(eps_growth_rate*100)
#
#     print "--------------------------------------------------------------------------"
#
# def calcBVPS(incomeStmtData, calculationsData) :
#     # Calculate Retained earnings per share
#     bookvalue = calculationsData.loc[:, "bookvaluepershare"] * incomeStmtData.loc[:,
#                                                                              "weightedavedilutedsharesos"]
#     bookvalue.name = "bookvalue"
#     cumulativeData = pd.concat([calculationsData.loc[:, 'bookvaluepershare'],
#                                 bookvalue,
#                                 incomeStmtData.loc[:, "weightedavedilutedsharesos"]], axis=1)
#     cumulativeData = util.dropNaRows(cumulativeData, 'bookvalue')
#
#
#     print "--------------- Book Value --------------------------------------------"
#     print "Year      Book Value/Share      Book Value                         Num Shares"
#     for index, row in cumulativeData.iterrows():
#         print "{}       ${:0,.2f}             ${:20,.2f}            {:20,.2f}".format(index,
#                                                                                        row['bookvaluepershare'],
#                                                                                        row['bookvalue'],
#                                                                                        row['weightedavedilutedsharesos'])
#
#     bvps_growth_rate = util.CAGR(cumulativeData.loc[:, 'bookvaluepershare'].iloc[0],
#                                  cumulativeData.loc[:, "bookvaluepershare"].iloc[::-1].iloc[0],
#                                     len(cumulativeData.loc[:, 'bookvaluepershare'].index))
#
#     bv_growth_rate = util.CAGR(cumulativeData.loc[:, 'bookvalue'].iloc[0],
#                                cumulativeData.loc[:, "bookvalue"].iloc[::-1].iloc[0],
#                                  len(cumulativeData.loc[:, 'bookvalue'].index))
#
#     util.pct_change_stats("Book Value", cumulativeData.loc[:,'bookvalue'])
#
#     print "Book Value Per Share Growth Rate is {:0,.2f}%".format(bvps_growth_rate * 100)
#     print "Book Value Growth Rate is {:0,.2f}%".format(bv_growth_rate * 100)
#
#     print "------------------------------------------------------------------------------\n"
#
