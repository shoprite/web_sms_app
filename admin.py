import web, random, extras, os
from pymongo import MongoClient
from web.contrib.template import render_jinja
from extras import utils

urls = ('/*', 'index',
		'/notify', 'notify'
	)

render = render_jinja(
  os.path.join(os.path.dirname(__file__),'templates'),
	encoding='utf-8')

class index:
	def GET(self):
		records = self._get_records()
		print '****' , records.count()
		return render.index(records=records)

	def _get_records(self):
		client = MongoClient()
		db = client.shoprite_db
		return db.messages.find()

class notify:
	def GET(self):
		return render.notify()

	def POST(self):
		data = web.input()
		print data
		product_code = data.product_code
		shop_code = data.shop_code
		return self.send_notification(shop_code, product_code)

	def send_notification(self, shop_code, product_code):
		client = MongoClient()
		product_name = extras.products[product_code]
		shop_name = extras.shops[shop_code]
		affected_messges = client.shoprite_db.messages.find({'product_name': product_name, 'notified':False})
		loyalty_code = self.generate_loyalty_code() # need to generate IN loop
		message = '%s is back in stock @ %s. Your loyalty code is %s' % (product_name, shop_name, loyalty_code)
		utils()._send_sms([m['customer_number'] for m in affected_messges], message )
		return message

	def generate_loyalty_code(self):
		return random.randrange(100000, 999999)

app_admin = web.application(urls, locals())
