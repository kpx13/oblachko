# -*- coding: utf-8 -*-
from tornado import web
from tornado_routes import route

from basehandler import BaseHandler, authorized
from models.user import UserDB

url_base = 'user'

def tmpl(url):
    return '%s/%s.html' % (url_base, url)


@route('profile', name='profile')
class Profile(BaseHandler):
    
    @authorized
    def get(self):
        self.context.update({'title': u'Профиль',
                             'user': UserDB.get_full(self.user_obj['_id'])
                        })
        self.render(tmpl('profile'))