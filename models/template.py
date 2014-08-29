# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_link_repr
from bson.objectid import ObjectId
from content import ContentDB

@connection.register
class TemplateDB(BaseDocument):
    
    __collection__ = 'template'
    __title__ = u'Шаблон'
    
    skeleton = {
                    'id': int,
                    'user': ObjectId,
                    'name': unicode,        # название задания
                    'comment': unicode,     # комментарий
                    'content': ObjectId,    # содержимое
                }
    @property
    def name(self):
        return self['name']
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Id', 'id'),
                (u'Юзер', 'user'),
                (u'Название', 'name'),
                (u'Содержимое', 'db_content')]
    
    @property
    def db_content(self):
        return db_link_repr(ContentDB, self['content'])
    
    