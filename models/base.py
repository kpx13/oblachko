# -*- coding: utf-8 -*-
from mongolite import Connection, Document
from bson.objectid import ObjectId
from tornado.options import options as tornado_options_dict
import settings
import logging

connection = Connection()

logging.info(u'Работаем с базой данных %s.' % settings.get('db_name'))

class BaseDocument(Document):
    __database__ = settings.get('db_name')
    __title__ = u'Тайтл не установлен!'
    __short_fields__ = []
    
    @property
    def name(self):
        """ Имя сущности, по умолчанию  выводится айдишник"""
        return str(self['_id'])
    
    @property
    def for_select(self):
        return (str(self['_id']), self.name)
    
    @classmethod
    def get_for_select(cls):
        return [ u.for_select for u in connection[cls.__name__].find() ]
    
    @classmethod
    def create(cls):
        a = connection[cls.__name__]()
        a.save() 
        return a
    
    @classmethod
    def create_from_data(cls, data):
        new_obj = connection[cls.__name__]()
        keys = cls.skeleton.keys()
        for k in keys:
            if k in data:
                if cls.skeleton[k] == ObjectId:
                    new_obj[k] = ObjectId(data[k])
                else:
                    new_obj[k] = data[k]
            else:
                logging.warning(u'Ключ %s не обнаружен в skeleton. Класс %s' % (k, cls.__name__))
        if 'id' in keys:
            from counter import Counter
            new_obj['id'] = Counter.insert(cls.__collection__)       
        new_obj.save() 
        return new_obj
    
    @classmethod
    def get_title(cls):
        return cls.__title__
    
    @classmethod
    def get_db_name(cls):
        return cls.__collection__
    
    @classmethod
    def exists(cls, _id):
        return connection[cls.__name__].find_one({'_id': ObjectId(_id)})
    
    @classmethod
    def get_by_id(cls, _id):
        return connection[cls.__name__].find_one({'_id': ObjectId(_id)})
    
    @classmethod
    def get_data_by_id(cls, _id):
        return dict(connection[cls.__name__].find_one({'_id': ObjectId(_id)}))
    
    @classmethod
    def get_full(cls, _id):
        return cls.get_data_by_id(_id) 
    
    @classmethod
    def get_middle(cls, _id):
        return cls.get_data_by_id(_id) 
    
    @classmethod
    def get_short(cls, _id):
        return cls.get_data_by_id(_id)
    
    @classmethod
    def get_random(cls):
        from random import randrange
        count = connection[cls.__name__].find().count()
        if count > 1:
            return connection[cls.__name__].find().skip(randrange(1, count)).limit(1)[0]
        else: 
            return connection[cls.__name__].find_one()
    
    @classmethod
    def get_list(cls):
        """ Возвращает список всех объектов """
        return [x for x in connection[cls.__name__].find()]
    
    @classmethod
    def get_table_by_user(cls, user_id):
        if 'user' in cls.skeleton:
            return connection[cls.__name__].find({'user': user_id}, fields=cls.__short_fields__)
        else:
            logging.warning(u'Ключ %s не обнаружен в skeleton. Класс %s' % ('user', cls.__name__))
    
    @classmethod
    def get_cursor(cls, filter={}, fields=None):
        if fields:
            return connection[cls.__name__].find(filter, fields=fields)
        else:
            return connection[cls.__name__].find(filter)
        
    @classmethod
    def get_one(cls, filter={}, fields=None):
        if fields:
            return connection[cls.__name__].find_one(filter, fields=fields)
        else:
            return connection[cls.__name__].find_one(filter)
    
    @classmethod
    def load(cls, doc):
        return connection[cls.__name__](doc=doc).save()
    
    @classmethod
    def get_count(cls):
        """ Возвращает кол-во всех объектов """
        return connection[cls.__name__].find().count()
    
    def update(self, data):
        keys = self.skeleton.keys()
        for k in keys:
            if k in data:
                if self.skeleton[k] == ObjectId:
                    if data[k]:
                        self[k] = ObjectId(data[k])
                else:
                    self[k] = data[k] # TODO сделать проверку на наличие ф-ции update_key
        self.save()
    
    
    @classmethod
    def delete_all(cls):
        """ Удаляет все объекты """
        for x in connection[cls.__name__].find():
            x.delete()
    
    @staticmethod
    def get_table_cols():
        return []
    
    
    @classmethod
    def get_db_info(cls):
        return {
                    'db_name': cls.__collection__,
                    'name': cls.__title__,
                    'count': connection[cls.__name__].find().count(),
                }
        
    
    @classmethod    
    def load_testdata(cls):
        cls.delete_all()


def db_bool_repr(value):
    if value:
        return """<i class="fa fa-check text-success text"></i>"""
    else:
        return """<i class="fa fa-times text-danger text"></i>"""

def db_link_repr(model, obj_id):
    if obj_id:
        return u'<a href="/db/%s/full/%s">%s >>></a>' % (model.get_db_name(), obj_id, model.get_by_id(obj_id).name)

