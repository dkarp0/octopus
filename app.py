import json

import requests
import tornado.ioloop
import tornado.template
import tornado.web

import page_parser


class Handler(tornado.web.RequestHandler):
    loader = None

    def initialize(self):
        super().initialize()
        self.loader = tornado.template.Loader('templates')


class MainHandler(Handler):
    def get(self):
        self.set_status(200)
        self.write(self.loader.load("main.html").generate())


class WordCloudHandler(Handler):
    def post(self):
        self.set_status(200)
        url = self.get_body_argument('url')
        word_counts = page_parser.Parser.parse(requests.get(url).content)
        self.write(self.loader.load("wordcloud.html").generate(url=url, word_counts=json.dumps(word_counts)))


def make_app():
    return tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
        (r"/", MainHandler),
        (r"/wordcloud/", WordCloudHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
