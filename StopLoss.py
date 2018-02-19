import gdax, json, time
from AUTH import auth
global price

# API key
auth = auth()

public = gdax.PublicClient()

def get_products(currency='USD'):
	'''Modify JSON object get_products to get quotes in various currencies
	Default behavior: USD
	Options: BTC, USD, GBR, EUR
	'''
	return [products for products in public.get_products() if products['quote_currency'] == currency.upper()]

def get_accounts(i=0):
	''' Default behavior: Return account inventory if balance is greater than 0
	Options: -1 to return all, else i'''
	return [item for item in auth.get_accounts() if float(item['balance']) > i]


def printJSON(JSON):
	''' Prints JSON object in readable format'''
	print(json.dumps(JSON, indent=4))


class MyWebsocketClient(gdax.WebsocketClient):
	def __init__(self, product_id, stoploss):
		# Add price variable
		super(MyWebsocketClient, self).__init__(products = product_id)
		self.current_price = 0
		self.max_price = 0
		self.stoploss = stoploss

	def on_message(self, msg):
		threshold = 0

		if msg['type'] == 'match':
			print(msg['product_id'], msg['price'])
			self.price = float(msg['price'])

			# Update max price if necessary
			if self.max_price < self.price:
				self.max_price = self.price
				threshold = self.max_price - self.stoploss
				print("Max price is updated to " + str(self.max_price))
				print("Threshold is now " + str(threshold))

			# Check if price exceeds stopgap
			if self.price < threshold:
				self.stop = True
				print("-- Stoploss triggered at " + str(self.price))

			
	def on_close(self):
		print("-- Websocket Closing --")


wsClient = MyWebsocketClient(product_id = 'BTC-USD', stoploss = .02)
wsClient.start()





# Buying .5 ethereum
# print(auth.buy(type = 'market', size = '0.5', product_id = 'ETH-USD'))
# print(auth.sell(price = '5000', size = '0.5', product_id = 'BTC-USD'))
# printJSON(auth.get_orders())
# printJSON(auth.get_accounts())



