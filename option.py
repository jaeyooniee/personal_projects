# Title: Call Option Strike Optimizer
# Details: Find the most profitable call option strike based on expected stock price. 
# Details: This includes automatic budget allocation and comparison with direct stock investing.

import csv
import os
import datetime

print("------------------Finding the best options possible!!------------------\n")

while True:

    ticker = input("What is the ticker of the stock/index?: ")
    current_price = float(input(f"What is the current price of {ticker}? ($USD): "))
    budget = float(input("How much are you considering to invest in? ($USD): "))
    stock_amount = int(budget/current_price)

    file_path = input("\nEnter the CSV file name for options data: ")
    file_name = os.path.basename(file_path)

    idx = file_name.index('-exp-')
    maturity_date = file_name[idx+5:idx+15]

    print(f"\nThe Expiring Date is {maturity_date}.")

    call_option_info = []
    contracts_amount = []

    with open(file_path, "r") as f: # Download option data file from Barchart.com
        reader = csv.DictReader(f)

        for row in reader:
            if not row["Strike"][0].isdigit():
                continue

            strike = float(row['Strike'])
            ask = float(row['Ask'])
            types = row['Type']

            if types == 'Put':
                continue

            else:
                call_option_info.append([strike, ask])
                contracts_amount.append(budget // (ask*100)) # how many option contracts is the user buying

    expected_price = float(input(f"\nWhat is the expected price of {ticker}? ($USD): "))

    net_profit = []
    info_length = len(call_option_info)

    for i in range(info_length):
        intrinsic = max(expected_price-call_option_info[i][0], 0) * 100
        cost = call_option_info[i][1] * 100

        net_profit.append((intrinsic-cost) * contracts_amount[i]) 

    max_profit = max(net_profit)

    print("\n------------------RESULTS------------------\n")

    return_investment = (expected_price-current_price)*stock_amount

    print(f"If you have directly invested in {ticker}, the profit/loss is: ${return_investment:.1f}.")
    print(f"The Maximum Profit from the investment is ${max_profit:.1f}.\n")

    for i in range(info_length):
        if net_profit[i] == max_profit:
            print(f"Best Strike Price: ${call_option_info[i][0]:.1f}!!")

    print("\n-------------------Comments-------------------\n")

    if return_investment > max_profit:
        print(f"""By Directly Investing in {ticker} would make ${return_investment:.1f}\nBy Investing in Call Option would make ${max_profit}\n
            Therfore, it is wise to directly invest in {ticker}.
    """)

    elif return_investment < max_profit:
        print(f"""By Investing in Call Option would make ${max_profit:.1f}\nBy Directly Investing in {ticker} would make ${return_investment}
Therfore, it is wise to invest in call option of {ticker}.
    """)
        
    else:
        print(f"It will either get you same maximum profit, however, it is wise to consider investing directly in {ticker} in this case.")

    while True:
        is_end = False
        n = int(input("\nIf you want to see more information of the results. Choose functions:\n 1. See every option result\n 2. Go through other stock/index\n 3. End program\nPlease enter a number: "))
        print()

        if n == 1:
            print("Strike  Returns")
            for i in range(info_length):
                print(f"${call_option_info[i][0]:.1f}  ${net_profit[i]:.1f}")

        elif n == 2:
            print()
            break

        else:
            print("Ending Program...\n")
            is_end = True
            break

    if is_end:
        break