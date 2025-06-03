from tqdm import tqdm
import pandas as pd
from fetch import fetch_earnings_calendar
from event_study import abnormal_iv_series
from viz import plot_avg_abn, heatmap_tstats
from stats import t_test_mean
from config import UNIVERSE

abn_iv_matrix = {}

for tkr in UNIVERSE:
    cal = fetch_earnings_calendar(tkr)
    # loop over past N earnings events; append each to abn_iv_matrix
    for dt, eps, est, surprise in cal.head(8).itertuples(index=False):
        s = abnormal_iv_series(tkr, dt)
        abn_iv_matrix[(tkr, dt)] = s

abn_df = pd.concat(abn_iv_matrix, axis=1)
plot_avg_abn(abn_df)

tstats = t_test_mean(abn_df)
heatmap_tstats(tstats)