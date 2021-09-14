import os
import requests, urllib.parse
import pandas
import datetime
import numpy as np
import utils, logging

# Debugging
# logging.basicConfig(level=logging.DEBUG)
# utils.display_max_pandas()  # To see database fully.

def search_company_insider_db(ticker) -> pandas.DataFrame:
    """
    Will dataframe of insider transaction, only applicable to US stocks and at the mercy of unreliable website php scripts.
    Return data: pandas.DataFrame
    Obtained from: http://www.j3sg.com/
    """
    email = urllib.parse.quote("michaelperes1@gmail.com")
    password = urllib.parse.quote("OvgGdjJccyvrg5DdfnVl")  # I give permission for anyone to use these credentials.
    login_url = "http://www.j3sg.com/log-test.php?remember=1&DV2=yes&userid=michaelperes1@gmail.com&password=OvgGdjJccyvrg5DdfnVl&Submit22=GO"
    ticker_url = f"http://www.j3sg.com/Reports/Stock-Insider/Generate.php?tickerLookUp={ticker}&DV=no&remember=1&userid={email}&password={password}"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    session = requests.Session()
    session.get(login_url, headers=HEADERS)
    data = session.get(ticker_url, headers=HEADERS)
    php_sess = ""
    if data.ok:
        for c in session.cookies:
            # print(c.name, c.value)
            if c.name == "PHPSESSID":
                php_sess = c.value
    if not php_sess:
        print("PHP Session ID couldn't not be determined...")
        exit()
    url = "http://www.j3sg.com/Reports/Stock-Insider/retrieveDownloads.php?download1=yes&Submit2=Download"
    filename = f"{ticker.upper()}-{datetime.datetime.today().strftime('%Y-%m-%d')}_insider_data.xls"
    # print(session.cookies)
    data = session.get(url, headers=HEADERS)
    # pprint(data.content)
    if data.ok:
        with open(filename, "wb+") as writer:
            writer.write(data.content)
        # For some reason the data from the excel file is always corrupt or wrong format.  | https://www.devcoons.com/how-to-restore-corrupted-excel-files-using-python/
        file_path = utils.fix_corrupt_excel_file(filename)
        print(f"Insider Data File Path: {file_path}")
        os.remove(filename)
        dataframe = pandas.read_excel(file_path)
        session.close()
        return dataframe
    logging.error("Error when accessing website.")

