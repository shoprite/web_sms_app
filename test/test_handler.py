from nose.tools import *
from shoprite_app import app 
from shoprite_app import handler
import requests, json

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
    pass

  @with_setup(__start_server, __stop_server)
  def test_get_request(self):
    r = app.request('/')
    assert_equal(r.status, '200 OK')

  @with_setup(__start_server, __stop_server)
  def test_get_reponse(self):
    r = app.request('/')
    assert_is_not_none(r.data)

  @with_setup(__start_server, __stop_server)
  def test_receive_request_from_provider(self):
    r = app.request('/', 'GET', data=self.data, host='0.0.0.0:8080')
    assert_equals(r.status, '200 OK')


  @with_setup(__start_server, __stop_server)
  def test_respond_to_request(self):
    r = app.request('/', 'GET', data=self.data, host='0.0.0.0:8080')
    assert_equal(r.data, 'Thank you for notifying us!')


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
  

