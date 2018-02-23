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



class TrailingStopLoss(gdax.WebsocketClient):
	''' Function that allows you to place a sell trailing stop loss
		orders in real time using a constant spread. '''
	def __init__(self, product_id, stoploss, quantity, auth):
		super(MyWebsocketClient, self).__init__(products = product_id)
		self.current_price = 0.0
		self.max_price = 0.0
		self.threshold = 0.0
		self.stoploss = stoploss
		self.message_count = 0
		self.quantity = quantity
		self.current_orderID = None

		# Pass in auth object
		self.auth = auth

		self.start_datetime = None
		self.end_datetime = None
		

	def on_message(self, msg):

		# Match order 
		if msg['type'] == 'match':

			# Update real time price
			self.price = float(msg['price'])
			text.write(str(self.price) + "\n")

			# Update max price and threshold if necessary
			if (self.max_price < self.price):
				self.max_price = self.price
				self.threshold = self.max_price - self.stoploss

				text.write("Max price is updated to " + str(self.max_price) + "\n")
				text.write("Threshold is now " + str(self.threshold) + "\n")


			# If first message
			if self.message_count == 0:

				# Save datetime 
				self.start_datetime = msg['time']

				# Initialize stoploss order
				order = self.auth.sell(type = 'market', price=str(self.threshold), size=str(self.quantity), product_id=self.product_id)
				
				# Save order ID
				self.current_orderID = order['id']


			# Update max price and threshold if necessary
			if (self.max_price < self.price):
				self.max_price = self.price
				self.threshold = self.max_price - self.stoploss

				text.write("Max price is updated to " + str(self.max_price) + "\n")
				text.write("Threshold is now " + str(self.threshold) + "\n")

				# Cancel current stoploss
				self.auth.cancel_order(self.current_orderID)
				text.write("Old order canceled, id: " + self.current_orderID)

				# Initialize stoploss order
				order = self.auth.sell(type = 'market', price=str(self.threshold), size=str(self.quantity), product_id=self.product_id)

				# Save order ID
				self.current_orderID = order['id']
				text.write("New order set, id: " + self.current_orderID)
				

			# Check if price exceeds stoploss threshold
			if (self.price <= self.threshold):

				text.write("-- Stoploss triggered at " + str(self.price))
				text.write("Starting time: " + self.start_datetime)
				text.write("Ending time: " + self.end_datetime)
				text.close()

				# Close websocket
				self.stop = True

			# Update message count and final datetime
			self.message_count += 1
			self.end_datetime = msg['time']

			
	def on_close(self):
		print("-- Websocket Closing --")



# Writing output to text file
start = time.clock()
text = open('Output.txt', "w")

wsClient = TrailingStopLoss(product_id = 'BTC-USD', stoploss = 0.01, auth = auth)
wsClient.start()

print(time.asctime())







# Buying .5 ethereum
# print(auth.buy(type = 'market', size = '0.5', product_id = 'ETH-USD'))
# print(auth.sell(price = '5000', size = '0.5', product_id = 'BTC-USD'))
# printJSON(auth.get_orders())
# printJSON(auth.get_accounts())


