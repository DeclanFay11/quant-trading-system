import matplotlib.pyplot as plt

def plot_equity_curve(equity_curve):
    """Plot the equity curve of the trading strategy."""
    plt.figure(figsize=(10, 6))
    plt.plot(equity_curve)
    plt.title('Equity Curve')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value')
    plt.show()