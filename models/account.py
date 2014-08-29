# -*- coding: utf-8 -*-

from bson.objectid import ObjectId
import datetime
import hashlib

from base import connection, BaseDocument, db_bool_repr, db_link_repr
from user import UserDB


def get_hash(password):
    return hashlib.sha256(password).hexdigest()

def get_approve_code(a):
    return a['email'] + str(a['_id'])[:10] + a['password_hash'][:10]

@connection.register
class AccountDB(BaseDocument):
    
    __collection__ = 'account'
    __title__ = u'Аккаунт'
    
    skeleton = {
                    'user': ObjectId,
                    'email': unicode,
                    'password_hash': unicode,
                    'date_registry': datetime.datetime,
                }
    
    @property
    def name(self):
        return self['email']
    
    @staticmethod
    def check_email(email):
        return connection.AccountDB.find_one({'email': email}) is None
    
    @staticmethod
    def check_password(data):
        a = connection.AccountDB.find_one({'email': data['email'], 
                                           'password_hash': get_hash(data['password'])})
        if a:
            return a['user']
        else:
            return None
    
    @classmethod
    def create(cls, data):
        a = connection.AccountDB()
        a['email'] = data['email']
        a['password_hash'] = get_hash(data['password'])
        a['date_registry'] = datetime.datetime.utcnow()
        a['user'] = None
        a.save()
        
        from units.export import send_html_mail
        send_html_mail(data['email'], 
                  u'Подтверждение аккаунта LifeRacing',
                  'account/email_approve.html', 
                  {'approve_code': a.approve_code})
        return a
    
    @property
    def approve_code(self):
        return get_approve_code(self)
    
    @staticmethod
    def approve(approve_code):
        email = approve_code[:-20]
        a = connection.AccountDB.find_one({'email': email})
        if not a:
            return False
        if a['user'] is not None:
            return False
        if a.approve_code == approve_code:
            a['user'] = UserDB.create()['_id']
            a.save()
            return a['user']
        else:
            return False
    
    def change_password(self, data):
        self['password_hash'] = get_hash(data['password'])
        self.save()
        
    def update(self, data):
        self.change_password(data)
    
    """ Работа с модулем db """
    
    @staticmethod
    def get_table_cols():
        return [(u'Email', 'email'),
                (u'Дата регистрации', 'date_registry'),
                (u'Акт.', 'db_is_active'),
                (u'Юзер', 'db_userlink')]
    
    @property
    def db_is_active(self):
        return db_bool_repr(self['user'])
    
    @property
    def db_userlink(self):
        return db_link_repr(UserDB, self['user'])
