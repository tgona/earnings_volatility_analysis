import pandas as pd
from .config import EVENT_WINDOW, BASELINE_START, BASELINE_END
from .vol import get_chain_yf, atm_iv
from .io import fetch_price_series

def abnormal_iv_series(ticker, announce_date):
    """Returns a Series indexed by day_in_event_window (−5,…,+5)."""
    # pull spot prices & option chain for each day
    window = pd.date_range(announce_date + pd.Timedelta(BASELINE_START, "D"),
                           announce_date + pd.Timedelta(EVENT_WINDOW, "D"),
                           freq="B")
    ivs = []
    for d in window:
        # skip if market closed
        try:
            spot = fetch_price_series(ticker, d, d + pd.Timedelta(1, "D")).iloc[0]
        except IndexError:
            continue
        chain = get_chain_yf(ticker, d.strftime("%Y-%m-%d"))
        ivs.append({"d": d, "iv": atm_iv(chain, spot)})
    iv_df = pd.DataFrame(ivs).set_index("d")

    # baseline mean
    baseline = iv_df.loc[
        announce_date + pd.Timedelta(BASELINE_START, "D"):
        announce_date + pd.Timedelta(BASELINE_END, "D")
    ]["iv"].mean()
    
    iv_df["abn_iv"] = iv_df["iv"] - baseline
    iv_df["event_day"] = (iv_df.index - announce_date).days
    return iv_df.set_index("event_day")["abn_iv"]
