import yfinance as yf
import pandas as pd
from tqdm import tqdm

def fetch_earnings_calendar(ticker):
    t = yf.Ticker(ticker)
    cal = t.get_earnings_dates(limit=40) #current limit set to 40, can change later
    cal = cal.reset_index()                              # turn index into col 0

    # robust column map in case yfinance changes labels slightly
    rename_map = {
        cal.columns[0]: "date",                          # former index
        "Reported EPS": "epsactual",
        "EPS Estimate": "epsestimate",
        "Surprise(%)": "surprise",
        "Surprise %": "surprise",                        # alt label in some versions
    }
    cal = cal.rename(columns=rename_map)

    # standardise dtypes
    cal["date"] = pd.to_datetime(cal["date"].dt.date)    # keep calendar date only
    cal["epsactual"]   = pd.to_numeric(cal["epsactual"], errors="coerce")
    cal["epsestimate"] = pd.to_numeric(cal["epsestimate"], errors="coerce")
    cal["surprise"]    = pd.to_numeric(cal["surprise"], errors="coerce")

    return cal[["date", "epsactual", "epsestimate", "surprise"]]\
             .sort_values("date", ascending=False)       # newest first

def fetch_price_series(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=False)["Adj Close"]
    return df