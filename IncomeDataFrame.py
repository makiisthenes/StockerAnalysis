import matplotlib.pyplot as plt

import utils
from DataFrame import DataFrame



class IncomeDataFrame(DataFrame):
    def __init__(self, ticker, dataframe=None):
        super().__init__()
        self.ticker = ticker.upper()
        self.currency = utils.get_company_currency(ticker)
        self.company_name = None
        if not dataframe:
            dataframe = self.get_dataframe(sheet_type="income")
        self.dataframe = dataframe
        self.flabels, self.dlabels = self.parse_dataframe()
        self.column_int = 0
        self.revenues = []
        self.expenses = []
        self.big_values = []

        # Raw Data Points
        self.tr = self.get_row('totalRevenue', self.big_values)  # Total Revenue
        self.cor = self.get_row('costOfRevenue', self.big_values)  # Cost of Revenue
        self.gp = self.get_row('grossProfit', self.big_values)  # Gross Profit

        self.rd = self.get_row("researchDevelopment", self.expenses)  # Research Development
        self.sga = self.get_row('sellingGeneralAdministrative', self.expenses)  # Selling General and Administrative
        self.ooe = self.get_row('otherOperatingExpenses', self.expenses)  # Other Operating Expenses
        self.toe = self.get_row('totalOperatingExpenses', self.big_values)  # Total Operating Expenses
        self.oi = self.get_row('operatingIncome', self.revenues)  # Operating Income

        self.ie = self.get_row('interestExpense', self.expenses)  # Interest Expense
        self.toie = self.get_row('totalOtherIncomeExpenseNet', self.expenses)  # Total Other Income Expense Net
        self.ibt = self.get_row('incomeBeforeTax', self.revenues)  # Income before Tax
        self.ite = self.get_row('incomeTaxExpense', self.expenses)  # Income Tax Expense
        self.ntco = self.get_row('netIncomeFromContinuingOps', self.revenues)  # Net Income From Continuing Operations.
        self.ni = self.get_row('netIncome', self.revenues)  # Net Income
        self.ntacs = self.get_row('netIncomeApplicableToCommonShares', self.revenues)  # Net Income Applicable To Common Shares.



        self.eac = self.get_row('effectOfAccountingCharges')  # Effect Of Accounting Charges
        self.mi = self.get_row('minorityInterest')  # Minority Interest

        self.ei = self.get_row('extraordinaryItems')  # Extraordinary Items
        self.nr = self.get_row('nonRecurring')  # Non Recurring
        self.ot = self.get_row('otherItems')  # Other Items

        self.do = self.get_row('discontinuedOperations')  # Discontinued Operations
        self.ebit = self.get_row('ebit')  # EBIT


        if self.revenues:
            self.column_int +=1
        if self.expenses:
            self.column_int +=1
        if self.big_values:
            self.column_int +=1


        # Processed Data Points.
        if (not self.tr.empty and not self.cor.empty) or (not self.oi.empty and not self.tr.empty):
            self.column_int +=1
            # Gross Margin
            if not self.tr.empty and not self.cor.empty:
                self.gm = ((self.tr - self.cor) / self.tr) * 100
            # Operating Margin
            if not self.oi.empty and not self.tr.empty:
                self.om = (self.oi / self.tr) * 100

        # Stats
        self.pm = (self.ntco / self.tr) * 100  # Profit Margin






    # Final Result methods, present to user.
    def plot_graph(self):
        plt.figure(figsize=(10, 8))  # Window Size in inches.
        # Plot Methods Here
        self.figure1_plot()
        self.figure2_plot()
        self.figure3_plot()
        self.figure4_plot()
        plt.suptitle(f"{self.company_name} [{self.ticker.upper()}] Income Statement Analysis")
        plt.show()


    def figure1_plot(self):
        """
        Plots Key Performance Margins.
        """
        if self.column_int >= 1:
            fig1_legend = ["Gross Margin", "Operating Margin", "Profit Margin"]
            plt.subplot(self.subplot_col_int(1))
            plt.plot(self.gm)  # Gross Margin Ratio.
            for i in range(len(self.gm.values)):
                plt.text(self.gm.index[i], self.gm.values[i], str(round(self.gm.values[i], 2)) + "%")
            # Good Gross Margin is dependant on the industry the company is in.
            plt.plot(self.om)  # Operating Margin Ratio.
            for i in range(len(self.om.values)):
                plt.text(self.om.index[i], self.om.values[i], str(round(self.om.values[i], 2))+ "%")
            plt.plot(self.pm)  # Profit Margin Ratio.
            for i in range(len(self.pm.values)):
                plt.text(self.pm.index[i], self.pm.values[i], str(round(self.pm.values[i], 2)) + "%")
            plt.title(f"Income Basic Ratios.")
            plt.ylabel("% Percentage Ratio")
            plt.xlabel("Yearly Dates")
            plt.axhline(y=0, color='b', linestyle='--')
            plt.axhline(y=50, color='b', linestyle='--')
            plt.legend(fig1_legend, loc="lower right")


    def figure2_plot(self):
        """
        Plots Expenses Data Points.
        """
        if self.column_int >= 2:
            fig2_legend = []
            plt.xlabel("Yearly Dates")
            plt.ylabel(f"Values in {self.currency}")
            plt.subplot(self.subplot_col_int(2))
            for label, asset in self.expenses:
                fig2_legend.append(label)
                plt.plot(asset)
            plt.title(f"Expenses Values.")
            plt.legend(fig2_legend, loc="lower right")
            # Add all assets that are available.


    def figure3_plot(self):
        if self.column_int >= 3:
            fig3_legend = []
            plt.xlabel("Yearly Dates")
            plt.ylabel(f"Values in {self.currency}")
            plt.subplot(self.subplot_col_int(3))
            for label, asset in self.revenues:
                fig3_legend.append(label)
                plt.plot(asset)
            plt.title(f"Revenues Values.")
            plt.legend(fig3_legend, loc="lower right")
            # Add all assets that are available.

    def figure4_plot(self):
        """
        Plot fourth graph on page, debt to equity ratio.
        """
        if self.column_int >=4:
            fig4_legend = []
            plt.xlabel("Yearly Dates")
            plt.ylabel(f"Values in {self.currency}")
            plt.subplot(self.subplot_col_int(4))
            for label, asset in self.big_values:
                fig4_legend.append(label)
                plt.plot(asset)
            plt.title(f"Macro Values.")
            plt.legend(fig4_legend, loc="lower right")
            # Add all assets that are available.


    def show_stats(self):
        if not self.gm.empty:
            self.parse_stat(self.gm, "Gross Margin")
        if not self.om.empty:
            self.parse_stat(self.om, "Operating Margin")
        if not self.pm.empty:
            self.parse_stat(self.pm, "Profit Margin")
        self.parse_stat(None, "Industry Ratios")
