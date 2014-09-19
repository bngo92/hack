import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("client.html")


class MusicHandler(tornado.web.RequestHandler):
  def get(self):
    self.set_header('Content-Type', 'audio/mpeg')
    self.write(open('paradise.mp3', 'rb').read())


class WSHandler(tornado.websocket.WebSocketHandler):
  connections = set()

  def check_origin(self, origin):
    return True

  def open(self):
    print('new connection')
    WSHandler.connections.add(self)

  def on_message(self, message):
    print('message received %s' % message)
    for connection in WSHandler.connections:
      connection.write_message(message)

  def on_close(self):
    print('connection closed')
    WSHandler.connections.remove(self)


application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/music', MusicHandler),
  (r'/ws', WSHandler),
])


if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
