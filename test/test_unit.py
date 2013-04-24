import subprocess
import os
from nose.tools import *
from shoprite_app import app, handler 
import shoprite_app
import requests, json
import admin
from admin import products, shops

from paste.fixture import TestApp

from models import Message
from factories import MessageFactory

app_dir = os.path.join(os.path.dirname(__file__), "..")

DATABASE = 'shoprite_db_test'

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

  @with_setup(__start_server, __stop_server)
  def test_sms_host_reachable(self):
    req = utils()._send_sms([self.dest], self.msg)
    assert_equal(req.status_code, 200)
    
  @with_setup(__start_server, __stop_server)
  def test_sms_send_successful(self):
    req = utils()._send_sms([self.dest], self.msg)
    json_obj = json.loads(req.content)

    assert_equal(json_obj['results'][0]['status'], '0')
    assert_equal(json_obj['results'][0]['destination'], self.dest)
    assert_not_equal(json_obj['results'][0]['messageid'], '')

  def test_can_retrieve_infobip_credentials(self):
    h = utils()
    h.get_credentials()
    assert_is_not_none(h.LOGIN)
    assert_is_not_none(h.PWD)

  def test_clean_message(self):
    msg1 = '234 5546'
    msg2 = '3532 4254 463 62346'
    assert_equal(utils().clean_sms(msg1), '2345546')
    assert_equal(utils().clean_sms(msg2), '3532425446362346')

  def test_sms_is_valid(self):
    message = '203 89896'
    clean_message = utils().clean_sms(message)
    assert_true(utils().is_valid_sms(clean_message))

  def test_can_persist_records_to_database(self):
    test_data = {
      'customer_number' : '0827824665',
      'timestamp'   : '2013-04-27 10:33:16',
      'product_name': 'Test Product',
      'shop_name'   : 'Test Shop',
      'notified'    : False
    }

    record_id = utils()._persist(test_data, 'messages_test')
    assert_is_not_none(record_id)



class TestProducts:
  def test_can_create_product(self):
    product_code = '00451'
    product_name = 'Cat Brand Pea Nuts Paste'
    p = products().add(product_code, product_name)

    assert_is_not_none(p)

  def test_can_retrieve_product_by_product_code(self):
    product_code = '00652'
    product_name = 'Foolscap L/S'
    products().add(product_code, product_name)

    get_product = products().get('00652')
    assert_equal(get_product['product_code'], '00652')


class TestShops:
  def test_can_create_shop(self):
    shop_code = '456'
    shop_name = 'Rosebank Mall'
    s = shops().add(shop_code, shop_name)

    assert_is_not_none(s)

  def test_can_retrieve_shop_by_shop_code(self):
    shop_code = '865'
    shop_name = 'Braamfontein Annex B'
    shops().add(shop_code, shop_name)

    get_shop = shops().get('865')
    assert_equal(get_shop['shop_code'], '865')

class TestModels:

  def test_must_retrieve_all_messages(self):
    messages = Message().all()
    initial_count = messages.count()

    new_message = MessageFactory().create()
    new_message.save()

    messages = Message().all()
    new_count = messages.count()

    assert_equal(1, new_count - initial_count)


