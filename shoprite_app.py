import os, web, requests, json
from requests import Request, Session
from pymongo import MongoClient

urls = (
            '/', 'handler',
            '/test', 'test'
            )
app = web.application(urls, globals())

class handler:        
  def GET(self):
    data = web.input()
    print data
    response = self._send_sms(data.sender, data.text)
    self._persist(data)
    return 'Thank you for notifying us!'

  def _send_sms(self, dest, msg):
    request = requests.Request('POST',
        'http://api.infobip.com/api/v3/sendsms/json')

    request.headers = { 'content-type' : 'application/json' }
    json_obj = {
        'authentication' : {
          'username' : 'test',
          'password' : 'test'
          },
        'messages'      : {
          'sender'    : 'Shoprite',
          'text'      : 'Thank you for notifying us!',
          'recipients': [
            { 'gsm' : '27827824665' }
            ]
          } # close messages
        } # close json_obj

    request.data = json.dumps(json_obj)

    # send the request
    s = Session()
    return s.send(request.prepare())

  def _persist(self, data):
    client = MongoClient()
    db = client.shoprite_db
    messages = db.messages
    message_id = messages.insert(data)

class test:
  def GET(self):
    return web.input()

def is_test():
    if 'WEBPY_ENV' in os.environ:
        return os.environ['WEBPY_ENV'] == 'test'

if (not is_test()) and __name__ == "__main__": app.run()