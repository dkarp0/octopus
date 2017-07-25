import json
import os

import requests
import sqlalchemy
import tornado.ioloop
import tornado.template
import tornado.web
from sqlalchemy.orm import sessionmaker

import models
import page_parser


class Handler(tornado.web.RequestHandler):
    loader = None
    session = None

    def initialize(self):
        super().initialize()
        self.loader = tornado.template.Loader('templates')
        self.session = self.init_session()

    @staticmethod
    def init_session():
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            engine = sqlalchemy.create_engine(os.getenv('SQLALCHEMY_DATABASE_URI', ''))
        else:
            engine = sqlalchemy.create_engine('sqlite:///test.db')

        models.Base.metadata.create_all(engine)
        return sessionmaker(bind=engine, autoflush=False)()


class MainHandler(Handler):
    def get(self):
        self.set_status(200)
        self.write(self.loader.load("main.html").generate())

    def post(self):
        self.set_status(200)
        url = self.get_body_argument('url')
        word_counts = page_parser.Parser.parse(requests.get(url).content)
        self.write(self.loader.load("wordcloud.html").generate(url=url, word_counts=json.dumps(word_counts)))
        self.finish()

        models.save(word_counts, self.session)


class AdminHandler(Handler):
    def post(self):
        key = self.request.files['key'][0]['body']
        try:
            words = models.get(self.session, key)
        except (ValueError, TypeError):
            self.write('Please make sure to upload the correct Private Key')
            self.set_status(403)
            return

        self.set_status(200)
        self.write(self.loader.load("list.html").generate(words=words))

    def get(self):
        self.set_status(200)
        self.write(self.loader.load("admin.html").generate())


def make_app():
    return tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
        (r"/", MainHandler),
        (r"/admin/", AdminHandler),
        (r"/_ah/health", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
