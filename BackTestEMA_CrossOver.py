import pandas as pd

# Function to calculate EMA
def calculate_ema(data, period):
    return data.ewm(span=period, adjust=False).mean()

# Function to check crossover
def detect_crossover(data):
    data["5EMA"] = calculate_ema(data["close"], 5)
    data["20EMA"] = calculate_ema(data["close"], 20)
    if len(data) < 2:
        return None

    # Check for crossovers
    last_5ema = data["5EMA"].iloc[-2]
    last_20ema = data["20EMA"].iloc[-2]
    current_5ema = data["5EMA"].iloc[-1]
    current_20ema = data["20EMA"].iloc[-1]

    if last_5ema < last_20ema and current_5ema > current_20ema:
        return "Bullish"  # Buy CE
    elif last_5ema > last_20ema and current_5ema < current_20ema:
        return "Bearish"  # Buy PE
    return None

# Backtesting function
def backtest_strategy(historical_data):
    trade_log = []
    position = None  # Track open positions
    entry_price = 0  # Track entry price
    
    for i in range(len(historical_data)):
        counter = 0
        current_data = historical_data.iloc[:i+1]  # Simulate real-time data feed
        crossover_signal = detect_crossover(current_data)
        counter+1
        print("Counter : ",counter)
        if crossover_signal == "Bullish" and position is None:
            position = "Buy CE"
            entry_price = current_data["close"].iloc[-1]
            trade_log.append({"Timestamp": current_data.index[-1], "Signal": "Buy CE", "Price": entry_price})
        
        elif crossover_signal == "Bearish" and position is None:
            position = "Buy PE"
            entry_price = current_data["close"].iloc[-1]
            trade_log.append({"Timestamp": current_data.index[-1], "Signal": "Buy PE", "Price": entry_price})

        elif position == "Buy CE" and crossover_signal == "Bearish":
            exit_price = current_data["close"].iloc[-1]
            profit = exit_price - entry_price
            trade_log.append({"date": current_data.index[-1], "Signal": "Sell CE", "Price": exit_price, "Profit": profit})
            position = None

        elif position == "Buy PE" and crossover_signal == "Bullish":
            exit_price = current_data["close"].iloc[-1]
            profit = entry_price - exit_price
            trade_log.append({"date": current_data.index[-1], "Signal": "Sell PE", "Price": exit_price, "Profit": profit})
            position = None

    # Convert trade log to DataFrame
    trade_log_df = pd.DataFrame(trade_log)
    return trade_log_df

# Load historical data (replace 'nifty_data.csv' with your dataset)
# Ensure the file has columns: 'Timestamp' and 'Close'
historical_data = pd.read_csv("NIFTY 500_minute.csv", parse_dates=["date"], dayfirst=True)

# Run the backtest
results = backtest_strategy(historical_data)

# Save results to CSV
results.to_csv("backtest_results.csv", index=False)

print("Backtest completed. Results saved to backtest_results.csv.")
