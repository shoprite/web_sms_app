import re, requests, json, os
from pymongo import MongoClient
from requests import Request, Session

products = {
              '43298':'Orange Jam',
              '53264':'Huggies Nappies',
              '78568':'Coffee Mug',
              '82584':'Disposable Nakpins L/S',
              '98997':'Pepsi'
    }

shops = {
              '535':'Randburg',
              '643':'Braamfontein Annex B',
              '941':'Rosebank',
              '853':'Linden'
    }


class utils:
  LOGIN = None
  PWD = None

  def __init__(self):
  	self.get_credentials()

  def _send_sms(self, dest, message):
    request = requests.Request('POST',
        'http://api.infobip.com/api/v3/sendsms/json')

    request.headers = { 'content-type' : 'application/json' }
    recipients = []
    for rec in dest:
      recipients.append({'gsm' : rec})
    
    json_obj = {
        'authentication' : {
          'username' : self.LOGIN,
          'password' : self.PWD
          },
        'messages'      : {
          'sender'    : 'Shoprite',
          'text'      : message,
          'recipients': recipients
          } # close messages
        } # close json_obj

    request.data = json.dumps(json_obj)

    # send the request
    s = Session()
    return s.send(request.prepare())

  def get_credentials(self):
    root = os.path.dirname(__file__)
    f = open(os.path.join(root,'login.cred'), 'r')
    self.LOGIN, self.PWD = f.read().replace('\n','').split(':')

  def _persist(self, data, table='messages'):
    client = MongoClient()
    db = client.shoprite_db
    messages = getattr(db, table)
    return messages.insert(data)

  def is_valid_sms(self, msg):
    regex = r'^\d{3}[\s]*\d{5}$'
    return re.match(regex, msg) is not None

  def clean_sms(self, msg):
    return msg.replace(' ','')
