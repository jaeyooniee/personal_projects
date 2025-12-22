
#Compare rolling win rates of S&P 100 vs S&P 500 (Custom Day Window and Step)

"""
Program results:

start_date     end_date
1995-01-01 -> 1999-12-31 (window_days=365, step_days=7): win_rate=34/52 (65.38%) - Dotcom Bubble
2000-01-01 -> 2004-12-31 (window_days=365, step_days=7): win_rate=17/52 (32.69%)
2005-01-01 -> 2009-12-31 (window_days=365, step_days=7): win_rate=17/52 (32.69%) - Bearish market
2010-01-01 -> 2014-12-31 (window_days=365, step_days=7): win_rate=23/52 (44.23%)
2015-01-01 -> 2019-12-31 (window_days=365, step_days=7): win_rate=28/52 (53.85%)
2020-01-01 -> 2024-12-31 (window_days=365, step_days=7): win_rate=34/52 (65.38%) - AI bubble(?)


Personal Research:

- From 1995-1999, the annual return from investing S&P500 index was 34.11%, 20.26%, 31.01%, 26.67% and 19.53%.
These numbers can be considered as decent returns when it comes to market indices. Markets in 1995-1999 were actually 
amazingly bullish. 

- In mid to late 1990s, traditional industries such as energy, finance, industrials and consumer goods had a large presence. 
Technology stocks existed but were not yet dominant. (e.g. Exxon Mobil, Coca-cola, General Electric, Merck, P&G and so on)

- There were also changes in the number of companies per sector and shifts in sector leadership between 1995-1999.

- Technology now occupies a far larger share of the index than it did in the past.
In the early 2000s, IT accounted for about 20-25% of the index, whereas today its share and concentration among 
top companies are significantly higher (currently 35%).

- In the past, companies tended to remain in the index for decades. 
Today, due to technological disruption, M&A, and slower growth, turnover is much more frequent.

- In 1995, S&P 500 sector weights were fairly balanced: 
The largest sector (Consumer Discretionary) had ~15% and The smallest (Utilities) had ~5%.

- Today, sector distribution has become much more uneven:
IT services now dominates with ~25% and Telecommunications has fallen to around 2%.

- This represents a systematic and steady shift over the past few decades, 
where market capitalization has become concentrated in fewer, dominant sectors, especially Financials and IT.

- Actually, this concentration brings back 2000 (the Dotcom bubble), when tech valuations similarly dominated the index.

- The index these days is far more concentrated than in 1995, with only a few sectors driving the majority of total returns.

- Today's S&P 500 is not a broadly diversified representation of the economy, 
but rather heavily dependent on a few sectors and mega-cap firms.

source: https://www.tfginvest.com/insights/the-impact-of-the-sp-tech-industry-concentration
source: https://einvestingforbeginners.com/historical-sp-500-industry-weights-20-years


Q1. What kind of companies led S&P100 to outperform S&P500? 
A1. In 5 years time gap, it was 1995-1999 and 2020-2024 when S&P100 index beated S&P500 index. 
Those moments continued due to widely known 'Dotcom Bubble' at 2000 and huge AI investment from big techs which is still 
an ongoing event. When we list the firms that led the stock market at the moment, there are Microsoft, General Electric, Intel, 
Cisco Systems, IBM, Exxon Mobil from 1995 to 1999 and Apple, Microsoft (again), Amazon, Alphabet, NVIDIA, Meta, Broadcom from 
2020 ~. The results indicates that TECH COMPANIES were always with the market when the bubble was getting (seemingly) endlessly big
and these few tech firms eventually affected the increase of the market indices to a meaningful extent.


Q2. Why did this happen? What's the similarity between 1995-2000 and 2020-2025?
A2. As mentioned above, both the late 1990s and early 2020s experienced powerful bull markets driven by 
technological revolutions and abundant liquidity. During 1995-2000, optimism around the Internet and personal computing 
fueled soaring valuations, while from 2020-2025, the rise of artificial intelligence, cloud computing, and semiconductors 
produced a similar surge in investor enthusiasm. In both periods, easy monetary policy and cheap capital encouraged speculation, 
leading to extreme market concentration where a handful of dominant firms drove most of the index's returns.
Investor psychology also played a key role, as widespread belief in a “new era” of growth created momentum-driven rallies 
detached from fundamentals. Ultimately, both eras illustrate how technological transformation
can reshape market structures and make the S&P 500 heavily reliant on just a few mega-cap companies.



Q3. As long as IT and Computing industries develops, will this trend last forever?
A3. The answer is no. There have been numerous shifts all over the world for few centuries (Agriculture -> Mechanics -> 
Energy -> Hardware & Software -> Artificial Intelligence & Robotics -> ?) and a number of expectation in few decades contain 
different aspects in which the leading industry will take human beings to next level. Getting rid of former machines and
technologies makes no sense, however, it'll likely to be disappear by itself or hardly be used in future according to human history 
of revolution so far. Human will find an answer to improve the possible downsides of current technologies and open a new era.


"""

