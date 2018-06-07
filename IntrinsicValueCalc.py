import numpy as np
from Globals import DISCOUNT_RATE, STANDARD_PERIOD_PV

class IntrinsicValueCalc(object):
    def __init__(self):
        pass

    def calcValueBasedOnEPS(self, last_eps):
        # Gather Input Parameters
        est_growth_rate = float(raw_input("Enter estimated growth rate in %? "))
        est_future_pe = int(raw_input("Enter future P/E? "))
        discount_rate = raw_input("Enter discount rate in %? ")
        if discount_rate == "":
            discount_rate = float(DISCOUNT_RATE)
            print "\nUsing default discount rate of {:,.2f}%".format(discount_rate)
        else:
            discount_rate = float(discount_rate)

        # Estimate Future eps
        future_eps = np.fv(rate=float(est_growth_rate / 100), nper=int(STANDARD_PERIOD_PV), pmt=0,
                           pv=last_eps) * -1
        future_share_value = future_eps * est_future_pe
        print "\nFuture eps is ${:,.2f}, future share value at PE of {} is ${:,.2f}".format(future_eps, est_future_pe,
                                                                                            future_share_value)

        cur_price_to_pay = np.pv(rate=float(discount_rate / 100), nper=int(STANDARD_PERIOD_PV), pmt=0,
                                 fv=future_share_value) * -1
        print "Discounting at {:,.2f}% rate, current fair value is ${:,.2f}".format(discount_rate, cur_price_to_pay)

    def calcValueBasedOnBookValueGrowth(self, last_price, bookvaluepershare, dividendSeries):
        # Gather Input Parameters
        est_roe=20.0#float(raw_input("Enter estimated growth ROE in %?"))
        est_retention_rate=100.0#float(raw_input("Enter retention rate in %?"))
        est_future_pe = 12#int(raw_input("Enter future P/E? "))

        equity_growth_rate = est_roe * est_retention_rate
        print "Equity growth rate is {:,.2f}%".format(equity_growth_rate / 100)

        future_equity = np.fv(rate=float(equity_growth_rate / 100), nper=int(STANDARD_PERIOD_PV), pmt=0,
                           pv=bookvaluepershare) * -1

        future_per_earnings_per_share = future_equity * est_roe
        future_share_value = future_per_earnings_per_share * est_future_pe
        print type(dividendSeries)
        print dividendSeries.i#['cashdividendpershare'].iloc[::-1]
       # future_share_value_with_div = future_share_value + dividendSeries['cashdividendpershare'].iloc[::-1].head(10).sum()
        #projReturn = np.rate(nper=STANDARD_PERIOD_PV, pmt=0, pv=last_price, fv=future_share_value_with_div)
        #print "projReturn is {:, .2f}%".format(projReturn)

        # est_growth_rate = float(raw_input("Enter estimated growth rate? "))
        # est_future_pe = int(raw_input("Enter future P/E? "))
        # discount_rate = raw_input("Enter discount rate? ")
        # if discount_rate == "":
        #     discount_rate = float(DISCOUNT_RATE)
        #     print "\nUsing default discount rate of {:,.2f}%".format(discount_rate)
        # else:
        #     discount_rate = float(discount_rate)
        #
        # # Estimate Future eps
        # future_eps = np.fv(rate=float(est_growth_rate / 100), nper=int(STANDARD_PERIOD_PV), pmt=0,
        #                    pv=last_eps) * -1
        # future_share_value = future_eps * est_future_pe
        # print "\nFuture eps is ${:,.2f}, future share value at PE of {} is ${:,.2f}".format(future_eps, est_future_pe,
        #                                                                                     future_share_value)
        #
        # cur_price_to_pay = np.pv(rate=float(discount_rate / 100), nper=int(STANDARD_PERIOD_PV), pmt=0,
        #                          fv=future_share_value) * -1
        # print "Discounting at {:,.2f}% rate, current fair value is ${:,.2f}".format(discount_rate, cur_price_to_pay)


