# -*- coding: utf-8 -*-

from base import BaseDocument, connection

@connection.register
class RecordDB(BaseDocument):
    __collection__ = 'record'
    
    skeleton = {
        'papka': unicode,
        'fajl': unicode,
        'region': unicode,
        'naimenovanie': unicode,
        'polnoe-naimenovanie': unicode,
        'kratkoe-naimenovanie': unicode,
        'rukovoditel': unicode,
        'dolzhnost-rukovoditelya': unicode,
        'data-registratsii': unicode,
        'yuridicheskij-adres': unicode,
        'fakticheskij-adres': unicode,
        'telefon': unicode,
        'veb-sajt': unicode,
        'e-mail': unicode,
        'okato': unicode,
        'otrasl': unicode,
        'okved': unicode,
        'okpo': unicode,
        'inn': unicode,
        'ogrn': unicode,
        'kpp': unicode,

    }
    
    pass
