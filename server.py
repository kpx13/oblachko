# -*- coding: utf-8 -*-

import os
import tornado.ioloop
from tornado.web import StaticFileHandler
import tornado.web
import tornado.httpserver

from tornado.options import define
from tornado.options import options as tornado_options_dict
define("environment",   default="dev", help="environment")
define("port",          default=8000, type=int)

# TODO Я полагаю, что это безобразие с 
# сеттингсами и импортами надо отрефакторить.
tornado.options.parse_command_line()
import settings
URL_PREFIX = ''
CURR_PATH = os.path.dirname(os.path.realpath(__file__))

from handlers.basehandler import ListHandler, DetailsHandler, ExportHandler

class Application(tornado.web.Application):
    def __init__(self):
        
        req_handlers = [
            (r'/', ListHandler),
            (r'/details/(.*)', DetailsHandler),
            (r'/export', ExportHandler),
            (r'/static/(.*)', StaticFileHandler, {'path':  CURR_PATH + '/static'}),
            (r'/media/(.*)', StaticFileHandler, {'path': CURR_PATH + '/media'}),
            (r'/ico/(.*)', StaticFileHandler, {'path': CURR_PATH + '/static/images'}),
        ] 

        app_env = tornado_options_dict.environment
        app_settings = settings.app_options[ app_env ]
        app_settings.update(settings.default_app_options)

        tornado.web.Application.__init__(self, req_handlers, **app_settings)
        
    def period_run(self):
        pass


def main():
    try:
        app = Application()
        http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
        http_server.listen(tornado_options_dict.port)
        loop = tornado.ioloop.IOLoop.instance()
        loop.start()
    except KeyboardInterrupt:
        return

if __name__ == '__main__':
    main()


