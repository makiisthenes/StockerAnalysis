from abc import ABC, abstractmethod
from yahoo_fin import stock_info, news
import utils

# Abstract Class for all statements.
class DataFrame(ABC):
    def __init__(self):
        self.ticker = None
        self.company_name = None
        self.dataframe = None
        self.flabels = None
        self.column_int = None


    @abstractmethod
    def plot_graph(self):
        pass

    @abstractmethod
    def show_stats(self):
        pass


    # Methods inherited.
    def get_dataframe(self, sheet_type):
        """
        Will get pandas dataframe of chosen statement for given ticker.
        sheet_type: String | Choose from "balance", "income" or "cashflow" statements.
        """
        dataframe = []
        if sheet_type == "balance":
            dataframe = stock_info.get_balance_sheet(self.ticker)  # Also confirms ticker exists.
        elif sheet_type == "income":
            dataframe = stock_info.get_income_statement(self.ticker)
        elif sheet_type == "cashflow":
            dataframe = stock_info.get_cash_flow(self.ticker)
        else:
            print("You need to add a sheet_type parameter to the get_dataframe() method in class.")
            exit()
        self.company_name = utils.get_company_name(self.ticker)  # Get companies name using ticker.
        if not dataframe.empty:
            return dataframe
        else:
            print(f"We can't find any information with the ticker {self.ticker} you have entered.")


    def parse_dataframe(self):
        """
        Extract information such as x, y labels from dataframe.
        """
        label1 = list(self.dataframe.index)  # Financial Labels
        label2 = [date.date() for date in list(self.dataframe.columns)]  # Date Labels
        return label1, label2


    def get_row(self, label, append_iter=None):
        """
        From dataframe extract row with matching query as financial label.
        """
        try:
            data_row = self.dataframe.iloc[self.flabels.index(label)]
            if append_iter is not None:
                append_iter.append((label, data_row))
        except ValueError as e:
            # This label is not in dataframe finance labels available.
            return []
        else:
            return data_row


    def subplot_col_int(self, position):
        """
        Used for designating the subplot value, according on whether there is enough data
        for presentation.
        """
        sub_string = str(self.column_int) + "1" + str(position)
        return int(sub_string)


    def parse_stat(self, data, title):
        """
        Method used in conjunction with show_stats method.
        :param data: DataFrame
        :param title: String
        :return: None
        """
        try:
            dates = [date.date() for date in list(data.axes[0])]
            print(title)
            for index, value in enumerate(data.values):
                print(f"{dates[index]} --> {value}")
        except Exception as e:
            pass
        return


    # Debugging Methods.
    def show_contents(self):
        """Shows type of data passed and contents of this data."""
        print(type(self.dataframe))
        print(self.dataframe)


    # Experimental Methods to use later on.
    def gen_stats(self):
        """These stats are just extracted from yahoo and not calculated locally."""
        stock_stats = stock_info.get_stats(self.ticker)
        val_stock_stats = stock_info.get_stats_valuation(self.ticker)
        print(stock_stats)
        print(val_stock_stats)


    def get_news(self):
        news_outlet = news.get_yf_rss(self.ticker)
        return news_outlet