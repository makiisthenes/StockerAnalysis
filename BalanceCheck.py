from BalanceDataFrame import BalanceDataFrame

# ticker = "googl"
ticker = "INTC"  # intel
b1 = BalanceDataFrame(ticker)
print(b1.flabels)
print(b1.show_stats())
b1.plot_graph()  # Blocking code


# b1.show_contents()
# stock_stats = stock_info.get_stats('nflx')
# print(stock_stats)
# stock_val_stats = stock_info.get_stats_valuation("nflx")
# print(stock_val_stats)
# print(b1.get_raw_json())