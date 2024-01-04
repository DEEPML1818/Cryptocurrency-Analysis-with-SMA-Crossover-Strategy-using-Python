# Install necessary libraries
# You can install these libraries using: pip install pandas matplotlib requests

import pandas as pd
import matplotlib.pyplot as plt
import requests

# Function to fetch cryptocurrency data from CoinGecko API
def get_crypto_data(symbol, days):
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart'
    params = {'vs_currency': 'usd', 'days': days}
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

# Function to calculate daily returns
def calculate_daily_returns(df):
    df['daily_return'] = df['price'].pct_change()
    return df

# Function to calculate simple moving averages (SMA)
def calculate_sma(df, short_window, long_window):
    df['short_sma'] = df['price'].rolling(window=short_window, min_periods=1).mean()
    df['long_sma'] = df['price'].rolling(window=long_window, min_periods=1).mean()
    return df

# Function to generate buy/sell signals based on SMA crossover
def generate_signals(df):
    df['signal'] = 0.0
    df['signal'][df['short_sma'] > df['long_sma']] = 1.0  # Buy signal
    df['signal'][df['short_sma'] < df['long_sma']] = -1.0  # Sell signal
    return df

# Function to visualize data and trading signals
def visualize_data(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['price'], label='Cryptocurrency Price')
    plt.plot(df['short_sma'], label='Short-term SMA')
    plt.plot(df['long_sma'], label='Long-term SMA')

    # Plot buy signals
    plt.plot(df[df['signal'] == 1.0].index,
             df['short_sma'][df['signal'] == 1.0],
             '^', markersize=10, color='g', label='Buy Signal')

    # Plot sell signals
    plt.plot(df[df['signal'] == -1.0].index,
             df['short_sma'][df['signal'] == -1.0],
             'v', markersize=10, color='r', label='Sell Signal')

    plt.title('Cryptocurrency Analysis with SMA Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Main function to run the project
def main():
    # Parameters
    symbol = 'bitcoin'  # Change to your preferred cryptocurrency symbol
    days = 365  # Number of days of historical data to fetch
    short_window = 20  # Short-term SMA window
    long_window = 50  # Long-term SMA window

    # Fetch data
    crypto_data = get_crypto_data(symbol, days)

    # Calculate returns and SMAs
    crypto_data = calculate_daily_returns(crypto_data)
    crypto_data = calculate_sma(crypto_data, short_window, long_window)

    # Generate trading signals
    crypto_data = generate_signals(crypto_data)

    # Visualize data and signals
    visualize_data(crypto_data)

# Run the project
if __name__ == "__main__":
    main()