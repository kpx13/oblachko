# -*- coding: utf-8 -*-

import logging

from bson.objectid import ObjectId
from base import BaseDocument, connection, db_link_repr
from counter import Counter
from models.requisites import RequisitesDB
from models.emailsettings import EmailSettingsDB

@connection.register
class UserDB(BaseDocument):
    
    __collection__ = 'userdb'
    __title__ = u'Юзер'
    
    skeleton = {
                    'id': int,
                    'requisites': ObjectId,     # реквизиты
                    'emailsettings': ObjectId,  # email настройки
                }
    

    @staticmethod
    def create():
        a = connection.UserDB()
        a['id'] = Counter.insert('user')
        a['requisites'] = RequisitesDB.create()['_id']
        a['emailsettings'] = EmailSettingsDB.create()['_id']
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
    def get_table_cols():
        return [(u'Id', 'id'),
                (u'Реквизиты', 'db_requisiteslink'),
                (u'Настройки email', 'db_emailsettingslink')]
    
    @property
    def db_requisiteslink(self):
        return db_link_repr(RequisitesDB, self['requisites'])
    
    @property
    def db_emailsettingslink(self):
        return db_link_repr(EmailSettingsDB, self['emailsettings'])
