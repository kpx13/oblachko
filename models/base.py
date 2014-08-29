# -*- coding: utf-8 -*-
import json
from datetime import datetime
from random import randrange
from mongolite import Connection, Document
from bson.objectid import ObjectId
import logging

import settings

connection = Connection()

logging.info(u'Работаем с базой данных %s.' % settings.get('db_name'))

class BaseDocument(Document):
    __database__ = settings.get('db_name')
    __title__ = u'Тайтл не установлен!'
    __short_fields__ = []

    @property
    def id(self):
        """ Возвращает айдишник из БД. Тип - ObjectID """
        return self['_id']

    @property
    def name(self):
        """ Имя сущности, по умолчанию  выводится айдишник"""
        if 'name' in self.__class__.skeleton:
            return self['name']
        else:
            return str(self.id)

    @classmethod
    def con(cls):
        # returns connection
        return connection[cls.__name__]

    @classmethod
    def create(cls):
        "Создаёт пустой документ"
        a = cls.con()()
        a.save()
        return a

    @classmethod
    def create_from_data(cls, data):
        new_obj = cls.create()
        cls.update_obj_from_data(new_obj, data)
        return new_obj

    @classmethod
    def get_id_cursor(cls, filter={}):
        return cls.con().find(filter, fields=['_id', 'order']).sort('order', 1)

    @classmethod
    def get_cursor(cls, filter={}, fields=None):
        if fields:
            return cls.con().find(filter, fields=fields + ['order']).sort('order', 1)
        else:
            return cls.con().find(filter).sort('order', 1)

    @classmethod
    def get_one(cls, filter={}, fields=None):
        if fields:
            return cls.con().find_one(filter, fields=fields)
        else:
            return cls.con().find_one(filter)

    @classmethod
    def get_count(cls, filter={}):
        """ Возвращает кол-во объектов под заданному типу """
        return cls.con().find(filter).count()

    @classmethod
    def update_obj_from_data(cls, obj, data):
        keys = cls.skeleton.keys()
        for k in keys:
            if k in data:
                if (cls.skeleton[k] == ObjectId) and type(data[k]) != ObjectId:
                    if data[k]:
                        obj[k] = ObjectId(data[k])
                    else:
                        obj[k] = None
                elif (cls.skeleton[k] == list) and type(data[k]) == unicode:
                    obj[k] = json.loads(data[k])
                else:
                    obj[k] = data[k]
        obj.save()
    
    @classmethod
    def exists(cls, _id):
        return bool(cls.get_one({'_id': ObjectId(_id)}))
    
    @classmethod
    def get_by_id(cls, _id):
        return cls.get_one({'_id': ObjectId(_id)})
    
    @classmethod
    def get_data_by_id(cls, _id):
        return dict(cls.get_one({'_id': ObjectId(_id)}))
    
    @classmethod
    def get_full(cls, _id):
        return cls.get_data_by_id(_id)

    @classmethod
    def update_order(cls, items_order):
        items = [cls.get_by_id(i) for i in items_order]
        last_orders = [i.order for i in items]
        last_orders.sort()
        # todo сделать здесь обработку для None

        for ind in range(0, len(items)):
            items[ind]['order'] = last_orders[ind]
            items[ind].save()

    @property
    def order(self):
        if 'order' in self and self['order']:
            return self['order']
        elif 'id' in self and self['id']:
            return self['id']
        else:
            return None

    @property
    def full(self):
        return dict(self)
    
    @classmethod
    def get_middle(cls, _id):
        return cls.get_data_by_id(_id) 
    
    @classmethod
    def get_short(cls, _id):
        return cls.get_data_by_id(_id)
    
    @classmethod
    def get_random(cls):
        count = cls.get_count()
        if count > 1:
            return cls.get_cursor().skip(randrange(1, count)).limit(1)[0]
        else: 
            return cls.get_one()
    
    @classmethod
    def get_table_by_user(cls, user_id):
        # todo где используется?
        if 'user' in cls.skeleton:
            return cls.get_cursor({'user': user_id}, cls.__short_fields__)
        else:
            logging.warning(u'Ключ %s не обнаружен в skeleton. Класс %s' % ('user', cls.__name__))

    def update(self, data):
        self.__class__.update_obj_from_data(self, data)

    @classmethod
    def load(cls, doc):
        return connection[cls.__name__](doc=doc).save()


    @classmethod
    def delete_all(cls):
        """ Удаляет все объекты """
        for obj in cls.get_id_cursor():
            obj.delete()

    @staticmethod
    def load_initial_data():
        pass


def search_object(obj_id, available_types):
    u"Выполняет поиск объекта по нескольким коллекциям"
    for db_name in available_types:
        curr = connection[db_name].find_one({'_id': ObjectId(obj_id)})
        if curr:
            return curr
    return None