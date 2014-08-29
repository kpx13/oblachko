# -*- coding: utf-8 -*-
import logging
import json
import tornado.web
from pycket.session import SessionMixin
from settings import jinja_env

from models.user import UserDB

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
        self.__start_time = time.time()
        super(BaseHandler, self).initialize(**kwargs)
        self.context = { 
               'alerts': self.get_alerts(),
               'title': u'Заглушка',
               'user': self.user_obj,
               'uri': self.request.uri,
            }
        if self.user_id:
            self.context.update({'user_id': self.user_id})
            
    def on_finish(self):
        #statprof.stop()
        #statprof.display(open('reports/profiling/%s' % self.__class__.__name__, 'w'))
        self.__duration_time = (time.time() - self.__start_time) * 1000  # msec
        open('reports/profiling/handlers', 'a').write('%24s%16.3f\n' % (self.__class__.__name__, self.__duration_time))

    
    def render(self, template):
        self.context.update(self.get_template_namespace())
        self.write(jinja_env.get_template(template).render(self.context))
        self.xsrf_token
        self.flush()
        
    @property
    def is_ajax(self):
        request_x = self.request.headers.get('X-Requested-With')
        return request_x == 'XMLHttpRequest'

    def render_json(self, data):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data))
    
    # мои функции
    def set_alert(self, atype, text):
        alerts = [a for a in self.session.get('alerts', [])] # глубокое копирование 
        alerts.append((atype, text))    # добавляем ещё один
        self.session.set('alerts', alerts)  
    
    def get_alerts(self):
        alerts = [a for a in self.session.get('alerts', [])] # глубокое копирование 
        self.session.set('alerts', [])  # удаляем все
        return alerts
    
    def set_user(self, acc_id):
        if acc_id:
            self.session.set('user_id', acc_id)
        else:
            self.session.set('user_id', None) # logout
    
    @property
    def user_obj(self):
        u_id = self.session.get('user_id', None)
        if u_id:
            return UserDB.get_by_id(u_id)
        else:
            return None
    
    @property
    def user_id(self):
        return self.session.get('user_id', None)


class Home(BaseHandler):
    
    def get(self):
        self.render('home.html')
    
    
class TestBill(BaseHandler):
    
    def get(self):
        from units.documents import create_context, create_bill, create_pdf_bill
        from models.requisites import RequisitesDB
        from datetime import datetime
        from units.export import send_mail_by_queue
        
        sender = RequisitesDB.get_one({'inn': '772160030650'})
        recipient = RequisitesDB.get_one({'inn': '7729687715'})
        bill_num = 156
        date = datetime.now()
        items = [{  'name': u'Услуги по поддержке сайта за май 2014г',
                    'unit': u'мес.',      
                    'count': 1,
                    'price': 10000  },
                 {  'name': u'Оплата хостинга',
                    'unit': u'мес.',      
                    'count': 6,
                    'price': 250  },
                 {  'name': u'За красивые глаза',
                    'unit': u'шт.',      
                    'count': 2,
                    'price': 666.6  }]
        
        context = create_context(sender, recipient, bill_num, date, items)
        self.write(create_bill(context))
        self.xsrf_token
        self.flush()
        create_pdf_bill(context, 'asdf.pdf')
        send_mail_by_queue('annkpx@gmail.com', u'Привет!', create_bill(context))
