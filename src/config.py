# some example tickers we can focus on for testing
UNIVERSE = ["AAPL", "MSFT", "AMZN", "PLTR", "NVDA"]
'''
We current look at a window of 5 days (5 before, 5 after), with an estimation window of -30 to -10, can fine-tune later.
Current data backend is yfinance, can change to polygon, optionmetrics, etc later.
'''
EVENT_WINDOW   = 5        
BASELINE_START = -30      
BASELINE_END   = -10
BACKEND = "yfinance"    