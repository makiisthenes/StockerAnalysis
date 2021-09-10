# Income Sheet Check
from yahoo_fin import stock_info
import matplotlib.pyplot as plt
import utils
from IncomeDataFrame import IncomeDataFrame

i1 = IncomeDataFrame("intc")
i1.show_stats()
i1.plot_graph()