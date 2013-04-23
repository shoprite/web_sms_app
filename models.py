from pymongo import MongoClient
from extras import utils
from web.contrib.template import render_jinja
import web,os

render = render_jinja(
  os.path.join(os.path.dirname(__file__),'templates'),
	encoding='utf-8')

class products:

	client = MongoClient()
	product = client.shoprite_db.products

	def GET(self):
		records = self.get_all()
		return render.products(records=records)

	def add(self, product_code, product_name):
		data = {
			'product_code' : product_code,
			'product_name' : product_name
		}

		return utils()._persist(data, 'products')

	def get(self, product_code):
		try: 
			return self.product.find_one({'product_code' : product_code})
		except:
			print sys.exc_info()[0]
			return None

	def get_all(self):
		return self.product.find()

	def POST(self):
		data = web.input() 
		self.add(data.product_code, data.product_name)
	 	raise web.seeother('/products')

class shops:

	client = MongoClient()
	shop = client.shoprite_db.shops

	def GET(self):
		records = self.get_all()
		return render.shops(records=records)

	def add(self, shop_code, shop_name):
		data = {
			'shop_code' : shop_code,
			'shop_name' : shop_name
		}

		return utils()._persist(data, 'shops')

	def get(self, shop_code):
		try: 
			return self.shop.find_one({'shop_code' : shop_code})
		except:
			return None

	def get_all(self):
		return self.shop.find()

	def POST(self):
		data = web.input() 
		self.add(data.shop_code, data.shop_name)
	 	raise web.seeother('/shops')
