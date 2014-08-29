# -*- coding: utf-8 -*-

from base import BaseDocument, connection, db_bool_repr

@connection.register
class PeriodicDB(BaseDocument):
    
    __collection__ = 'periodic'
    __title__ = u'Периодичность'
    
    skeleton = {
                    'time_h': int,  # время: часы
                    'time_m': int,  # время: минуты
                    'week': list,   # список из дней недели. пр: 1, 0, 0, 1, 0, 0, 0
                    'month': list,  # число месяца
                    'count': int,   # кол-во отправленных
                    'active': bool, # задание активно
                }
    
    @property
    def name(self):
        return self.db_dates + u' в ' + self.db_time
    
    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Даты', 'db_dates'),
                (u'Время', 'db_time'),
                (u'Отправлено', 'count'),
                (u'Активно', 'db_active')]
    
    @property
    def db_dates(self):
        if self['month']:
            return u'По %s числам месяца' % self['month']
        else:
            return u'Дни недели: %s' % ', '.join(self['week']) 
    
    @property
    def db_time(self):
        return u"%02d:%02d" % (self['time_h'], self['time_m'])
    
    @property
    def db_active(self):
        return db_bool_repr(self['active'])
    
    