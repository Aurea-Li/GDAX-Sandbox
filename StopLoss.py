import gdax, json
from AUTH import auth

class TrailingStopLoss(gdax.WebsocketClient):
	''' Function that allows you to place a sell trailing stop loss
		orders in real time using a constant spread. '''
	def __init__(self, product_id, stoploss, quantity):
		super(TrailingStopLoss, self).__init__(products = product_id)

		# Setting stop loss attributes
		self.current_price = 0.0
		self.max_price = 0.0
		self.threshold = ''
		self.stoploss = stoploss
		self.quantity = quantity
		self.current_orderID = None
		self.product_id = product_id
		self.first = True

		# Authenticating access to buying/selling 
		self.authenticated = auth()

		# Timestamp beginning and end of stoploss 
		self.start_datetime = None
		self.end_datetime = None
		

	def on_message(self, msg):

		# Match order 
		if msg['type'] == 'match':

			# Update real time price
			self.price = float(msg['price'])

			text.write("Current price: " + msg['price'] + "\n")

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
					
					text.write("Old order canceled, id: " + self.current_orderID + "\n")

				# Initialize stoploss order
				order = self.authenticated.sell(stop = 'loss', stop_price=str(self.threshold),
				price = str(self.threshold), size=str(self.quantity), product_id=self.product_id)

				# Save order ID
				self.current_orderID = order['id']

				text.write("New order set, id: " + self.current_orderID + "\n")

			# Check if price exceeds stoploss threshold
			if self.price <= float(self.threshold):

				text.write("-- Stoploss triggered at " + str(self.price) + "\n")
				text.write("Starting time: " + self.start_datetime + "\n")
				text.write("Ending time: " + self.end_datetime + "\n")
				text.close()

				# Close websocket
				self.stop = True

			# If first message
			if self.first:

				# Save datetime
				self.start_datetime = msg['time']
				self.first = False

			# Update final datetime
			self.end_datetime = msg['time']



# Writing output to text file
text = open('Output.txt', "w")

# Initializing and starting the Trailing Stop Loss
wsClient = TrailingStopLoss(product_id = 'BTC-USD', stoploss = 0.02, quantity = 0.5)
wsClient.start()






