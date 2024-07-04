import pandas as pd
import numpy as np

def backtest(data: pd.DataFrame, signals: pd.Series, initial_capital: float = 10000.0) -> dict:
    """Perform backtesting of a trading strategy."""
    # Create a DataFrame with positions and portfolio value
    positions = signals.shift(1)
    portfolio = pd.DataFrame(index=data.index)
    portfolio['positions'] = positions * data['Close']
    portfolio['cash'] = initial_capital - (positions.diff() * data['Close']).cumsum()
    portfolio['total'] = portfolio['positions'] + portfolio['cash']
    portfolio['returns'] = portfolio['total'].pct_change()

    # Calculate performance metrics
    total_return = (portfolio['total'].iloc[-1] - initial_capital) / initial_capital
    sharpe_ratio = np.sqrt(252) * portfolio['returns'].mean() / portfolio['returns'].std()
    
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'equity_curve': portfolio['total']
    }