# This is to help me determine whether a stock is currently a good buy [DEFENSIVE (passive) INVESTOR].
import datetime

# 700$ == 505.41£

curr_year = datetime.date.today().year
tenago_year = curr_year - 10


def continue_script():
    """Checkpoint function to see if user wants to continue calculating if stock is a good buy."""
    while True:
        user_input = input("To still continue regardless, please press [y], to stop determing press [n]:: ")
        if user_input not in ["Y", "N", "n", "y"]:
            print("Please select [y] for continue, [n] for stop.")
        else:
            if user_input.upper() == "Y":
                return True
            return False


# Defensive Investor Stock Choice.
while True:
    print("Determing if stock is a good buy.")

    # 1 Diversity
    n_comp = int(input("Please tell me the number of companies that are in your portfolio:: "))
    if not 0 <= n_comp < 30:
        print("According to Graham, you are invested into too many companies currently")
        if not continue_script():
            exit()

    # 2 Large Company
    sales_comp = int(input("Please input the value of sales company makes annualy in £ Millions:: "))
    if sales_comp < 505.41:
        print("According to Graham, a company not making at least $700 mil in yearly sales is not a good buy.")
        if not continue_script():
            exit()

    # 3 Conservatively Financed
    cur_asts = int(input("Please input the companies current value of assets in the company, in £s:: "))
    cur_labs = int(input("Please input the companies current value of liabilities in the company, in £s:: "))
    cur_rat = cur_asts / cur_labs
    if cur_rat < 2:
        print("This company is not well [consevatively] financed, and shouldnt be bought.")
        if not continue_script():
            exit()

    # 4 Dividend
    twenty_div_history = bool(
        int(input("Please enter 1 if the company has a 20 year dividend history, and 0 if it doesn't:: ")))
    if not twenty_div_history:
        print("This company does not have sufficent dividend history, so shouldnt be bought...")
        if not continue_script():
            exit()
    else:
        div_input = input("[OPTIONAL] Enter the last 20 year dividends seperated by a comma:: ")
        div_history = div_input.split(",")

    # 5 No Earnings Deficit
    no_earning_def = bool(
        int(input("Please enter 1 if the company has no earning deficit in the last 10 years, and 0 if it does:: ")))
    if not no_earning_def:
        print("This company has earning discrepencies, so shouldnt be bought...")
        if not continue_script():
            exit()
    else:
        earning_input = input("[OPTIONAL] Enter the last 20 year dividends seperated by a comma:: ")
        earning_history = earning_input.split(",")

    # 6 Earning Growth
    ten_ago_earnings = float(input(f"Enter the annual earnings of stock at year [{curr_year}]:: "))  # Current year
    curr_earnings = float(input(f"Enter the annual earnings of stock at year [{tenago_year}]:: "))  # 10 years ago
    earning_grow = ((curr_earnings / ten_ago_earnings) - 1) * 100
    if earning_grow < 33:
        print(f"This company earnings has not grown more than 33% in the last 10 years, so shouldn't be bought.")
        if not continue_script():
            exit()
    else:
        print(f"Company Growth for past 10 years: {earning_grow}%")

    # 7 Cheap Assets
    curr_price = int(input("Enter current market price per share:: "))
    tot_outstdn_shares = int(input("Enter total number of outstanding shares:: "))
    market_cap = curr_price * tot_outstdn_shares
    max_valuation = (cur_asts - cur_labs) * 1.5
    if market_cap > max_valuation:
        print(f"This stock price seems too high for its given valuation, so shouldn't be bought.")
        if not continue_script():
            exit()

    # 8 Cheap Earnings
    pe_rat = curr_price / curr_earnings
    print(f"Calculated P/E is [{pe_rat}].")
    if not bool(int(input("If this is accurate, input 1, if incorrect, input 0"))):
        pe_rat = int(input("Enter the accurate P/E ratio:: "))
    if pe_rat > 15:
        print(f"This stocks price to earnings ratio is too high, so shouldn't be bought.")
        if not continue_script():
            exit()

    print("Congrats this is a good stock to buy as a defensive investor!!")
    # You could also invest in Index Funds!! as another viable option.

# More Checks
# 9 Dividend Payout Ratio

# Michael Peres
