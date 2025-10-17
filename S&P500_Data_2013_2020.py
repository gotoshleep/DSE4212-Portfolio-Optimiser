# %%
import pandas as pd

df = pd.read_csv(r'C:\Users\harry\Downloads\sp_500_historical_components.csv')

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Ensure 'tickers' is string
df['tickers'] = df['tickers'].astype(str)

# Filter date range
df = df[(df['date'] >= '2013-01-01') & (df['date'] < '2021-01-08')]

# Function to parse tickers from CSV string
def parse_ticker_list(s):
    if pd.isna(s): 
        return []
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    items = [t.strip() for t in s.split(',') if t.strip() != '']
    return items

# Apply parsing
df['ticker_list'] = df['tickers'].apply(parse_ticker_list)

# Keep only relevant columns
df = df[['date', 'ticker_list']]

df


# %%
# Extract first date of each month
df['year_month'] = df['date'].dt.to_period('M')  # e.g., 2020-01
month_starts = df.groupby('year_month')['date'].min().reset_index()
month_starts.columns = ['year_month', 'start_date']

# Loop over each month and get tickers that were present throughout the month
results = []

for i in range(len(month_starts) - 1):
    start = month_starts.loc[i, 'start_date']
    end = month_starts.loc[i + 1, 'start_date']

    # Filter rows from start to just before next month’s start
    month_df = df[(df['date'] >= start) & (df['date'] < end)]

    all_tickers = set().union(*month_df['ticker_list'])

    # Get intersection of ticker_lists in this period
    if not month_df.empty:
        surviving = set(month_df.iloc[0]['ticker_list'])
        for tickers in month_df['ticker_list']:
            surviving &= set(tickers)

        not_survived = all_tickers - surviving

        results.append({
            'date': start,
            'ticker_list': sorted(list(surviving)),
            'not_survived': sorted(list(not_survived)),
            'all tickers': len(all_tickers)
        })

# Create final tickers DataFrame
survivors_df = pd.DataFrame(results)
survivors_df['num_survivors'] = survivors_df['ticker_list'].apply(len)

# Reindex to ensure all months are present, forward-fill missing months
survivors_df['month'] = survivors_df['date'].dt.to_period('M').dt.to_timestamp()
survivors_df.set_index('month', inplace=True)
full_month_range = pd.date_range('2013-01-01', '2020-12-01', freq='MS')
survivors_df = survivors_df.reindex(full_month_range)
survivors_df.ffill(inplace=True)
survivors_df.reset_index(inplace=True)
survivors_df.rename(columns={'index': 'month'}, inplace=True)

survivors_df


# %%
# Explode the ticker_list so each row has one ticker
exploded = survivors_df.explode('ticker_list')

# Assign presence flag
exploded['value'] = 1

# Pivot the table
pivot_df = exploded.pivot_table(
    index='date',        # Each row is a month
    columns='ticker_list',
    values='value',
    fill_value=0         # If the ticker wasn't present, put 0
)

#sort columns (tickers)
pivot_df = pivot_df.sort_index(axis=1)
pivot_df = pivot_df.sort_index(axis=0)


pivot_df

# %%
summary_data = []

for ticker in pivot_df.columns:
    series = pivot_df[ticker]
    active_months = series[series == 1]

    if not active_months.empty:
        summary_data.append({
            'ticker': ticker,
            'first_seen': active_months.index.min(),
            'last_seen': active_months.index.max(),
            'months_active': active_months.count()
        })

summary_df = pd.DataFrame(summary_data)
summary_df = summary_df.sort_values('ticker').reset_index(drop=True)
summary_df['ticker'] = summary_df['ticker'].replace('FB', 'META')

summary_df

# %%
import yfinance as yf


# Ensure dates are datetime 
summary_df['first_seen'] = pd.to_datetime(summary_df['first_seen'])
summary_df['last_seen'] = pd.to_datetime(summary_df['last_seen'])

# Function to get first and last day of the month
def get_month_range(start, end):
    start_of_month = start.to_period('M').to_timestamp()       # first day of month
    end_of_month = end.to_period('M').to_timestamp('M')        # last day of month
    return start_of_month, end_of_month

# Function to fetch stock data from Yahoo Finance
def get_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(start=start_date, end=end_date + pd.Timedelta(days=1))  # Add 1 day to include end date
        stock_data['ticker'] = ticker
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# Loop through summary_df and collect stock data
stock_data_list = []
success_count = 0  # Counter for successful tickers

for idx, row in summary_df.iterrows():
    ticker = row['ticker']
    first_seen = row['first_seen']
    last_seen = row['last_seen']
    
    # Adjust to first and last day of the month
    start_date, end_date = get_month_range(first_seen, last_seen)
    
    stock_data = get_stock_data(ticker, start_date, end_date)
    
    if not stock_data.empty:
        stock_data_list.append(stock_data)
        success_count += 1  # Increment if data fetched successfully

# Combine all stock data
all_stock_data = pd.concat(stock_data_list)
all_stock_data.reset_index(inplace=True)

# Print count of tickers successfully fetched
print(f"Number of tickers successfully fetched: {success_count}")

all_stock_data


# %%
SP500_all_stock_data = all_stock_data.drop(columns=['Dividends', 'Stock Splits','Capital Gains'])

#Daily returns
SP500_all_stock_data['daily_return'] = (
    SP500_all_stock_data.groupby('ticker')['Close']
    .pct_change()
)

#Monthly returns
monthly_returns = (
    SP500_all_stock_data
    .set_index('Date')
    .groupby('ticker')['Close']
    .resample('ME')
    .ffill()             # forward-fill missing days within month
    .pct_change()        # monthly percentage change
    .reset_index(name='monthly_return')
)

SP500_all_stock_data = SP500_all_stock_data.merge(
    monthly_returns[['Date', 'ticker', 'monthly_return']],
    on=['Date', 'ticker'],
    how='left'
)

#Check index membership, if tikcer is in ticker_list for that month
SP500_all_stock_data['Date'] = SP500_all_stock_data['Date'].dt.tz_localize(None)
SP500_all_stock_data['month'] = SP500_all_stock_data['Date'].dt.to_period('M').dt.to_timestamp()


SP500_all_stock_data = SP500_all_stock_data.merge(
    survivors_df[['month', 'ticker_list']],
    on='month',
    how='left'
)

SP500_all_stock_data['membership_index'] = SP500_all_stock_data.apply(
    lambda row: row['ticker'] in row['ticker_list'],
    axis=1
)

SP500_all_stock_data

# %%
SP500_all_stock_data_Final = SP500_all_stock_data.drop(columns=['ticker_list','month'])

SP500_all_stock_data_Final


