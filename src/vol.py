from datetime import timedelta
import py_vollib.black_scholes.implied_volatility as iv
import numpy as np

def get_chain_yf(ticker, as_of):
    """
    Returns option chain DataFrame for the given trade date.
    yfinance chain contains an 'impliedVolatility' column already;
    if the swapped backend doesn't, we invert Black-Scholes here.
    """
    t = yf.Ticker(ticker)
    chain = []
    for exp in t.options:
        opt = t.option_chain(exp)
        opt.calls["type"] = "call"
        opt.puts["type"] = "put"
        tmp = pd.concat([opt.calls, opt.puts])
        tmp["expiration"] = pd.to_datetime(exp)
        chain.append(tmp)
    chain = pd.concat(chain)
    chain["quote_date"] = as_of
    return chain

def atm_iv(chain, spot):
    """returns the front-month at-the-money Implied Vol (mid of C/P)."""
    front = chain.sort_values("expiration").groupby("type").first().reset_index()
    # choose strike nearest to spot
    idx = (front["strike"] - spot).abs().idxmin()
    return front.loc[idx, "impliedVolatility"]
