from pymongo import MongoClient
from pprint import pprint

class dbController:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client["financialData"]
        self.stockCol = self.db["stockData"]
        # Accessing stockData collection from financialData database. MongoDB.

    def create_entry(self, ticker_data):
        """ticker_data format:
        ticker_data = \
            {
                "ticker_name":stock_name,
                "ticker_info":
                    {
                        "company_info": {},
                        "balance": {
                            2020: {"cash": 100000, "shortLongTermDebt": 25000},
                            2019: {"cash": 85000, "shortLongTermDebt": 15000}
                        },
                        "income": {},
                        "cashflow": {},
                    }
            }
        """
        result = self.stockCol.insert_one(ticker_data)
        return result

    def read_entry(self, ticker):
        """ Read a specific ticker entry."""
        query_result = self.stockCol.find_one({'ticker_name': ticker})
        return query_result

    def update_entry(self, ticker, data):
        """Update a specific ticker entry."""
        pass

    def delete_entry(self, ticker):
        """Delete ticker data entry."""
        self.stockCol.find_one({'ticker_name': ticker})
        return

    def print_entry(self, ticker):
        query_result = self.stockCol.find_one({'ticker_name': ticker})
        if query_result:
            pprint(query_result)
        else:
            print(f"Entry is not found, are you sure {ticker} is a stock name in database")
        return