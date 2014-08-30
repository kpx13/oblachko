# -*- coding: utf-8 -*-
import logging
import json
import tornado.web
from settings import jinja_env
from common import filter_list
from models.record import RecordDB
from sendaction import send_export
import time

def authorized(method):
    """ Декоратор, проверяющий, авторизован юзер или нет """
    def wrapper(self, *args, **kwargs):
        user = self.user_id
        if not user:
            self.redirect('/account/login')
            return
        return method(self, *args, **kwargs)
    return wrapper

class BaseHandler(tornado.web.RequestHandler):
    """ Базовый обработчик """

    # перезаписанные функции
    def initialize(self, **kwargs):
        #statprof.start()
        super(BaseHandler, self).initialize(**kwargs)
        self.context = {
               'title': u'Заглушка',
               'uri': self.request.uri,
            }
    
    def render(self, template):
        self.context.update(self.get_template_namespace())
        self.write(jinja_env.get_template(template).render(self.context))
        self.xsrf_token
        self.flush()

    def render_json(self, data):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data))


def get_filter_request(key, value):
    if value:
        return {key: {'$regex': ".*%s.*" % value}}
    else:
        return {}

class ListHandler(BaseHandler):

    def get(self):
        start_time = time.time()
        self.page = int(self.get_argument('page', 1))
        self.filters = {
            'otrasl': self.get_argument('otrasl', ''),
            'okved': self.get_argument('okved', ''),
            'region': self.get_argument('region', ''),
        }

        self.filter_dict = {}
        self.filter_dict.update(get_filter_request('otrasl', self.filters['otrasl']))
        self.filter_dict.update(get_filter_request('okved', self.filters['okved']))
        self.filter_dict.update(get_filter_request('papka', self.filters['region']))

        self.context.update({'title': u'Все записи в базе данных',
                             'req_time': (time.time() - start_time) * 100000,
                             'filters': self.filters})

        self.context.update(filter_list(RecordDB, self.page, self.filter_dict))
        self.render('list.html')

class ExportHandler(BaseHandler):

    def post(self):
        start_time = time.time()
        self.filters = {
            'otrasl': self.get_argument('otrasl', ''),
            'okved': self.get_argument('okved', ''),
            'region': self.get_argument('region', ''),
        }

        self.filter_dict = {}
        self.filter_dict.update(get_filter_request('otrasl', self.filters['otrasl']))
        self.filter_dict.update(get_filter_request('okved', self.filters['okved']))
        self.filter_dict.update(get_filter_request('papka', self.filters['region']))
        send_export(self.filter_dict, self.get_argument('email', ''))
        self.redirect('/')

class DetailsHandler(BaseHandler):
    def get(self, record_id):
        item = RecordDB.get_full(record_id)
        self.context.update({
            'title': item['polnoe-naimenovanie'],
            'item': item
        })
        self.render('details.html')
