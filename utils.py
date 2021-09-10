import time
import pandas as pd
import yfinance as yf  # Experimental.
import os
import win32com.client
# Utils for stock financials analysis.

# Different stock have different labels on their balance sheets, so assessment can be done differently.
BALANCE_SHEET_LABELS =\
    ['intangibleAssets',  # added
     'totalLiab',  # added
     'totalStockholderEquity',  # added
     'otherCurrentLiab',  # added
     'totalAssets',  # added
     'commonStock',  # added
     'retainedEarnings',  # added
     'otherLiab',  # added
     'treasuryStock',  # added
     'otherAssets',  # added
     'cash',  # added
     'totalCurrentLiabilities',  # added
     'deferredLongTermAssetCharges',  # added
     'shortLongTermDebt',  # added
     'otherStockholderEquity',  # added
     'propertyPlantEquipment',  # added
     'totalCurrentAssets',  # added
     'netTangibleAssets',  # added
     'netReceivables',  # added
     'longTermDebt',  # added
     'accountsPayable',  # added
     'capitalSurplus',  # added
     'minorityInterest',  # added
     'deferredLongTermLiab',  # added
     'otherCurrentAssets',  # added
     'goodWill',  # added
     'longTermInvestments',  # added
     'inventory',  # added
     'shortTermInvestments'  # added
     ]


INCOME_STAT_LABELS = \
    ['researchDevelopment',  # added
     'effectOfAccountingCharges',  # added
     'incomeBeforeTax',  # added
     'minorityInterest',  # added
     'netIncome',  # added
     'sellingGeneralAdministrative',  # added
     'grossProfit',  # added
     'ebit',  # added
     'operatingIncome',  # added
     'otherOperatingExpenses',  # added
     'interestExpense',  # added
     'extraordinaryItems',  # added
     'nonRecurring',  # added
     'otherItems',  # added
     'incomeTaxExpense',  # added
     'totalRevenue',  # added
     'totalOperatingExpenses',  # added
     'costOfRevenue',  # added
     'totalOtherIncomeExpenseNet',  # added
     'discontinuedOperations',  # added
     'netIncomeFromContinuingOps',  # added
     'netIncomeApplicableToCommonShares'  # added
     ]

CASHFLOW_STAT_LABELS = \
    ['changeToLiabilities',  # added
     'totalCashflowsFromInvestingActivities',  # added
     'netBorrowings',  # added
     'totalCashFromFinancingActivities',  # added
     'changeToOperatingActivities',  # added
     'issuanceOfStock',  # added
     'netIncome',  # added
     'changeInCash',  # added
     'effectOfExchangeRate',  # added
     'totalCashFromOperatingActivities',  # added
     'depreciation',  # added
     'otherCashflowsFromInvestingActivities',  # added
     'otherCashflowsFromFinancingActivities',  # added
     'changeToNetincome',  # added
     'capitalExpenditures',  # added
     'investments',  # added
     'repurchaseOfStock',  # added
     'dividendsPaid',  # added
     'changeToInventory',  # added
     'changeToAccountReceivables'  # added
     ]


def parse_dataframe(dataframe):
    """
    Extract information such as x, y labels from dataframe.
    """
    flabels = list(dataframe.index)  # Financial Labels
    dlabels = [date.date() for date in list(dataframe.columns)]  # Date Labels
    return flabels, dlabels


def no_dup_list_append(list1, list2):
    for i in list2:
        if i not in list1:
            list1.append(i)


def get_company_name(ticker):
    return get_company_data(ticker)["longName"]


def get_company_data(ticker):
    comp_name = yf.Ticker(ticker)
    return comp_name.info

def get_company_currency(ticker):
    return get_company_data(ticker)["financialCurrency"]


def get_gross_margin_average(industry):
    pass

# Restoring Corrupt Excel Files using Python
def fix_corrupt_excel_file(filename):
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = False  # Hide Excel Window.
    xl.DisplayAlerts = False  # Allow Changes to Local Files without User Warning.

    # print(os.path.join(os.getcwd(), filename))
    wb = xl.Workbooks.Open(os.path.join(os.getcwd(), filename))
    new_filename = "".join(filename.split(".")[0:-1]) + "fixed" + ".xlsx"
    insider_dir = os.path.join(os.path.expanduser('~/Documents'), "InsiderData")
    if not os.path.isdir(insider_dir):
        os.makedirs(insider_dir)
    new_file_path = os.path.join(insider_dir, new_filename)
    wb.ActiveSheet.SaveAs(new_file_path, 51)  # https://docs.microsoft.com/en-us/office/vba/api/excel.xlfileformat
    xl.Application.Quit()
    return new_file_path

def display_max_pandas():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)