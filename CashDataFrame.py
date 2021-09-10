import matplotlib.pyplot as plt
from DataFrame import DataFrame

class CashDataFrame(DataFrame):
    def __init__(self, ticker, dataframe=None):
        super().__init__()
        self.ticker = ticker.upper()
        self.company_name = None
        if not dataframe:
            dataframe = self.get_dataframe(sheet_type="cashflow")
        self.dataframe = dataframe
        self.flabels, self.dlabels = self.parse_dataframe()
        self.column_int = 0


        # Cashflow Income
        self.ni = self.get_row("netIncome")  # Net Income

        # Cashflow from Operating Activities
        self.coa = self.get_row("changeToOperatingActivities")  # Changes to Operating Activities
        self.d = self.get_row("depreciation")  # Depreciation
        self.cic = self.get_row("changeInCash")  # Change in Cash
        self.ctar = self.get_row("changeToAccountReceivables")  # Changes to Account Receivables
        self.ctl = self.get_row("changeToLiabilities")  # Changes to Liabilities
        self.cti = self.get_row("changeToInventory")  # Change to inventory
        self.tcoa = self.get_row("totalCashFromOperatingActivities")  # Total Cash From Operating Activities
        self.eex = self.get_row("effectOfExchangeRate")  # Effect of Exchange Rate


        # Cashflow from Investing Activities
        self.i = self.get_row("investments")  # Investments
        self.ocia = self.get_row("otherCashflowsFromInvestingActivities")  # Other Cashflows from Investing Activities
        self.tcia = self.get_row("totalCashflowsFromInvestingActivities")  # Total cash flows from Investing Activities


        # Cashflow from Financing Activities
        self.nb = self.get_row("netBorrowings")  # Net Borrowings
        self.ros = self.get_row("repurchaseOfStock")  # Repurchase of Stock
        self.dp = self.get_row("dividendsPaid")  # Dividends Paid
        self.ocfa = self.get_row("otherCashflowsFromFinancingActivities")  # Other cash flows from Financing Activities
        self.tcfa = self.get_row("totalCashFromFinancingActivities")  # Total Cash from Financing Activities
        self.ios = self.get_row("issuanceOfStock")  # Issuance Of Stock


        # End Finance
        self.ce = self.get_row("capitalExpenditures")  # Capital Expenditures
        self.cni = self.get_row("changeToNetincome")  # Change to Net Income


        # Processed
        self.cf = self.tcoa - self.ce  # Free Cash Flow
        # This free cashflow tells us who much cash or cash equivalence, the company has from all expenditures, this year.

        # If a company has a negative cash flow and you see the purchase of stock or issuance of dividends that can be seen as a red flag.
        # Acquiring a company when there was no reason to, can also be a red flag.















    def plot_graph(self):
        pass

    def show_stats(self):
        pass