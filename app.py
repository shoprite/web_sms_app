import web
from pymongo import MongoClient

urls = (
            '/(.*)', 'handler'
            )
app = web.application(urls, globals())

class handler:        
  def GET(self, sender='', receiver='', text='', timestamp=''):
    data = web.input()
    self._persist(data)
    return 'Message successfully received and saved'

  def _persist(self, data):
    client = MongoClient()
    db = client.shoprite_db
    messages = db.messages
    message_id = messages.insert(data)


if __name__ == "__main__":
  app.run()
