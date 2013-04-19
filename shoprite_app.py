import os, web, requests, json
from requests import Request, Session
from pymongo import MongoClient
import re

urls = (
            '/', 'handler',
            '/test', 'test'
            )
app = web.application(urls, globals())

class handler:        
  LOGIN = None
  PWD = None

  def __init__(self):
    self.get_credentials()


  def GET(self):
    data = web.input()
    print data
    response = self._send_sms(data.sender, data.text)
    self._persist(data)
    return response.content

  def _send_sms(self, dest, msg):
    request = requests.Request('POST',
        'http://api.infobip.com/api/v3/sendsms/json')

    request.headers = { 'content-type' : 'application/json' }
    json_obj = {
        'authentication' : {
          'username' : self.LOGIN,
          'password' : self.PWD
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
  
  def get_credentials(self):
    f = open('login.cred', 'r')
    self.LOGIN, self.PWD = f.read().replace('\n','').split(':')


  def _persist(self, data):
    client = MongoClient()
    db = client.shoprite_db
    messages = db.messages
    message_id = messages.insert(data)

  def is_valid_sms(self, msg):
    regex = r'^\d{3}[\s]*\d{5}$'
    return re.match(regex, msg) is not None

  def clean_sms(self, msg):
    return msg.replace(' ','')

def is_test():
    if 'WEBPY_ENV' in os.environ:
        return os.environ['WEBPY_ENV'] == 'test'


if (not is_test()) and __name__ == "__main__": app.run()