def parse_sell_buy_stats(data):
    """
    Will tell us how many people sold or bought and their values for date periods of 0-3 months, 3-6 months, 6-9 months, 9-12 months, and 12-24 months
    :param data: pandas.DataFrame
    :return: stats: dict
    """
    ACTIONS = {
        "B": "Buy",
        "S": "Sell",
        "OE": "Options Exercised",
        "IO": "Initial Ownership",
        "AB": "Automatic Buy",
        "AS": "Automatic Sell",
        "A": "Acquired",
        "D": "Disposed"
    }


    # Date Constraints
    today = datetime.datetime.today().date()  # .strftime('%d-%m-%Y')
    three_month = (datetime.datetime.today() - datetime.timedelta(weeks=12)).date()
    six_month = (datetime.datetime.today() - datetime.timedelta(weeks=24)).date()
    one_year = (datetime.datetime.today() - datetime.timedelta(days=365)).date()
    two_year = (datetime.datetime.today() - datetime.timedelta(days=365*2)).date()
    # print(today, three_month, six_month, one_year, two_year)

    # Assign Lists
    buy_actions = [0, 0, 0, 0, 0]
    sell_actions = [0, 0, 0, 0, 0]
    buy_shares = [0.0, 0.0, 0.0, 0.0, 0.0]
    sell_shares = [0.0, 0.0, 0.0, 0.0, 0.0]
    buy_value = [0.0, 0.0, 0.0, 0.0, 0.0]
    sell_value = [0.0, 0.0, 0.0, 0.0, 0.0]


    refined_data = data.loc[np.logical_or(data.Action =="S", data.Action == "B")]
    for index, row in refined_data.iterrows():
        # Determine which time category.
        current_date = row["Tran. Date"].date()
        filers_name = row["Filer Name"]
        action = row["Action"]
        shares = row["Shares"]
        mkt_value = str(row["Mkt Value"]).split("$")[1].replace(",","")

        if today == current_date:
            if action == "B":
                buy_actions[0] +=1
                buy_shares[0] += float(shares)
                buy_value[0] += float(mkt_value)
            else:
                sell_actions[0] += 1
                sell_shares[0] += float(shares)
                sell_value[0] += float(mkt_value)

        elif today > current_date > three_month:
            if action == "B":
                buy_actions[1] +=1
                buy_shares[1] += float(shares)
                buy_value[1] += float(mkt_value)
            else:
                sell_actions[1] += 1
                sell_shares[1] += float(shares)
                sell_value[1] += float(mkt_value)

        elif three_month >= current_date > six_month:
            if action == "B":
                buy_actions[2] +=1
                buy_shares[2] += float(shares)
                buy_value[2] += float(mkt_value)
            else:
                sell_actions[2] += 1
                sell_shares[2] += float(shares)
                sell_value[2] += float(mkt_value)

        elif six_month >= current_date > one_year:
            if action == "B":
                buy_actions[3] +=1
                buy_shares[3] += float(shares)
                buy_value[3] += float(mkt_value)
            else:
                sell_actions[3] += 1
                sell_shares[3] += float(shares)
                sell_value[3] += float(mkt_value)

        elif one_year >= current_date > two_year:
            if action == "B":
                buy_actions[4] +=1
                buy_shares[4] += float(shares)
                buy_value[4] += float(mkt_value)
            else:
                sell_actions[4] += 1
                sell_shares[4] += float(shares)
                sell_value[4] += float(mkt_value)
        else:
            # We don't need to parse more than 2 years before.
            break

    stats = \
        f"""
            Today, 
                {buy_actions[0]} insiders(s) bought the stock.
                Total Shares: {buy_shares[0]} Bought.
                Total Amount: ${buy_value[0]} in total. 
                
                {sell_actions[0]} insiders(s) sold the stock.
                Total Shares: {sell_shares[0]} Sold.
                Total Amount: ${sell_value[0]} in total. 
            
            Today--3months, 
                {buy_actions[1]} insiders(s) bought the stock.
                Total Shares: {buy_shares[1]} Bought.
                Total Amount: ${buy_value[1]} in total. 
                
                {sell_actions[1]} insiders(s) sold the stock.
                Total Shares: {sell_shares[1]} Sold.
                Total Amount: ${sell_value[1]} in total. 
            
            3months--6months, 
                {buy_actions[2]} insiders(s) bought the stock.
                Total Shares: {buy_shares[2]} Bought.
                Total Amount: ${buy_value[2]} in total. 
                
                {sell_actions[2]} insiders(s) sold the stock.
                Total Shares: {sell_shares[2]} Sold.
                Total Amount: ${sell_value[2]} in total. 
            
            6months--1yr, 
                {buy_actions[3]} insiders(s) bought the stock.
                Total Shares: {buy_shares[3]} Bought.
                Total Amount: ${buy_value[3]} in total. 
                
                {sell_actions[3]} insiders(s) sold the stock.
                Total Shares: {sell_shares[3]} Sold.
                Total Amount: ${sell_value[3]} in total. 
            
            1yr--2yr, 
                {buy_actions[4]} insiders(s) bought the stock.
                Total Shares: {buy_shares[4]} Bought.
                Total Amount: ${buy_value[4]} in total. 
                
                {sell_actions[4]} insiders(s) sold the stock.
                Total Shares: {sell_shares[4]} Sold.
                Total Amount: ${sell_value[4]} in total. 
            
        """
    return stats

def get_insider_stats(ticker):
    data = search_company_insider_db(ticker)  # Only for US companies, or companies under SEC authority.
    # print(data)
    stats = parse_sell_buy_stats(data)
    return stats

# Michael K Peres