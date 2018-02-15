import gdax
import json

public = gdax.PublicClient()

def get_products_USD():
	'''Modify JSON object get_products to only store USD'''
	return [products for products in public.get_products() if products['quote_currency'] == 'USD']


def printJSON(JSON):
	''' Prints JSON object in readable format. '''
	print json.dumps(JSON, indent = 4)


printJSON(get_products_USD())
