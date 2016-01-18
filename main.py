from __future__ import division
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import datetime
from tornado import gen

from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)

client_message = 0


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = set()
    def open(self):
        self.connections.add(self)
        print 'new connection'
        for con in self.connections:
            con.write_message("Another connection!")

    def on_message(self, message):
        m = message.split(',')
        alpha = int(m[0])
        beta = int(m[1])
        msg_type = m[2]
        print 'Alpha: %s Beta: %s' %(alpha, beta)
        if msg_type == 'COORD':
            for con in self.connections:
                con.write_message("COORD:%s,%s" %(alpha, beta))
        elif msg_type == 'FIRE!':
            for con in self.connections:
                con.write_message("FIRE!:%s,%s" %(alpha, beta))


    def on_close(self):
        print 'connection closed'

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler)
        ]
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port,address='0.0.0.0')
    print "Listening on port:", options.port
    main_loop = tornado.ioloop.IOLoop.instance()
    #main_loop.add_timeout(datetime.timedelta(seconds=2), test)
    #tornado.ioloop.PeriodicCallback(counter.increment, 2).start()
    main_loop.start()
