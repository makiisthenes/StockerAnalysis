from BalanceDataFrame import BalanceDataFrame
from IncomeDataFrame import IncomeDataFrame
from CashDataFrame import CashDataFrame
from InsiderTradingStats import get_insider_stats

def main():
    # Getting Balance Sheet Data for a specific company [NFLX].
    b1 = BalanceDataFrame("NFLX")
    b1.show_stats()
    b1.plot_graph()


    # Getting Income Sheet Data for a specific company [INTC].
    i1 = IncomeDataFrame("INTC")
    i1.show_stats()
    i1.plot_graph()


    # Getting Cashflow Data for a specific company [NFLX].
    c1 = CashDataFrame("NFLX")
    print(c1.cf)  # Free Cash Flow


    # Get Insider Info on Netflix for the last 2 years.
    get_insider_stats("NLFX")


if __name__ == "__main__":
    main()
