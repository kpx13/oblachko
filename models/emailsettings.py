# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_bool_repr

@connection.register
class EmailSettingsDB(BaseDocument):
    
    __collection__ = 'email_settings'
    __title__ = u'Настройки почты'
    
    skeleton = {
                    'smtp_name': unicode,   # адрес сервера
                    'smtp_port': unicode,   # порт
                    'login': unicode,       # логин для почты
                    'password': unicode,    # пароль
                    'checked': bool,        # проверка пройдена
                }
    
    @property
    def name(self):
        return self['login']

    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'SMTP сервер', 'smtp_name'),
                (u'Проверено', 'db_is_checked'),
                ]

    @property
    def db_is_checked(self):
        return db_bool_repr(self['checked'])