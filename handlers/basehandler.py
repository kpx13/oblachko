# -*- coding: utf-8 -*-
import logging
import json
import tornado.web
from pycket.session import SessionMixin
from settings import jinja_env
from common import filter_list
from models.record import RecordDB
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

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
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



class ListHandler(BaseHandler):

    def get(self):
        start_time = time.time()
        self.page = int(self.get_argument('page', 1))
        self.filter_dict = {}
        """
        self.category = self.get_argument('category', None)
        self.tag = self.get_argument('tag', None)
        if self.category:
            self.filter_dict['category'] = ObjectId(self.category)
            print 'category', self.filter_dict['category']
        if self.tag:
            # в списке тегов встречается данный
            self.filter_dict['tags'] = {'$in': [self.tag]}

        self.context.update({'category': self.category,
                             'tag': self.tag,
                             'url_base': self._url})
        """

        self.context.update({'title': u'Все записи в базе данных',
                             'req_time': (time.time() - start_time) * 1000})
        #self.search()
        self.context.update(filter_list(RecordDB, self.page, self.filter_dict))
        self.render('list.html')

class DetailsHandler(BaseHandler):
    def get(self, record_id):
        item = RecordDB.get_full(record_id)
        self.context.update({
            'title': item['polnoe-naimenovanie'],
            'item': item
        })
        self.render('details.html')