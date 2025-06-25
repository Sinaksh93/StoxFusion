# run_daily.py
import yfinance as yf
import pandas as pd
import datetime, os
from nsetools import Nse

print("📌 Starting script...")

try:
    print("🔎 Fetching NSE symbols using nsetools...")
    nse = Nse()
    symbols_raw = nse.get_stock_codes()
    
    # Check if it's a dict or list
    if isinstance(symbols_raw, dict):
        tickers = [s + '.NS' for s in symbols_raw.keys() if s != 'SYMBOL']
    elif isinstance(symbols_raw, list):
        tickers = [s + '.NS' for s in symbols_raw]
    else:
        raise TypeError("⚠️ Unexpected format of stock codes returned by nsetools")

    print(f"✅ Loaded {len(tickers)} NSE symbols")

    def filter_under_200(tickers):
        print("⚙️ Filtering stocks under ₹200...")
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
            except Exception as e:
                print(f"⚠️ Failed on {sym}: {e}")
                continue
        return pd.DataFrame(rows)

    df = filter_under_200(tickers)
    df = df.sort_values(by='Volume', ascending=False)

    today = datetime.date.today().isoformat()
    file = f"under200_{today}.csv"
    df.to_csv(file, index=False)
    print(f"💾 Saved {len(df)} stocks to {file}")

    # Flag new entries
    previous = sorted([f for f in os.listdir() if f.startswith('under200_') and f != file])
    if previous:
        prev_df = pd.read_csv(previous[-1])
        prev_set = set(prev_df['Symbol'])
        df['New'] = df['Symbol'].apply(lambda x: '🚀 New!' if x not in prev_set else '')
    else:
        df['New'] = ''

    df.to_csv(file, index=False)
    print("✅ Final CSV saved with 🚀 new flags (if any)")

except Exception as e:
    print(f"❌ Script failed: {e}")
    raise
