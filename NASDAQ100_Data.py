# %%
import nasdaq_100_ticker_history
from datetime import date, timedelta
from nasdaq_100_ticker_history import tickers_as_of
import pandas as pd

# Define date range
start_date = date(2015, 1, 1)
end_date = date(2020, 12, 31)

records = []
current = start_date

while current <= end_date:
    try:
        tickers = tickers_as_of(current.year, current.month, current.day)
        # Keep tickers as a list
        records.append({
            "date": current,
            "tickers": sorted(list(tickers))  # <-- list of tickers
        })
    except Exception as e:
        print(f"Error on {current}: {e}")
    current += timedelta(days=1)

# Convert to DataFrame
df_nasdaq100 = pd.DataFrame(records)

# Display first few rows
print(df_nasdaq100)
print(f"\n Collected {len(df_nasdaq100)} days of NASDAQ-100 data with tickers as lists.")



# %%
# Step 1: Explode the 'tickers' list so each row is a (date, ticker) pair
exploded = df_nasdaq100.explode('tickers')

# Step 2: Add a presence indicator
exploded['value'] = 1

# Step 3: Pivot to get the presence matrix
presence_matrix = exploded.pivot_table(
    index='date',           # rows = daily dates
    columns='tickers',      # columns = ticker symbols
    values='value',
    fill_value=0            # fill with 0 if ticker not present
)

# Optional: sort rows and columns
presence_matrix = presence_matrix.sort_index(axis=0)  # sort by date
presence_matrix = presence_matrix.sort_index(axis=1)  # sort by ticker

# Show the result
print(presence_matrix)



# %%
summary_data = []

for ticker in presence_matrix.columns:
    series = presence_matrix[ticker]
    active_periods = series[series == 1]

    if not active_periods.empty:
        summary_data.append({
            'ticker': ticker,
            'first_seen': active_periods.index.min(),
            'last_seen': active_periods.index.max(),
            'days_active': active_periods.count()
        })

# Convert to DataFrame
summary_df = pd.DataFrame(summary_data)

# Optional: sort alphabetically
summary_df = summary_df.sort_values('ticker').reset_index(drop=True)

print(summary_df)


# %%
import yfinance as yf
import pandas as pd

# Ensure dates are datetime just in case
summary_df['first_seen'] = pd.to_datetime(summary_df['first_seen'])
summary_df['last_seen'] = pd.to_datetime(summary_df['last_seen'])

# Function to fetch stock data from Yahoo Finance
def fetch_yfinance_data(stock_symbol, start_dt, end_dt):
    try:
        ticker_obj = yf.Ticker(stock_symbol)
        stock_hist = ticker_obj.history(start=start_dt, end=end_dt + pd.Timedelta(days=1))  # include end date
        stock_hist['ticker'] = stock_symbol
        return stock_hist
    except Exception as e:
        print(f"Error fetching data for {stock_symbol}: {e}")
        return pd.DataFrame()

# Collect stock data for all tickers based on exact daily first and last seen
collected_stock_data = []

for idx, record in summary_df.iterrows():
    stock_ticker = record['ticker']
    start_date = record['first_seen']
    end_date = record['last_seen']
    
    stock_hist = fetch_yfinance_data(stock_ticker, start_date, end_date)
    
    if not stock_hist.empty:
        collected_stock_data.append(stock_hist)

# Combine all into one DataFrame
combined_stock_data = pd.concat(collected_stock_data)
combined_stock_data.reset_index(inplace=True)

print(combined_stock_data.head())


# %%
combined_stock_data[combined_stock_data['ticker'] == 'GMCR']

# %%
combined_stock_data


# %%



