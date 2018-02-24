import gdax, json
from AUTH import auth
global price

# API key
API = auth()

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
	def __init__(self, product_id, stoploss, quantity):
		super(TrailingStopLoss, self).__init__(products = product_id)
		self.current_price = 0.0
		self.max_price = 0.0
		self.threshold = ''
		self.stoploss = stoploss
		self.first = True
		self.quantity = quantity
		self.current_orderID = None

		self.authenticated = auth()

		self.product_id = product_id



		self.start_datetime = None
		self.end_datetime = None
		

	def on_message(self, msg):

		# Match order 
		if msg['type'] == 'match':

			# Update real time price
			self.price = float(msg['price'])

			text.write(str(self.price) + "\n")
			print(self.price)

			# If first message
			if self.first:

				# Save datetime 
				self.start_datetime = msg['time']

			# Updating max price
			if self.max_price < self.price:

				# Set max price and threshold
				self.max_price = self.price
				threshold = str(self.max_price - self.stoploss)

				# Truncate threshold to fit GDAX requirements
				self.threshold = threshold[: (threshold.find('.') + 3)]

				text.write("Max price is updated to " + str(self.max_price) + "\n")
				text.write("Threshold is now " + self.threshold + "\n")

				if not self.first:

					# Cancel current stoploss
					self.authenticated.cancel_order(self.current_orderID)
					text.write("Old order canceled, id: " + self.current_orderID)

					print("Old order canceled, id: " + self.current_orderID)

				# Initialize stoploss order
				order = self.authenticated.sell(price=str(
					self.threshold), size=str(self.quantity), product_id=self.product_id)

				printJSON(order)

				# Save order ID
				self.current_orderID = order['id']
				text.write("New order set, id: " + self.current_orderID)

				print("New order ID: " + self.current_orderID)
				

			# Check if price exceeds stoploss threshold
			if self.price <= float(self.threshold):

				text.write("-- Stoploss triggered at " + str(self.price) + "\n")
				text.write("Starting time: " + self.start_datetime + "\n")
				text.write("Ending time: " + self.end_datetime + "\n")
				text.close()

				# Close websocket
				self.stop = True

			# Update final datetime
			self.end_datetime = msg['time']

			# Set first boolean to false at end of iteration
			self.first = False

			
	def on_close(self):
		print("-- Websocket Closing --")



# Writing output to text file

text = open('Output.txt', "w")

wsClient = TrailingStopLoss(product_id = 'ETH-USD', stoploss = 0.02, quantity = 1)
wsClient.start()

# first = True

# if first:
# 	print('yes')

# if not first:
# 	print('no')

# Buying .5 ethereum
# auth.buy(type = 'market', size = '1', product_id = 'ETH-USD')
# print(auth.sell(price = '5000', size = '0.5', product_id = 'BTC-USD'))
# printJSON(auth.get_orders())
# printJSON(auth.get_accounts())


