#! /usr/bin/env python3

import tornado.ioloop
import tornado.web
import tornado.concurrent
import subprocess

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')

def subprocess_handler(request_handler, to_run):
    proc = subprocess.Popen(
        [to_run],
        stdout=subprocess.PIPE,
        shell=True
    )

    for line in iter(proc.stdout.readline,''):
        html = line.rstrip().decode('utf-8') + '<br/>\n'
        request_handler.write(html)
        yield tornado.gen.sleep(0.1)
        yield request_handler.flush()

class FooHandler(tornado.web.RequestHandler):
    def initialize(self, start):
        self.start = start

    @tornado.gen.coroutine
    def get(self):
        foo = self.start
        while True:
            foo += 1
            self.write(str(foo)+'<br>')
            yield tornado.gen.sleep(0.1)
            yield self.flush()

class VaderHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        return subprocess_handler(self, './cowsay-vader.sh')

class DragonHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        return subprocess_handler(self, './cowsay-fun.sh')

if __name__ == '__main__':
    application = tornado.web.Application([
        (r'/', MainHandler),
        (r'/foo', FooHandler, dict(start=2)),
        (r'/dragon', DragonHandler),
        (r'/vader', VaderHandler)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
