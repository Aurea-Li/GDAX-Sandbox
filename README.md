### GDAX Sandbox Project

This project is an independent study to implement additional functionality to GDAX, Coinbase's cryptocurrency exchange platform. Work in progress.

#### Trailing Stop Loss

The function `TrailingStopLoss` in `StopLoss.py` allows you to implement a trailing stop loss in GDAX.  

##### Example

```python
wsClient = TrailingStopLoss(product_id = 'BTC-USD', stoploss = 0.02, quantity = 0.5)
wsClient.start()
```

#### References
1. GDAX API: [https://docs.gdax.com/](https://docs.gdax.com/)
2. "Unofficial" Python Client Library: [https://github.com/danpaquin/gdax-python](https://github.com/danpaquin/gdax-python)