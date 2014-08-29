# -*- coding: utf-8 -*-
import logging
from tornado_routes import route

from basehandler import BaseHandler
from forms.auth import RegisterForm, LoginForm
from models.account import AccountDB

url_base = 'account'

def tmpl(url):
    return '%s/%s.html' % (url_base, url)


@route('register', name='register')
class Register(BaseHandler):
    def get(self):
        self.context.update({'title': u'Регистрация',
                        'form': RegisterForm()
                        })
        self.render(tmpl('register'))

    
    def post(self, *args, **kwargs):
        form = RegisterForm(self.request.arguments)
        
        if form.validate():
            
            if AccountDB.check_email(form.email.data):
                AccountDB.create(form.data)
                self.render(tmpl('register_need_approve'))
                return
            else:
                form.set_field_error('email', "email_occupied")
        
        self.context.update({'form': form})
        self.render(tmpl('register'))

@route('approve/(.*)', name='approve')
class Approve(BaseHandler):
    
    def get(self, approvecode):
        user_id = AccountDB.approve(approvecode)
        if user_id:
            self.set_user(user_id)
            self.render(tmpl('register_user'))
        else:
            self.render(tmpl('register_bad_code'))
        
        
@route('login', name='login')
class Login(BaseHandler):
    def get(self):
        self.context.update({'title': u'Вход',
                        'form': LoginForm()
                        })
        self.render(tmpl('login'))

    
    def post(self, *args, **kwargs):
        form = LoginForm(self.request.arguments)
        
        if form.validate():
            if AccountDB.check_email(form.email.data):    # если данный емейл не зарегистрирован
                form.set_field_error('email', 'not_found')
            else:
                a = AccountDB.check_password(form.data)
                if a:
                    timezone = self.get_argument('timezone', None)
                    self.session.set('timezone', timezone)
                    logging.info(u'%s таймзона' % timezone)
                    self.set_user(a)
                    self.set_alert('success', u'Вход выполнен успешно.')
                    self.redirect('/')
                    return
                else:
                    form.set_field_error('password', 'wrong_password')                    
        
        self.context.update({'form': form})
        self.render(tmpl('login'))
        
@route('logout', name='logout')
class Logout(BaseHandler):
    def get(self):
        self.set_user(None)
        self.render(tmpl('logout'))
        
