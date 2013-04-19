import subprocess
import os
from web import utils
from nose.tools import *
from shoprite_app import app, handler 
import shoprite_app
import requests, json
import admin

from paste.fixture import TestApp


app_dir = os.path.join(os.path.dirname(__file__), "..")

class TestHandler:
  """ Tests for the handler class
  """
  data = { 
        'sender' : '0844264215',
        'receiver' : '31202',
        'text'     : 'skdhjfljsldkjfljssdf',
        'datetime' : '2013-04-21 06:12:21',
        'encoding' : 'utf-8',
        'esm'      : 'something',
        'output'   : 'json'
        }
  dest = '27827824665'
  msg = 'Wheres my nappies?'

  def __start_server(self):
    app.run()

  def __stop_server(self):
    del app

  # def setup(self):
  #   middleware = []
  #   self.testApp = TestApp(app.wsgifunc(*middleware))

  # def test_get_request(self):

  #   response = self.testApp.get('/?sender=me&text=bleh', headers={'Content-Type': 'application/json'})
  #   assert_equal(response.status, 200)

  # @with_setup(__start_server, __stop_server)
  # def test_get_reponse(self):
  #   r = app.request(data=self.data)
  #   assert_is_not_none(r.data)

  # @with_setup(__start_server, __stop_server)
  # def test_receive_request_from_provider(self):
  #   r = app.request(data=self.data)
  #   assert_equals(r.status, '200 OK')


  # @with_setup(__start_server, __stop_server)
  # def test_respond_to_request(self):
  #   r = app.request( data=self.data)
  #   assert_equal(r.data, 'Thank you for notifying us!')


  @with_setup(__start_server, __stop_server)
  def test_sms_host_reachable(self):
    req = handler()._send_sms(self.dest, self.msg)
    assert_equal(req.status_code, 200)
    
  @with_setup(__start_server, __stop_server)
  def test_sms_send_successful(self):
    req = handler()._send_sms(self.dest, self.msg)
    json_obj = json.loads(req.content)

    assert_equal(json_obj['results'][0]['status'], '0')
    assert_equal(json_obj['results'][0]['destination'], self.dest)
    assert_not_equal(json_obj['results'][0]['messageid'], '')

  def test_can_retrieve_infobip_credentials(self):
    h = handler()
    h.get_credentials()
    assert_is_not_none(h.LOGIN)
    assert_is_not_none(h.PWD)

  def test_clean_message(self):
    msg1 = '234 5546'
    msg2 = '3532 4254 463 62346'
    assert_equal(handler().clean_sms(msg1), '2345546')
    assert_equal(handler().clean_sms(msg2), '3532425446362346')

  def test_sms_is_valid(self):
    message = '203 89896'
    clean_message = handler().clean_sms(message)
    assert_true(handler().is_valid_sms(clean_message))

  def test_product_name_can_be_retrieved_from_product_code(self):
    product_code = '98997'
    product_name = handler.products[product_code]
    assert_equal(product_name, 'Pepsi')

  def test_can_retrieve_shop_from_shop_code(self):
    shop_code = '535'
    shop_name = handler.shops[shop_code]
    assert_equal(shop_name, 'Randburg')

  def test_can_retrieve_records_from_database(self):
    records = admin.index()._get_records()
    assert_is_not_none(records)

  def test_can_persist_records_to_database(self):
    test_data = {
      'customer_no' : '0827824665',
      'timestamp'   : '2013-04-27 10:33:16',
      'product_name': 'Test Product',
      'shop_name'   : 'Test Shop'
    }

    record_id = handler()._persist(test_data)
    assert_is_not_none(record_id)

    

