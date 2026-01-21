import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

def calculate_returns(df):
    
    df = df.copy()
    
    if isinstance(df['Close'], pd.DataFrame):
        price = df['Close'].mean(axis=1)
    else:
        price = df['Close']
    
    df['Returns_Simple'] = price.pct_change()
    
    df['Returns_Log'] = np.log(1 + df['Returns_Simple'])
    
    df['Cumulative_Returns'] = (1 + df['Returns_Simple']).cumprod() - 1
    
    return df

def add_technical_indicators(df):
    
    df = df.copy()
    
    if isinstance(df['Close'], pd.DataFrame):
        price = df['Close'].mean(axis=1)
    else:
        price = df['Close']
    
    df['SMA_20'] = price.rolling(window=20).mean()
    df['SMA_50'] = price.rolling(window=50).mean()
    
    delta = price.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['EMA_12'] = price.ewm(span=12, adjust=False).mean()
    df['EMA_26'] = price.ewm(span=26, adjust=False).mean()
    
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    
    df['BB_Middle'] = df['SMA_20']
    std_20 = price.rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + 2 * std_20
    df['BB_Lower'] = df['BB_Middle'] - 2 * std_20
    
    df['Portfolio_Close'] = price
    
    return df

def get_statistics(df):
    
    returns = df['Returns_Log'].dropna()
    
    return {
        
        "Volatilité Annuelle": returns.std() * np.sqrt(252),
        "Skewness": returns.skew(),
        "Kurtosis": returns.kurtosis(),
        
        "Moyenne": returns.mean(),
        "Médiane": returns.median(),
        "Écart-type": returns.std(),
        "Maximum": returns.max(),
        "Minimum": returns.min(),
        
        "Percentile_5": returns.quantile(0.05),
        "Percentile_25": returns.quantile(0.25),
        "Percentile_75": returns.quantile(0.75),
        "Percentile_95": returns.quantile(0.95)
    }

def test_normality(df):
    
    returns = df['Returns_Log'].dropna()
    return stats.shapiro(returns)[1]

def calculate_sharpe_ratio(df, risk_free_rate=0.0):
    
    returns = df['Strategy_Returns'].dropna()
    
    if len(returns) == 0:
        return 0.0
    
    excess_returns = returns - risk_free_rate / 252  
    sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
    
    return sharpe

def calculate_win_rate(df):
    
    strategy_returns = df['Strategy_Returns'].dropna()
    
    if len(strategy_returns) == 0:
        return 0.0
    
    winning_trades = (strategy_returns > 0).sum()
    total_trades = len(strategy_returns[strategy_returns != 0])
    
    if total_trades == 0:
        return 0.0
    
    return winning_trades / total_trades

def run_backtesting(df, initial_capital, strategy_type, transaction_fee=0.001):
    
    df = df.copy()
    
    if isinstance(df['Close'], pd.DataFrame):
        price = (1 + df['Close'].pct_change().mean(axis=1)).cumprod() * 100
    else:
        price = df['Close']

    df['Signal'] = 0.0
    if strategy_type == "SMA Crossover (Trend)":
        sma_20 = price.rolling(window=20).mean()
        sma_50 = price.rolling(window=50).mean()
        df.loc[sma_20 > sma_50, 'Signal'] = 1.0
    elif strategy_type == "RSI Mean Reversion":
        delta = price.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df.loc[df['RSI'] < 30, 'Signal'] = 1.0
        df.loc[df['RSI'] > 70, 'Signal'] = 0.0
        df['Signal'] = df['Signal'].ffill().fillna(0)
    else:  # Buy & Hold
        df['Signal'] = 1.0

    df['Pct_Change'] = price.pct_change()
    df['Trade_Action'] = df['Signal'].diff()
    
    df['Transaction_Cost'] = 0.0
    df.loc[df['Trade_Action'] != 0, 'Transaction_Cost'] = transaction_fee
    
    df['Strategy_Returns'] = df['Signal'].shift(1) * df['Pct_Change'] - df['Transaction_Cost']
    df['Equity_Curve'] = initial_capital * (1 + df['Strategy_Returns'].fillna(0)).cumprod()
    
    roll_max = df['Equity_Curve'].cummax()
    drawdown = (df['Equity_Curve'] - roll_max) / roll_max
    max_drawdown = abs(drawdown.min())

    gains = df.loc[df['Strategy_Returns'] > 0, 'Strategy_Returns'].sum()
    pertes = abs(df.loc[df['Strategy_Returns'] < 0, 'Strategy_Returns'].sum())
    profit_factor = gains / pertes if pertes > 0 else 1.0

    num_trades = int(df['Signal'].diff().abs().sum() / 2)
    if num_trades == 0 and df['Signal'].iloc[0] == 1:
        num_trades = 1
    
    total_return = (df['Equity_Curve'].iloc[-1] - initial_capital) / initial_capital
    
    sharpe_ratio = calculate_sharpe_ratio(df)
    win_rate = calculate_win_rate(df)
    
    if strategy_type == "Buy & Hold":
        df.iloc[0, df.columns.get_loc('Trade_Action')] = 1.0

    journal = df[df['Trade_Action'] != 0].copy()

    if not journal.empty:
        journal['Action'] = journal['Trade_Action'].apply(lambda x: "🟢 ACHAT" if x > 0 else "🔴 VENTE")
        journal['Prix_Execution'] = price
        journal['Frais'] = journal['Transaction_Cost'] * journal['Equity_Curve'].shift(1)
        journal['Cumulative_Returns'] = (journal['Equity_Curve'] - initial_capital) / initial_capital
    else:
        journal = pd.DataFrame(columns=['Action', 'Prix_Execution', 'Frais', 'Cumulative_Returns'])

    return df, total_return, max_drawdown, num_trades, profit_factor, sharpe_ratio, win_rate, journal

def calculate_correlation_matrix(symbols_data):
    
    returns_df = pd.DataFrame()
    
    for symbol, data in symbols_data.items():
        returns_df[symbol] = data['Returns_Log']
    
    return returns_df.corr()

def plot_pro_analysis(df):
    
    high_idx = df['High'].idxmax()
    low_idx = df['Low'].idxmin()
    high_val = df['High'].max()
    low_val = df['Low'].min()
    diff = high_val - low_val

    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close'], name='Prix'
    )])

    levels = [0, 0.236, 0.382, 0.5, 0.618, 1]
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    
    for level, color in zip(levels, colors):
        price = high_val - (level * diff)
        fig.add_hline(y=price, line_dash="dash", line_color=color, 
                      annotation_text=f"Fib {level*100}%", annotation_position="bottom right")

    fig.update_layout(title="Analyse Expert: Elliott + Fibonacci + Candlesticks", template="plotly_dark")
    return fig


