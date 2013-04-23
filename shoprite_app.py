import web, admin, extras, sys
from extras import utils
from models import products, shops

urls = (
            '/?', 'handler',
            '/admin', admin.app_admin
            )
app = web.application(urls, globals())
application = app

class handler:        
  def GET(self):
    data = web.input() # ?sender=0845678910&text=64353264&timestamp=2013-04-17%20203 
    
    if not self._is_valid_request(data):
      web.header('Content-Type', 'text/plain')
      raise web.badrequest('Invalid request')

    message = utils().clean_sms(data.text)
    if not utils().is_valid_sms(message):
      return
    
    shop_code = message[:3]
    product_code = message[3:]

    product_name = None
    shop_name = None

    try:
      product_name = products().get(product_code)['product_name']
      shop_name = shops().get(shop_code)['shop_name']

    except:
      return 'Invalid product or shop code\n', sys.exc_info()[1]

    message = 'Thanks for your input! You sent %s @ %s' % (product_name, shop_name)
    
    response = utils()._send_sms([data.sender], message)
    record = {
      'customer_number' : data.sender,
      'timestamp'       : data.timestamp,
      'product_code'    : product_code,
      'shop_code'       : shop_code,
      'notified'        : False
    }
    utils()._persist(record)
    return response.content

  def _is_valid_request(self, request_data):
    return request_data.has_key('sender') and request_data.has_key('text') and request_data.has_key('timestamp')


if __name__ == "__main__": app.run()
