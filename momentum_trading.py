import backtrader as bt
import yfinance as yf

class MomentumStrategy(bt.Strategy):
    params = (('rsi_period', 14), ('ema_short', 12), ('ema_long', 26))

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period)
        self.ema_short = bt.indicators.EMA(period=self.params.ema_short)
        self.ema_long = bt.indicators.EMA(period=self.params.ema_long)
        self.macd = bt.indicators.MACD()
        self.trades = []
        self.profit_trades = 0
        self.total_trades = 0

    def next(self):
        if not self.position:  # Pas de position ouverte
            if self.rsi > 50 and self.ema_short > self.ema_long and self.macd.macd > self.macd.signal:
                self.buy()
                self.entry_price = self.data.close[0]

        else:  # Si une position est ouverte
            if self.rsi > 70 or self.ema_short < self.ema_long:
                profit = self.data.close[0] - self.entry_price
                self.trades.append(profit)
                if profit > 0:
                    self.profit_trades += 1
                self.total_trades += 1
                self.close()

# Récupération des données
symbol = 'BTC-USD'
start_date = '2023-01-01'
end_date = '2024-01-01'
data = bt.feeds.PandasData(dataname=yf.download(symbol, start=start_date, end=end_date))

# Configuration du backtest
cerebro = bt.Cerebro()
cerebro.addstrategy(MomentumStrategy)
cerebro.adddata(data)
cerebro.broker.set_cash(10000)  # Capital initial

# Exécution du backtest
results = cerebro.run()
strategy = results[0]

# Calcul des performances
win_rate = (strategy.profit_trades / strategy.total_trades) * 100 if strategy.total_trades > 0 else 0
total_profit = sum(strategy.trades)

# Affichage des résultats
print(f"Taux de réussite : {win_rate:.2f}%")
print(f"Profit total : {total_profit:.2f}$")
print(f"Nombre total de trades : {strategy.total_trades}")