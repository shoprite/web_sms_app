from nose.tools import *
from shoprite_app import app 

class TestHandler:
  """ Tests for the handler class
  """

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
    assert_equal(r.data,'Received')


