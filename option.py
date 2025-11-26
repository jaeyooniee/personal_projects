# Title: Call Option Strike Optimizer
# Details: Find the most profitable call option strike based on expected stock price. 
# Details: This includes automatic budget allocation and comparison with direct stock investing.

print("------------------Finding the best options possible!!------------------\n")

ticker = input("What is the ticker of the stock/index?: ")
current_price = float(input(f"What is the current price of {ticker}?: "))
budget = float(input("How much are you considering to invest in? ($USD): "))
stock_amount = int(budget/current_price)

print("\nPlease type in the Strike Price($) and Ask Price($)")
print("*If you want to stop typing in the prices, input '-1'...\n")

call_option_info = []
option_amount = []

while True:
    x = list(map(float, input().split()))

    if len(x) == 1 and x[0] == -1:
        break

    call_option_info.append(x)
    option_amount.append(int(budget/x[-1]))

expected_price = float(input(f"\nWhat is the expected price of {ticker}? ($USD): "))

net_profit = []
info_length = len(call_option_info)

for i in range(info_length):
    profit = max(expected_price-call_option_info[i][0]-call_option_info[i][-1], 0) * option_amount[i]
    net_profit.append(profit)

max_profit = max(net_profit)

print("------------------RESULTS------------------\n")

return_investment = (expected_price-current_price)*stock_amount

print(f"If you have directly invested in {ticker}, the profit/loss is: ${return_investment:.1f}.")
print(f"The Maximum Profit from the investment is ${max_profit:.1f}.\n")

for i in range(info_length):
    if net_profit[i] == max_profit:
        print(f"Strike Price: ${call_option_info[i][0]:.1f}")

print("\n-------------------Comments-------------------\n")

if return_investment > max_profit:
    print(f"""By Directly Investing in {ticker} would make ${return_investment:.1f}\nBy Investing in Call Option would make ${max_profit}\n
        Therfore, it is wise to directly invest in {ticker}.
""")

elif return_investment < max_profit:
    print(f"""By Investing in Call Option would make ${max_profit:.1f}\nBy Directly Investing in {ticker} would make ${return_investment}\n
Therfore, it is wise to invest in call option of {ticker}.
""")
    
else:
    print(f"It will either get you same maximum profit, however, it is wise to consider investing directly in {ticker} in this case.")