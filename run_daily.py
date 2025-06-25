# run_daily.py
import yfinance as yf
import pandas as pd
import datetime, os
from nsetools import Nse

# Fetch all NSE tickers dynamically
nse = Nse()
symbols = nse.get_stock_codes()
tickers = [s + '.NS' for s in symbols.keys() if s != 'SYMBOL']
print(f"✅ Loaded {len(tickers)} NSE symbols")

# Filter for stocks under ₹200
def filter_under_200(tickers):
    rows = []
    for sym in tickers:
        try:
            info = yf.Ticker(sym).info
            price = info.get('regularMarketPrice')
            volume = info.get('volume') or 0
            mcap = info.get('marketCap') or 0
            name = info.get('shortName', sym)
            if price and price < 200:
                rows.append({'Name': name, 'Symbol': sym,
                             'Price': price, 'Volume': volume,
                             'MarketCap': mcap})
        except Exception:
            continue
    return pd.DataFrame(rows)

print("📊 Fetching live stock data…")
df = filter_under_200(tickers)

# Sort by volume and save
df = df.sort_values(by='Volume', ascending=False)
today = datetime.date.today().isoformat()
file = f"under200_{today}.csv"
df.to_csv(file, index=False)

# Flag new entries
previous = sorted([f for f in os.listdir() if f.startswith('under200_') and f != file])
if previous:
    prev_df = pd.read_csv(previous[-1])
    prev_set = set(prev_df['Symbol'])
    df['New'] = df['Symbol'].apply(lambda x: '🚀 New!' if x not in prev_set else '')
else:
    df['New'] = ''
df.to_csv(file, index=False)
print(f"✅ Saved {len(df)} under ₹200 stocks to {file}")
