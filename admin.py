import web
from pymongo import MongoClient
from web.contrib.template import render_jinja

urls = ('/*', 'index')

render = render_jinja(
	'templates',
	encoding='utf-8')

class index:
	def GET(self):
		records = self._get_records()
		return render.index(records=records)

	def _get_records(self):
		client = MongoClient()
		db = client.shoprite_db
		return db.messages.find()


app_admin = web.application(urls, locals())