import sys, re, web, util
from models import Product, Shop, Message

class MessageController:        
  def GET(self):
    data = web.input() # ?cellno=0845678910&reply=64353264&replydate=2013-04-17%20203 
    web.header('Content-Type', 'text/plain')

    if not self._is_valid_request(data):  
      raise web.badrequest('Invalid request')

    data.reply = data.reply.replace(' ', '')
    if not self._is_valid_text(data.reply):
      return

    try:
      message = self._parse_query(data).save()
    except Exception as exc:
      raise web.badrequest(exc.args[0])

    reply_text = 'Thanks for your input! You sent %s @ %s' % (Product(message.product_code).fetch().name, Shop(message.shop_code).fetch().name)
    
    response = util._send_sms(message.customer_number, reply_text)
    return response.content

  def _is_valid_request(self, request_data):
    return request_data.has_key('cellno') \
      and request_data.has_key('reply') \
      and request_data.has_key('replydate')

  def _is_valid_text(self, input):
    regex = r'^\d{3}[\s]*\d{5}$'
    return re.match(regex, input) is not None

  def _parse_query(self, query_params):
    shop_code = query_params.reply[:3]
    product_code = query_params.reply[3:]

    if not (Shop(shop_code).is_valid() and Product(product_code).is_valid()):
      raise Exception('Invalid product or shop code.')

    message = Message()
    message.customer_number = query_params.cellno
    message.product_code = product_code
    message.shop_code = shop_code
    message.timestamp = query_params.replydate #TODO: date conversion

    return message
