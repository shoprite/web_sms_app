from pymongo import MongoClient
from extras import utils
from web.contrib.template import render_jinja
import web, os, sys

render = render_jinja(
  os.path.join(os.path.dirname(__file__),'templates'),
	encoding='utf-8')

class Model(object):
	client = None
	db = None

	def __init__(self, db_name='shoprite_db'):
		self.client = MongoClient()
		self.db = getattr(self.client, db_name)

	def all(self):
		return getattr(self.db, type(self).__name__).find()

	def _persist(self, data):
		return getattr(self.db, type(self).__name__).insert(data)

class Message(Model): 
	customer_number = ''
	product_code = ''
	shop_code = ''
	timestamp = None
	notified = False

	def save(self):
		try:
			data = {
				'customer_number'	: self.customer_number,
				'product_code'		: self.product_code,
				'shop_code'			: self.shop_code,
				'timestamp'			: self.timestamp,
				'notified'			: self.notified
			}

			self._persist(data)
			return self
		except:
			print sys.exc_info()[1]
			return None

	def fetch_by(self, **kwargs):
		return getattr(self.db, type(self).__name__).find(kwargs)


class Entity(Model):

	def __init__(self, code, name):
		Model.__init__(self)
		self.code = code
		self.name = name

	def save(self):
		data = {
			'code' : self.code,
			'name' : self.name
		}

		return self._persist(data)

	def fetch(self):
		try: 
			data = getattr(self.db, type(self).__name__).find_one({'code' : self.code})
			self.code = data['code']
			self.name = data['name']

			return self
		except:
			print sys.exc_info()[1]
			return None

	def is_valid(self):
		return self.fetch() is not None

class Product(Entity):

	def __init__(self, code='', name=''):
		Entity.__init__(self, code, name)
		


class Shop(Entity):

	def __init__(self, code='', name=''):
		Entity.__init__(self, code, name)

