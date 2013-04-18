import subprocess
import os
from web import utils
from nose.tools import *
from shoprite_app import app 
from shoprite_app import handler
import requests, json

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

  def setup(self):
    middleware = []
    self.testApp = TestApp(app.wsgifunc(*middleware))

  def test_get_request(self):

    response = self.testApp.get('/?sender=me&text=bleh', headers={'Content-Type': 'application/json'})
    assert_equal(response.status, 200)

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


  # @with_setup(__start_server, __stop_server)
  # def test_sms_host_reachable(self):
  #   req = handler()._send_sms(self.dest, self.msg)
  #   assert_equal(req.status_code, 200)
    
  # @with_setup(__start_server, __stop_server)
  # def test_sms_send_successful(self):
  #   req = handler()._send_sms(self.dest, self.msg)
  #   json_obj = json.loads(req.content)

  #   assert_equal(json_obj['results'][0]['status'], '0')
  #   assert_equal(json_obj['results'][0]['destination'], self.dest)
  #   assert_not_equal(json_obj['results'][0]['messageid'], '')
  

