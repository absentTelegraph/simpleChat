import os
import random
import tornado.ioloop
from tornado import web
from tornado import websocket
from tornado.options import define, options, parse_command_line

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True
}

clients = []

class SocketHandler(websocket.WebSocketHandler):
    def open(self):
        self.name = hex(random.randint(1048576, 16777215))
        clients.append(self)
        self.write_message("* Welcome!")
        for client in clients:
            if not client is self:
                client.write_message("* " + str(self.name) + " joined")
        print "WebSocket opened - " + str(self.name)

    def on_message(self, message):
        self.write_message("You: " + message)
        for client in clients:
            if not client is self:
                client.write_message(str(self.name) + ") " + message)

    def on_close(self):
        clients.remove(self)
        for client in clients:
            if not client is self:
                client.write_message("* " + str(self.name) + " left")
        print "WebSocket closed - " + str(self.name)

class WebHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

if __name__ == "__main__":
    parse_command_line()
    application = web.Application([
        (r"/", WebHandler),
        (r"/websocket/?", SocketHandler),
    ], **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()