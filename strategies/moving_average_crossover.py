import pandas as pd

class MovingAverageCrossover:
    def __init__(self, data: pd.DataFrame, short_window: int, long_window: int):
        self.data = data
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self) -> pd.Series:
        """Generate buy/sell signals based on SMA crossover."""
        signals = pd.Series(index=self.data.index, dtype=int)
        signals[:] = 0

        # Calculate short and long term moving averages
        short_ma = self.data['Close'].rolling(window=self.short_window).mean()
        long_ma = self.data['Close'].rolling(window=self.long_window).mean()

        # Generate signals
        signals[short_ma > long_ma] = 1  # Buy signal
        signals[short_ma < long_ma] = -1  # Sell signal

        return signals