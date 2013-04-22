from paste.fixture import TestApp
from nose.tools import *
from shoprite_app import app

class TestCode():
  def setup(self):
    middleware = []
    self.testApp = TestApp(app)

  def test_invalid_page_request(self):
    r = self.testApp.get('/', expect_errors=True)
    r.mustcontain('Invalid')
    assert_equal(400, r.status)

  def test_receive_push_sms(self):
    url = ''
    data = {
        'sender' : '0827824665',
        'text'   : '53543298',
        'timestamp' :'2013'
        }

    response = self.testApp.get('/', data, headers={ 'Content-Type': 'text/plain'}, status=200)
    
