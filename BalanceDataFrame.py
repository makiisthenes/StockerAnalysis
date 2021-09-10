import matplotlib.pyplot as plt
from DataFrame import DataFrame


class BalanceDataFrame(DataFrame):
    def __init__(self, ticker, dataframe=None):
        super().__init__()
        self.ticker = ticker.upper()
        self.company_name = None
        if not dataframe:
            dataframe = self.get_dataframe(sheet_type="balance")
        self.dataframe = dataframe
        self.flabels, self.dlabels = self.parse_dataframe()
        self.column_int = 0
        self.assets = []
        self.liabilities = []


        # Assets
        self.c = self.get_row("cash", self.assets)  # Cash
        self.sti = self.get_row('shortTermInvestments', self.assets)  # Short Term Investments
        self.nr = self.get_row("netReceivables", self.assets)  # Net Receivables
        self.nta = self.get_row('netTangibleAssets', self.assets)  # Net Tangible Assets
        self.i = self.get_row("inventory", self.assets)  # Inventory
        self.oca = self.get_row("otherCurrentAssets", self.assets)  # Other Current Assets
        self.tca = self.get_row('totalCurrentAssets', self.assets)  # Total Current Assets

        self.lti = self.get_row('longTermInvestments', self.assets)  # Long Term Investments
        self.ppe = self.get_row('propertyPlantEquipment', self.assets)  # Property Plant & Equipment
        self.gw = self.get_row("goodWill", self.assets)  # Good Will
        self.ia = self.get_row('intangibleAssets', self.assets)  # Intangible Assets
        self.oa = self.get_row('otherAssets', self.assets)  # Other Non Current Assets
        self.dlc = self.get_row('deferredLongTermAssetCharges', self.assets)  # Deferred Long Term Asset Charges
        self.ta = self.get_row('totalAssets', self.assets)  # Total Assets


        # Liabilities
        self.cb = self.get_row('shortLongTermDebt', self.liabilities)  # Current Debt
        self.ap = self.get_row('accountsPayable', self.liabilities)  # Accounts Payable
        self.ocl = self.get_row('otherCurrentLiab', self.liabilities)  # Other Current Liabilities
        self.tcl = self.get_row('totalCurrentLiabilities', self.liabilities)  # Total Current Liabilities

        self.ltd = self.get_row('longTermDebt', self.liabilities)  # Long Term Debt
        self.ol = self.get_row('otherLiab', self.liabilities)  # Other Liabilities
        self.dltl = self.get_row('deferredLongTermLiab', self.liabilities)  # Deferred Long Term Liability
        self.mi = self.get_row('minorityInterest', self.liabilities)  # Minority Interest
        # Negative Goodwill
        self.tl = self.get_row('totalLiab', self.liabilities)  # Total Liabilities


        # Stockholder Equity
        self.cs = self.get_row('commonStock')  # Common Stock
        self.re = self.get_row('retainedEarnings')  # Retained Earnings
        self.ts = self.get_row('treasuryStock')  # Treasury Stock
        self.csp = self.get_row('capitalSurplus')  # Capital Surplus
        self.ose = self.get_row('otherStockholderEquity')  # Other Stockholder Equity
        self.tse = self.get_row('totalStockholderEquity')  # Total Stockholder Equity


        # Processed Data Points

        # Graph 1
        if not self.tca.empty and not self.tcl.empty:
            self.tca_tcl_ratio = self.tca / self.tcl  # Total Current Asset to  Total Current Liability Ratio
            self.column_int +=1
        else:
            print("There's no total current assets or liabilities data available for this stock.")
            self.tca_tcl_ratio = []

        if not self.ta.empty and not self.tl.empty:
            self.ta_tl_ratio = self.ta / self.tl  # Total Asset to  Total Liability Ratio
        else:
            print("There's no total assets or liabilities data available for this stock.")
            self.ta_tl_ratio = []

        # Graph 2
        if self.assets:
            # Check if asset list is empty.
            self.column_int += 1

        # Graph 3
        if self.liabilities:
            self.column_int +=1

        # Graph 4

        if (not self.tl.empty and not self.tse.empty) or (not self.ltd.empty and not self.tse.empty):
            self.column_int += 1
            if not self.tl.empty and not self.tse.empty:
                self.tde = self.tl / self.tse  # Total Debt-to-Equity Ratio
            if not self.ltd.empty and not self.tse.empty:
                self.ltde = self.ltd / self.tse  # Long Term Debt-to-Equity Ratio


        # Can also look at growth percentages and averages to enrich data insights.


    def plot_graph(self):
        plt.figure(figsize=(10, 8))  # Window Size in inches.
        self.figure1_plot()
        self.figure2_plot()
        self.figure3_plot()
        self.figure4_plot()
        plt.suptitle(f"{self.company_name} [{self.ticker.upper()}] Balance Sheet Analysis")
        plt.show()

    # Plotting with matplotlib
    def figure1_plot(self):
        """
        Plot first graph on page, assets and liabilities.
        """
        if self.column_int >= 1:
            fig1_legend = ["Current Asset/Liability Ratio", "Total Asset/ Total Liability Ratio"]
            plt.subplot(self.subplot_col_int(1))
            plt.plot(self.tca_tcl_ratio)  # Total Current Asset/ Liability Ratio.
            plt.plot(self.ta_tl_ratio)  # Total Asset/ Liability Ratio.
            plt.title(f"Asset-Liability Ratios.")
            plt.xlabel("Yearly Dates")
            plt.axhline(y=1, color='r', linestyle='--')  # Creating an asymptote at ratio 1.0, Ok Ratio.
            plt.axhline(y=2, color='g', linestyle='--')  # Creating an asymptote at ratio 2.0, Great Ratio.
            plt.legend(fig1_legend, loc="lower right")


    def figure2_plot(self):
        """
        Plot second graph on page, assets.
        """
        if self.column_int >=2:
            fig2_legend = []
            plt.xlabel("Yearly Dates")
            plt.subplot(self.subplot_col_int(2))
            for label, asset in self.assets:
                fig2_legend.append(label)
                plt.plot(asset)
            plt.title(f"Asset Values.")
            plt.legend(fig2_legend, loc="lower right")
            # Add all assets that are available.

    def figure3_plot(self):
        """
        Plot third graph on page, liabilities.
        """
        if self.column_int >=3:
            fig3_legend = []
            plt.xlabel("Yearly Dates")
            plt.subplot(self.subplot_col_int(3))
            for label, asset in self.liabilities:
                fig3_legend.append(label)
                plt.plot(asset)
            plt.title(f"Liabilities Values.")
            plt.legend(fig3_legend, loc="lower right")
            # Add all assets that are available.

    def figure4_plot(self):
        """
        Plot fourth graph on page, debt to equity ratio.
        """
        if self.column_int >=4:
            fig4_legend = []
            if not self.tl.empty and not self.tse.empty:
                plt.plot(self.tde)
                fig4_legend.append("Total Debt-to-equity Ratio")
            if not self.ltd.empty and not self.tse.empty:
                plt.plot(self.ltde)
                fig4_legend.append("Long Term Debt-to-Equity Ratio")
            # What the industry debt-equity ratio average is for this company.
            plt.subplot(self.subplot_col_int(4))
            plt.title(f"D/E Ratio")
            plt.legend(fig4_legend, loc="lower right")
            # Add all assets that are available.

    def show_stats(self):
        """
        Will present users with interesting stats and percentage ratio to give them a informed decision of whether the
        company is financially strong.
        :return: None
        """
        print("\n" + "#" * 10 + "Solvency Ratios" + "#" * 10)
        # Debt Ratios
        debtRatio = self.tl / self.ta
        self.parse_stat(debtRatio, "Debt Ratios")
        # Debt-to-equity Ratios
        print("-" * 10 + "\n" * 1)
        debt_eqRatio = self.tl / self.tse
        self.parse_stat(debt_eqRatio, "Debt-to-Equity Ratios")
        # Interest Coverage Ratios  | Need EBIT from Income Statement


        print("\n" + "#" * 10 + "Liquidity Ratios" + "#" * 10)
        # Current Ratios
        currentRatio = self.tca / self.tcl
        self.parse_stat(currentRatio, "Current Ratios")
        # Quick Ratio
        print("-" * 10 + "\n" * 1)
        inventory = 0 if not self.i.empty else self.i.empty
        quickRatio = (self.tca - inventory) / self.tcl
        self.parse_stat(quickRatio, "Quick Ratios")
        # Cash Ratio
        print("-" * 10 + "\n" * 1)
        cashRatio = self.c / self.tcl
        self.parse_stat(cashRatio, "Cash Ratios")


        print("\n" + "#" * 10 + "Profitability Ratios" + "#" * 10)
        # Income statement needed for all of the ratios in this category


        print("\n" + "#" * 10+ "Activity Ratios" + "#" * 10)