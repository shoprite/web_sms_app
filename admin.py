import os, random, json, web, util, models
from pymongo import MongoClient
from web.contrib.template import render_jinja
from models import Message, Product, Shop

urls = ('/?', 'AdminMessageController',
		'/(.*)s/?', 'EntityController'
	)

render = render_jinja(
  os.path.join(os.path.dirname(__file__),'templates'),
	encoding='utf-8')

class AdminMessageController:
	def GET(self):
		data = {
			'products'	: Product().all(),
			'shops'		: Shop().all(),
			'messages'	: Message().all()
		}
		return render.admin_index(**data)

	def POST(self):
		data = web.input()
		 
		product_code = data.product_code
		shop_code = data.shop_code
		return self.send_notification(shop_code, product_code)

	def send_notification(self, shop_code, product_code):
		affected_messages = Message().fetch_by(shop_code=shop_code, product_code=product_code)

		if affected_messages.count() == 0:
			raise web.seeother("/")

		product = Product(product_code).fetch()
		shop = Shop(shop_code).fetch()

		loyalty_code = self.generate_loyalty_code() # TODO: need to generate IN loop
		reply_text = '%s is back in stock @ %s. Your loyalty code is %s' % (product.name, shop.name, loyalty_code)

		response = util._send_sms([m['customer_number'] for m in affected_messages], reply_text )

		if response is not None:
			response_list = json.loads(response.content)['results']
			for r in response_list:
				if r['status'] == '0':
					affected_messages.collection.update({'notified': False, 'product_code': product_code, 'shop_code': shop_code , 'customer_number': r['destination']}, {'$set': {'notified': True}})
		
		return response.content

	def generate_loyalty_code(self):
		return random.randrange(100000, 999999)

class EntityController:
	def GET(self, entity_name):
		records = getattr(models, entity_name.capitalize())().all() # TODO: try-catch - if AttributeError, raise 404
		return getattr(render, entity_name)(records=records)

	def POST(self, entity_name):
		data = web.input()

		entity = getattr(models, entity_name.capitalize())(data.code, data.name)
		entity.save()
	 	raise web.seeother('/' + entity_name + 's')

app_admin = web.application(urls, locals())
