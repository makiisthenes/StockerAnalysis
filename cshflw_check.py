# Cash Flow Check
from yahoo_fin import stock_info
import utils

unique_labels = []
utils.display_max_pandas()
ticker = "NFLX"
cash_flow = stock_info.get_cash_flow(ticker)
flabels, _ = utils.parse_dataframe(stock_info.get_cash_flow("NFLX"))
flabels1, _ = utils.parse_dataframe(stock_info.get_cash_flow("WMT"))
flabels2, _ = utils.parse_dataframe(stock_info.get_cash_flow("INTC"))
flabels3, _ = utils.parse_dataframe(stock_info.get_cash_flow("GOOG"))
flabels4, _ = utils.parse_dataframe(stock_info.get_cash_flow("HD"))
flabels5, _ = utils.parse_dataframe(stock_info.get_cash_flow("PG"))


utils.no_dup_list_append(unique_labels, flabels)
utils.no_dup_list_append(unique_labels, flabels1)
utils.no_dup_list_append(unique_labels, flabels2)
utils.no_dup_list_append(unique_labels, flabels3)
utils.no_dup_list_append(unique_labels, flabels4)
utils.no_dup_list_append(unique_labels, flabels5)

print(unique_labels)

