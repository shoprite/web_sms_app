import web
from pymongo import MongoClient

urls = ('/', 'index')

class index:
	def GET(self):
		pass

	def _get_records(self):
		client = MongoClient()
		db = client.shoprite_db
		return db.messages.find()


app_admin = web.application(urls, locals())