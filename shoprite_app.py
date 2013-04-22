import web, admin, extras
from extras import utils

urls = (
            '/?', 'handler',
            '/admin', admin.app_admin
            )
app = web.application(urls, globals()).wsgifunc()
application = app

class handler:        

  

  def GET(self):
    data = web.input() # ?sender=0845678910&text=64353264&timestamp=2013-04-17%20203 
    print data
    message = utils().clean_sms(data.text)
    if not utils().is_valid_sms(message):
      return
    
    shop_code = message[:3]
    product_code = message[3:]

    product_name = None
    shop_name = None

    print product_code
    print shop_code

    try:
      product_name = extras.products[product_code]
      shop_name = extras.shops[shop_code]

    except:
      return 'Invalid product or shop code'

    message = 'Thanks for your input! You sent %s @ %s' % (product_name, shop_name)
    
    response = utils()._send_sms([data.sender], message)
    record = {
      'customer_number' : data.sender,
      'timestamp'       : data.timestamp,
      'product_name'    : product_name,
      'shop_name'       : shop_name,
      'notified'        : False
    }
    utils()._persist(record)
    return response.content


if __name__ == "__main__": app.run()
