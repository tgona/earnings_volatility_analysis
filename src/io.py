import yfinance as yf
import pandas as pd
from tqdm import tqdm

def fetch_earnings_calendar(ticker):
    t = yf.Ticker(ticker)
    cal = t.get_earnings_dates(limit=40) #current limit set to 40, can change later
    cal = cal.reset_index().rename(columns={"index": "date"})

    print(f"Columns after reset_index for {ticker}: {cal.columns}")
    cal = cal.rename(columns={cal.columns[0]: "date"}) 
    
    cal["date"] = pd.to_datetime(cal["date"].dt.date)
    return cal[["date", "epsactual", "epsestimate", "surprise"]]

def fetch_price_series(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=False)["Adj Close"]
    return df