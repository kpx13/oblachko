# -*- coding: utf-8 -*-

from base import connection, BaseDocument

MODULES = ['user',
           'bill',
           'template',
           'task']

@connection.register
class Counter(BaseDocument):
    """ Счётчик для разных моделей, используется для авто-инкремента """
    
    __collection__ = 'counter'
    __title__ = u'Счётчик'

    skeleton = {'_id': unicode,
                'seq': int    }

    @staticmethod
    def initial():
        """ Необходимо запустить при создании БД (если можно так назвать), и только 1 раз """
        for key in MODULES:
            connection.Counter({'_id': key, 'seq': 1}).save()
    
    
    @staticmethod
    def create_if_not_exists():
        """ Добавляет ключи если их ещё нет """
        for key in MODULES:
            if connection.Counter.find({'_id': key}).count() == 0:
                connection.Counter({'_id': key, 'seq': 1}).save() 

    @staticmethod
    def insert(name):   
        """ Инкрементирует счётчик и возращает новое значение. """            
        return connection.Counter.find_and_modify(query={'_id': name}, update={'$inc': {'seq': 1}})['seq']

    @staticmethod
    def reset_key(key):
        """ Сброс ключа """
        connection.Counter({'_id': key, 'seq': 1}).save()
    
    @staticmethod
    def next_key(key):
        """ Индекс следующего элемента """
        return connection.Counter.find_one({'_id': key})['seq']
        
    @staticmethod    
    def load_testdata():
        for key in MODULES:
            Counter.reset_key(key)
            
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Количество элементов', 'seq')]
        