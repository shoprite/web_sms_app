import web, random, extras, os
from pymongo import MongoClient
from web.contrib.template import render_jinja
from extras import utils

urls = ('/?', 'index',
		'/notify/?', 'notify',
		'/products/?', 'products',
		'/shops/?', 'shops'
	)

render = render_jinja(
  os.path.join(os.path.dirname(__file__),'templates'),
	encoding='utf-8')

class index:
	def GET(self):
		records = self._get_records()
		return render.index(records=records)

	def _get_records(self):
		client = MongoClient()
		db = client.shoprite_db
		return db.messages.find()

class notify:
	def GET(self):
		data = {
			'products' : products().get_all(),
			'shops'	   : shops().get_all()
		}
		return render.notify(**data)

	def POST(self):
		data = web.input()
		 
		product_code = data.product_code
		shop_code = data.shop_code
		return self.send_notification(shop_code, product_code)

	def send_notification(self, shop_code, product_code):
		client = MongoClient()

		affected_messges = client.shoprite_db.messages.find({'product_code': product_code, 'notified':False})

		if affected_messges.count() == 0:
			raise web.seeother("/notify")

		product = products().get(product_code)
		shop = shops.get(shop_code)

		loyalty_code = self.generate_loyalty_code() # need to generate IN loop
		message = '%s is back in stock @ %s. Your loyalty code is %s' % (product.product_name, shop.shop_name, loyalty_code)
		utils()._send_sms([m['customer_number'] for m in affected_messges], message )
		return message

	def generate_loyalty_code(self):
		return random.randrange(100000, 999999)

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

app_admin = web.application(urls, locals())
