import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from data.data_fetcher import fetch_data
from features.technical_indicators import calculate_sma, calculate_rsi
from strategies.moving_average_crossover import MovingAverageCrossover
from backtesting.backtest_engine import backtest

def analyze_stock(symbol):
    try:
        # Fetch data
        data = fetch_data(symbol, '2022-01-01', '2023-01-01')
        
        # Calculate indicators
        data['SMA_50'] = calculate_sma(data, 50)
        data['SMA_200'] = calculate_sma(data, 200)
        data['RSI'] = calculate_rsi(data, 14)
        
        # Create and run strategy
        strategy = MovingAverageCrossover(data, short_window=50, long_window=200)
        signals = strategy.generate_signals()
        
        # Backtest the strategy
        results = backtest(data, signals)
        
        return {
            'symbol': symbol,
            'total_return': results['total_return'],
            'sharpe_ratio': results['sharpe_ratio'],
            'current_signal': signals.iloc[-1],
            'current_rsi': data['RSI'].iloc[-1]
        }
    except Exception as e:
        print(f"Error analyzing {symbol}: {str(e)}")
        return None

def get_sp500_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]
    return df['Symbol'].tolist()

def main():
    sp500_symbols = get_sp500_symbols()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(analyze_stock, sp500_symbols))
    
    # Filter out None results (errors)
    results = [r for r in results if r is not None]
    
    # Sort stocks by total return
    results.sort(key=lambda x: x['total_return'], reverse=True)
    
    print("Top 10 stocks by historical performance:")
    for stock in results[:10]:
        print(f"{stock['symbol']}: Return: {stock['total_return']:.2%}, Sharpe: {stock['sharpe_ratio']:.2f}, Signal: {stock['current_signal']}, RSI: {stock['current_rsi']:.2f}")
    
    print("\nStocks with current buy signals:")
    buy_signals = [stock for stock in results if stock['current_signal'] == 1 and 30 < stock['current_rsi'] < 70]
    for stock in buy_signals[:10]:  # Show top 10 buy signals
        print(f"{stock['symbol']}: Return: {stock['total_return']:.2%}, Sharpe: {stock['sharpe_ratio']:.2f}, RSI: {stock['current_rsi']:.2f}")

if __name__ == "__main__":
    main()