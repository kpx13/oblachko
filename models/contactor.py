# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_link_repr
from bson.objectid import ObjectId
from requisites import RequisitesDB
import logging

@connection.register
class ContactorDB(BaseDocument):
    
    __collection__ = 'contactor'
    __title__ = u'Контрагент'
    __short_fields__ = ['requisites', 'email', 'user']
    
    skeleton = {
                    'user': ObjectId,
                    'requisites': ObjectId, # реквизиты
                    'email': unicode,       # email
                    'comment': unicode,     # комментарий
                }
    
    @classmethod
    def create(cls, user_id, requisites_id, email='', comment=''):
        alr = cls.get_one({'user': user_id, 'requisites': requisites_id})
        if alr:
            logging.warning(u'Попытка создать дублирующего контрагента')
            return alr
        a = connection[cls.__name__]()
        a['user'] = user_id
        a['requisites'] = requisites_id
        a['email'] = email
        a['comment'] = comment
        a.save() 
        return a
    
    @property
    def name(self):
        try:
            return RequisitesDB.get_one({'_id': self['requisites']}, ['name'])['name']
        except:
            logging.error(u'Ошибка с целостностью данных: нет реквизитов для user_id = %s' % self['_id'])
            return 'ERROR'

    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_columns():
        return [(u'Название', 'name'),
                (u'Email', 'email')]
        
    @staticmethod
    def get_table_cols():
        return [(u'Юзер', 'db_user'),
                (u'Название', 'name'),
                (u'Email', 'email'),
                (u'Комментарий', 'comment')]
    
    @property
    def db_user(self):
        from user import UserDB
        return db_link_repr(UserDB, self['user'])
