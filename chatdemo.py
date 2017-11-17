# coding:utf-8
# Created by yang
import uuid

import datetime
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import tornado.websocket
import logging
from tornado.options import define, options

define("port", default=8883, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True
        )

        super(Application, self).__init__(handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        ChatSocketHandler.waiters.remove(self)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        logging.info("got parsed %r", parsed)
        # self.username = parsed["username"]
        self.username = parsed.get("username")
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed.get("body"),
            "type": "message",
            # "client_id": self.client_id,
            "username": self.username,
            "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))
        ChatSocketHandler.send_updates(chat)

    @classmethod
    def send_updates(cls, chat): #向所有客户端发送聊天信息
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)


def main():
    tornado.options.parse_command_line()
    app=Application()
    app.listen(options.port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.current().stop()
    except Exception:
        pass

if __name__ == '__main__':
    main()

