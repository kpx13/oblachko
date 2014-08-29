# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_bool_repr, db_link_repr
from bson.objectid import ObjectId
from counter import Counter
import datetime

@connection.register
class BillDB(BaseDocument):
    
    __collection__ = 'bill'
    __title__ = u'Счёт'
    
    skeleton = {
                    'id': int,
                    'user': ObjectId,
                    'contractor': ObjectId, # контрагент
                    'template': ObjectId,   # шаблон, если есть
                    'task': ObjectId,       # задание, если есть
                    'content': ObjectId,    # содержимое
                    'number': int,          # номер счёта
                    'date_created': datetime.datetime,  # дата, когда был создан (и отправлен)
                    'send': bool,            # отправлен
                    'paid': bool,            # оплачен
                }
    @property
    def name(self):
        from content import ContentDB
        return ContentDB.get_by_id(self['content']).name
    
    @staticmethod
    def create_simple(user_id, contractor_id, content_id, number, date_created):
        b = connection.BillDB()
        b['user'] = user_id
        b['contractor'] = contractor_id
        b['content'] = content_id
        b['number'] = number
        b['date_created'] = date_created
        b['id'] = Counter.insert('bill')
        b.save()
        return b
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Id', 'id'),
                (u'Юзер', 'db_user'),
                (u'Контрагенты', 'db_contractors'),
                (u'Содержимое', 'db_content'),
                (u'Отправлен', 'db_send'),
                (u'Оплачен', 'db_paid'),]
    
    
    @property
    def db_user(self):
        from user import UserDB
        return db_link_repr(UserDB, self['user'])
    
    @property
    def db_content(self):
        from content import ContentDB
        return db_link_repr(ContentDB, self['content'])
    
    @property
    def db_contractors(self):
        from contactor import ContactorDB
        return db_link_repr(ContactorDB, self['contractor'])
    
    @property
    def db_send(self):
        return db_bool_repr(self['send'])
    
    @property
    def db_paid(self):
        return db_bool_repr(self['paid'])
    