"""
Update 21/12/2025 - Added Sharpe Ratio Analysis

I found that from 2020-01-01 to 2024-12-31, the sharpe ratio of S&P100 was 0.75 and that of S&P500 was 0.67.
This means that not even the returns of S&P100 outperformed the 'famous' index S&P500, also in terms of volatility or liquidity,
S&P100 was doing better. The result supports my argument that S&P100 is more efficient index to invest than S&P500 over time.

"""
# the code starts here

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data_analysis import load_data, simple_return, sharpe_ratio
import matplotlib.dates as mdates

def main():
    print("Welcome all! Let's figure out when and how many times S&P100 outperformed S&P500!")
    print("**********************************************************************************\n")

    start_input = input("Enter start date (YYYY-MM-DD): ")
    end_input = input("Enter end date (YYYY-MM-DD): ")

    window_days = int(input("Enter window size in DAYS: "))
    step_days = int(input("Enter step size in DAYS: "))

    start_date_obj = datetime.strptime(start_input, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_input, "%Y-%m-%d")

    results = []

    prices = load_data(start_input, end_input)

    current_start = start_date_obj

    while current_start + timedelta(days=window_days) <= end_date_obj:
        start_date = current_start.strftime("%Y-%m-%d")
        end_date = (current_start + timedelta(days=window_days)).strftime("%Y-%m-%d")

        print(start_date + "->" + end_date)

        delta = timedelta(days=step_days)
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end_limit = datetime.strptime(end_date, "%Y-%m-%d")

        step_results = []

        while start + delta <= end_limit:
            s = start.strftime("%Y-%m-%d")
            e = (start + delta).strftime("%Y-%m-%d")

            returns = simple_return(prices, s, e)

            if returns is None or len(returns) == 0:
                start += timedelta(days=step_days)
                continue

            if "S&P100" in returns.index and "S&P500" in returns.index:
                snp100 = returns["S&P100"]
                snp500 = returns["S&P500"]
                winner = "S&P100" if snp100 > snp500 else "S&P500"
                step_results.append(winner)

            start += timedelta(days=step_days)

        total = len(step_results)
        wins = step_results.count("S&P100")
        win_rate = (wins/total * 100) if total > 0 else 0

        results.append({
            "Start Date": current_start,
            "End Date": datetime.strptime(end_date, "%Y-%m-%d"),
            "Total Windows": total,
            "S&P100 Wins": wins,
            "Win Rate (%)": round(win_rate, 2)
        })

        current_start += timedelta(days=step_days)

    df = pd.DataFrame(results)
    print("\n===============================")
    print(f"{window_days}-Day Rolling Comparison Results ({step_days}-Day Steps)")
    print(df.to_string(index=False))
    print("===============================")

    print(f"S&P100 wins: {wins}/{total} ({win_rate:.2f}%)")

    sharpe_snp100 = sharpe_ratio(prices["S&P100"])
    sharpe_snp500 = sharpe_ratio(prices["S&P500"])

    print(f"\nSharpe Ratio: S&P100 - {sharpe_snp100:.2f}, S&P500 - {sharpe_snp500:.2f}")

    plt.figure(figsize=(12, 6))
    plt.plot(
        df["Start Date"],
        df["Win Rate (%)"],
        linewidth=1.0,
        color="blue",   
        alpha=0.9
    )

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    plt.title(f"S&P 100 Win Rate ({window_days}-Day Window, {step_days}-Day Step)", fontsize=15, pad=20)
    plt.xlabel("Year", fontsize=13)
    plt.ylabel("Win Rate (%)", fontsize=13)

    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()

    plt.style.use("seaborn-v0_8-whitegrid")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.show()


if __name__ == "__main__":
    main()
