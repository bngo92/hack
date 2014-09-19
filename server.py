import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.write(open("client.html").read())


class WSHandler(tornado.websocket.WebSocketHandler):

  def check_origin(self, origin):
    return True

  def open(self):
    print 'new connection'
    self.write_message("Hello World")

  def on_message(self, message):
    print 'message received %s' % message
    self.write_message(message)

  def on_close(self):
    print 'connection closed'


application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
])


if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()