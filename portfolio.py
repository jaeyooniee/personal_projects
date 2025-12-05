import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime

# 1. Portfolio and Benchmark Tickers
stock_ticker = ["000660.KS", "015760.KS", "278470.KS", "ARKG", "SGOV", "OKLO", "IONQ", "RKLB"]
benchmark_ticker = "OEF" # The reason I chose to use S&P100 over S&P500 - https://github.com/jaeyooniee/personal_projects/tree/snp-analysis

# 2. Investment Amounts (KRW for Korean, USD for U.S.)
investment_KRW = np.array([500000, 2000000, 2000000]) 
investment_USD = np.array([300, 3000, 500, 300, 500])

# 3. Download Close Prices
start_date = "2010-01-01"
end_date = datetime.datetime.today().strftime("%Y-%m-%d")

data = yf.download(stock_ticker + [benchmark_ticker], start=start_date, end=end_date, auto_adjust=False)["Close"]
data = data.dropna()

# 4. Get FX Rate (KRW=X → USD/KRW 환율)
fx = yf.download("KRW=X", start=start_date, end=end_date, auto_adjust=False)["Close"]
fx = fx.reindex(data.index, method="ffill")  # 날짜 정렬

# 5. Convert KRW investments to USD
current_fx = fx.iloc[0].item()
investment_KRW_to_USD = investment_KRW / current_fx

# 6. Combine weights (USD 기준)
investment_total_USD = np.concatenate([investment_KRW_to_USD, investment_USD])
weights = investment_total_USD / investment_total_USD.sum()

# Stock names
stock_names = []
for t in stock_ticker:
    info = yf.Ticker(t).info
    stock_names.append(info.get("longName", t))

# Sorted Output
sorted_portfolio = sorted(zip(stock_names, weights), key=lambda x: x[1], reverse=True)

print("\nPortfolio Weights (High → Low):")
for name, weight in sorted_portfolio:
    print(f"{name}: {weight * 100:.2f}%")

# 7. Returns
returns = data.pct_change().dropna()
portfolio_returns = returns[stock_ticker].dot(weights)

# Benchmark returns
benchmark_returns = returns[benchmark_ticker]

# 8. Sharpe Ratio
risk_free_rate = 0.05 / 252
excess_portfolio = portfolio_returns - risk_free_rate
excess_benchmark = benchmark_returns - risk_free_rate

sharpe_portfolio = (excess_portfolio.mean() / excess_portfolio.std()) * np.sqrt(252)
sharpe_benchmark = (excess_benchmark.mean() / excess_benchmark.std()) * np.sqrt(252)

print("\nSharpe Ratio (Portfolio USD):", sharpe_portfolio)
print("Sharpe Ratio (OEF - S&P100 ETF):", sharpe_benchmark)

# 9. Cumulative Return Graph Compare
cumulative_portfolio = (1 + portfolio_returns).cumprod() - 1
cumulative_benchmark = (1 + benchmark_returns).cumprod() - 1

cumulative_portfolio.iloc[0] = 0
cumulative_benchmark.iloc[0] = 0

plt.figure(figsize=(11,5))
plt.plot(cumulative_portfolio * 100, label="My Portfolio Return (%)", linewidth=2)
plt.plot(cumulative_benchmark * 100, label="OEF (S&P500 ETF) Return (%)", linewidth=2)
plt.title("Portfolio vs S&P500 ETF (OEF) - Cumulative Return (%)")
plt.xlabel("Date")
plt.ylabel("Return (%)")
plt.legend()
plt.grid(True)
plt.show()
