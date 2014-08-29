# -*- coding: utf-8 -*-

from base import BaseDocument, connection

@connection.register
class RequisitesDB(BaseDocument):
    
    __collection__ = 'requisites'
    __title__ = u'Реквизиты организации'
    
    skeleton = {
                    'name': unicode,            # название
                    'address': unicode,         # адрес
                    'inn': unicode,             # ИНН
                    'kpp': unicode,             # КПП
                    'bank_bik': unicode,        # БИК банка 
                    'bank_name': unicode,       # название банка
                    'bank_ks': unicode,         # корр. счет банка
                    'bank_account': unicode,    # расчетный счет
                    'accountant': unicode,      # ФИО бухгалтера
                }
    
    @property
    def name(self):
        return self['name']

    """ Вспомогательные функции для внутреннего использования """
    
    @staticmethod
    def get_table_cols():
        return [(u'Адрес', 'address'),]
