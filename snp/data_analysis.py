import yfinance as yf
import pandas as pd

def load_data(start_date, end_date):
    TICKERS = {
        "S&P500": "^GSPC",
        "S&P100": "^OEX",
    }
    
    raw = {}

    for label, ticker in TICKERS.items():
        s = yf.download(ticker, start=start_date, end=end_date, interval="1d", progress=False)["Close"]
        s.name = label
        raw[label] = s

    prices = pd.concat(raw.values(), axis=1).dropna()
    prices.columns = list(TICKERS.keys())
    return prices


def simple_return(prices, start_date, end_date):
    price_data = prices.loc[start_date:end_date].dropna()

    def simple_formula(df):
        return (df.iloc[-1] - df.iloc[0]) / df.iloc[0] * 100

    print("------------------------------")
    print(f"RETURN {start_date} ~ {end_date}:\n")

    simple_price_data = simple_formula(price_data)

    for index, value in simple_price_data.items():
        print(f"{index}: {value:.2f}%")

    print("\n------------------------------")

    return simple_price_data 

def sharpe_ratio(price_series):
    returns = price_series.pct_change().dropna()
    mean_return = returns.mean()
    volatility = returns.std()

    if volatility == 0:
        return None

    sharpe = (mean_return / volatility) * (252 ** 0.5)

    return sharpe
