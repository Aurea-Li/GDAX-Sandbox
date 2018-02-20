import gdax, json, datetime
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
		super(MyWebsocketClient, self).__init__(products = product_id)
		self.current_price = 0.0
		self.max_price = 0.0
		self.threshold = 0.0
		self.stoploss = stoploss
		self.start_time = time.asctime()
		self.end_time = None
		

	def on_message(self, msg):

		if msg['type'] == 'match':
			self.price = float(msg['price'])
			text.write(str(self.price) + "\n")
			printJSON(msg)

			# Update max price if necessary
			if (self.max_price < self.price):	
				self.max_price = self.price
				self.threshold = self.max_price - self.stoploss

				text.write("Max price is updated to " + str(self.max_price) + "\n")
				text.write("Threshold is now " + str(self.threshold) + "\n")

				# Cancel current stoploss

				# Set new stoploss order
				

			# Check if price exceeds stoploss threshold
			if (self.price <= self.threshold):

				text.write("-- Stoploss triggered at " + str(self.price))
				text.close()
				self.stop = True



			
	def on_close(self):
		print("-- Websocket Closing --")
		self.end_time = time.clock()
		print('Total time = ' + str(self.end_time - self.start_time))


# Writing output to text file
start = time.clock()
text = open('Output.txt', "w")

wsClient = MyWebsocketClient(product_id = 'BTC-USD', stoploss = 0.01)
wsClient.start()

print(time.asctime())







# Buying .5 ethereum
# print(auth.buy(type = 'market', size = '0.5', product_id = 'ETH-USD'))
# print(auth.sell(price = '5000', size = '0.5', product_id = 'BTC-USD'))
# printJSON(auth.get_orders())
# printJSON(auth.get_accounts())


