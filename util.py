import json, requests, credential
from requests import Session

def _send_sms(dest, message):
    request = requests.Request('POST',
        'http://api.infobip.com/api/v3/sendsms/json')

    request.headers = { 'content-type' : 'application/json' }
    recipients = []
    for rec in dest:
      recipients.append({'gsm' : rec})
    
    json_obj = {
        'authentication' : {
          'username' : credential.LOGIN, #TODO: make credentials global
          'password' : credential.PASS
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

    try:
      return s.send(request.prepare())
    except:
      return None