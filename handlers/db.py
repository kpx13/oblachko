# -*- coding: utf-8 -*-
import logging
from tornado_routes import route
from bson.objectid import ObjectId

from basehandler import BaseHandler

from forms.auth import RegisterForm
from forms.db import *

from models.common import *


def tmpl(url):
    return 'db/%s.html' % url

class BaseDBHandler(BaseHandler):
    _name = None    # название на латинице для шаблонов
    
    def initialize(self, **kwargs):
        super(BaseDBHandler, self).initialize(**kwargs)
        self.context.update({'module_name': self._name,
                             'modules_list': [(x.get_title(), x.get_db_name()) for x in MODULES_ALL]})

class BaseListHandler(BaseDBHandler):
    _model = None   
    
    def get(self):
        self.context.update({'title': u'%s | Cписок' % self._model.get_title(), 
                             'items': self._model.get_list(),
                             'count': self._model.get_count(),
                             'table_cols': self._model.get_table_cols()})
        self.render(tmpl('list'))

class BaseCreateHandler(BaseDBHandler):
    _model = None   
    _form = None    
    
    def get(self):
        self.context.update({'title': u'%s | Cоздание' % self._model.get_title(),
                             'form': self._form(),
                             'module_name': self._name})
        self.render(tmpl('create'))
        
    def post(self, *args, **kwargs):
        form = self._form(self.request.arguments)
        
        if form.validate():
            self.context.update({'title': u'%s | Cоздание' % self._model.get_title(),
                                 'item': self._model.create_from_data(form.data)})
            self.render(tmpl('full'))
        else:
            self.context.update({'title': u'%s | Cоздание | Ошибки' % self._model.get_title(),
                                 'form': form})
            self.render(tmpl('create'))

class BaseFullHandler(BaseDBHandler):
    _model = None   
    _template_name = tmpl('full')

    def get(self, _id):
        self.context.update({'title': u'%s | Детальная информация' % self._model.get_title(),
                             'item': self._model.get_full(_id),
                             'module_name': self._name})
        self.render(self._template_name)
        
class BaseMiddleHandler(BaseDBHandler):
    _model = None   
    _template_name = tmpl('middle')

    def get(self, _id):
        self.context.update({'title': u'%s | Представление middle' % self._model.get_title(),
                             'item': self._model.get_middle(_id),
                             'module_name': self._name})
        self.render(self._template_name)
        
class BaseShortHandler(BaseDBHandler):
    _model = None   
    _template_name = tmpl('short')

    def get(self, _id):
        self.context.update({'title': u'%s | Представление short' % self._model.get_title(),
                             'item': self._model.get_middle(_id),
                             'module_name': self._name})
        self.render(self._template_name)
        
class BaseEditHandler(BaseDBHandler):
    _model = None   
    _form = None    
    
    def get(self, _id):
        self.context.update({'title': u'%s | Редактирование' % self._model.get_title(),
                             'form': self._form(obj=self._model.get_data_by_id(_id)),
                             'module_name': self._name})
        self.render(tmpl('create'))
        
    def post(self, _id, *args, **kwargs):
        item = self._model.get_by_id(_id)
        form = self._form(self.request.arguments, obj=item)
        if form.validate():
            item.update(form.data)
            self.context.update({'title': u'%s | Редактирование' % self._model.get_title(),
                                 'item': item})
            self.render(tmpl('full'))
        else:
            self.context.update({'title': u'%s | Редактирование' % self._model.get_title(),
                                'form': form       })
            self.render(tmpl('create'))
            
class BaseDelHandler(BaseDBHandler):
    _model = None   
    
    def get(self, _id):
        self.context.update({'title': u'%s | Удаление TODO' % self._model.get_title(),
                             'item': self._model.get_by_id(_id),
                             'module_name': self._name })
        self.render(tmpl('full'))


def ClassFactory(attrs):
    model = attrs['model']
    name = model.get_db_name()
    form = None
    if 'form' in attrs:
        form = attrs['form']
        
    
    def add(name_postfix, base_handler, url_postfix):
        newclass = type(name + name_postfix , (base_handler, ), {})
        if 'override' in attrs:
            if name_postfix in attrs['override']:
                newclass = type(name + name_postfix , (base_handler, ), attrs['override'][name_postfix])
        newclass._name = name
        newclass._model = model
        newclass._form = form 
        newclass.route_params = {}
        newclass.url_name = None
        newclass.route_path = name + url_postfix
        return newclass
    
    result = [
                add('ListHandler', BaseListHandler, ''),
                add('DelHandler', BaseDelHandler, '/del/(.*)'),
                add('FullHandler', BaseFullHandler, '/full/(.*)'),
                add('MiddleHandler', BaseMiddleHandler, '/middle/(.*)'),
                add('ShortHandler', BaseShortHandler, '/short/(.*)'), 
           ]
    if form:
        result.extend([
                add('CreateHandler', BaseCreateHandler, '/create'),
                add('EditHandler', BaseEditHandler, '/edit/(.*)'),
            ])
    
    return result



"""                ACCOUNTS                """

def account_create_post(self):
    form = self._form(self.request.arguments)
    if form.validate():
        if AccountDB.check_email(form.email.data):
            a = AccountDB.create(form.data)
            self.context.update({'title': u'%s | Cоздание' % self._model.get_title(),
                                 'item': a})
            self.render(tmpl('full'))
            return
        else:
            form.set_field_error('email', "email_occupied")

    self.context.update({'title': u'%s | Cоздание | Ошибки' % self._model.get_title(),
                        'form': form       })
    self.render(tmpl('create'))

HANDLERS = [
                {'model': Counter, 'form': None},
                {'model': RequisitesDB, 'form': RequisitesForm},
                {'model': EmailSettingsDB, 'form': EmailSettingsForm},
                {'model': UserDB, 'form': UserForm},
                {'model': AccountDB, 'form': RegisterForm, 'override': {'CreateHandler': {'post': account_create_post}}},
                {'model': ContactorDB, 'form': ContractorForm},
                {'model': PeriodicDB, 'form': PeriodicForm},
                {'model': ContentDB, 'form': ContentForm},
                {'model': TemplateDB, 'form': TemplateForm},
                {'model': TaskDB, 'form': TaskForm},
                {'model': BillDB, 'form': BillForm},
            ]

additional_routes_list = []
for l in [ClassFactory(attrs) for attrs in HANDLERS]:
    additional_routes_list.extend(l)


@route('', name='dbindex')
class List(BaseDBHandler):
    _name='list'

    def get(self):
        self.context.update({'title': u'Список Коллекций',
                             'items': [ m.get_db_info() for m in MODULES_ALL ]})
        self.render(tmpl('collections'))


@route('dump')
class DumpHandler(BaseDBHandler):
    def get(self):
        create_dumps()
        self.set_alert('success', u'Выгрузка в файлы выполнена успешно.')
        self.redirect('/db')
        
@route('load')
class LoadHandler(BaseDBHandler):
    def get(self):
        load_from_dumps()
        self.set_alert('success', u'Загрузка базы данных из файлов выполнена успешно.')
        self.redirect('/db')

@route('reset')
class ResetHandler(BaseDBHandler):    
    def get(self):
        reset_all()
        self.redirect('/db')
