from scipy import stats
import statsmodels.formula.api as smf

def t_test_mean(abn_matrix):
    """
    abn_matrix: DataFrame where index=event_day, columns=tickers.
    Returns series of t-statistics for each relative day.
    """
    return abn_matrix.apply(lambda col: stats.ttest_1samp(col.dropna(), 0).statistic,
                            axis=1)

def cross_section_reg(df):
    """
    df needs columns abn_iv, surprise, pre_iv
    """
    mod = smf.ols("abn_iv ~ surprise + pre_iv", data=df).fit()
    return mod
