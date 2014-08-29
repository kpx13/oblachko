# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_link_repr
from bson.objectid import ObjectId

@connection.register
class TaskDB(BaseDocument):
    
    __collection__ = 'task'
    __title__ = u'Задание'
    
    skeleton = {
                    'id': int,
                    'user': ObjectId,
                    'name': unicode,        # название задания
                    'comment': unicode,     # комментарий
                    'contractors': list,    # список контрагентов
                    'periodic': ObjectId,   # настройки периодичности
                    'template': ObjectId,   # шаблон
                    'send_count': int,      # кол-во отправленных по данному заданию
                }
    @property
    def name(self):
        return self['name']
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Id', 'id'),
                (u'Юзер', 'db_user'),
                (u'Название', 'name'),
                (u'Контрагенты', 'db_contractors'),
                (u'Периодичность', 'db_periodic'),
                (u'Отправлено', 'send_count')]
    
    @property
    def db_user(self):
        from user import UserDB
        return db_link_repr(UserDB, self['user'])
    
    @property
    def db_periodic(self):
        from periodic import PeriodicDB
        return db_link_repr(PeriodicDB, self['periodic'])
    
    @property
    def db_contractors(self):
        from contactor import ContactorDB
        return ', '.join([db_link_repr(ContactorDB, ObjectId(c)) for c in self['contractors']])
    
    