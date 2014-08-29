# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
from models.record import RecordDB
RecordDB.delete_all()

REGIONS_FOLDER = u'/home/kpx/evomailing/bases/Regiony'

for dirname, dirnames, filenames in os.walk(REGIONS_FOLDER):
    #for subdirname in dirnames:
    #    print os.path.join(dirname, subdirname)[len(REGIONS_FOLDER) + 1:]

    for filename in filenames[:3]:  # Пока берём только 3 файла!!!
        folder_name = dirname[len(REGIONS_FOLDER) + 1:]
        print u'Папка: ', folder_name
        file_name = filename
        print u'Файл: ', file_name

        if file_name.endswith('.html') or file_name.endswith('.htm'):
            print u'Выполняется разбор файла...'
            soup = BeautifulSoup(open('/'.join([REGIONS_FOLDER, folder_name, file_name]), 'r').read())
            for tr in soup.findAll('tr', attrs={'class' : 'ReportRow'}):
                record_raw = [td.string for td in tr.findAll('td')]
                data = {
                    'papka': folder_name,
                    'fajl': file_name,
                    'naimenovanie': record_raw[0],
                    'polnoe-naimenovanie': record_raw[1],
                    'kratkoe-naimenovanie': record_raw[2],
                    'rukovoditel': record_raw[3],
                    'dolzhnost-rukovoditelya': record_raw[4],
                    'data-registratsii': record_raw[6],
                    'yuridicheskij-adres': record_raw[7],
                    'fakticheskij-adres': record_raw[8],
                    'telefon': record_raw[9],
                    'veb-sajt': record_raw[11],
                    'e-mail': record_raw[12],
                    'region': record_raw[13],
                    'okato': record_raw[14],
                    'otrasl': record_raw[15],
                    'okved': record_raw[16],
                    'okpo': record_raw[22],
                    'inn': record_raw[23],
                    'ogrn': record_raw[24],
                    'kpp': record_raw[25],
                }
                print '\t', data['kratkoe-naimenovanie'], u'...ok'
                RecordDB.create_from_data(data)
        else:
            print u'Непонятный формат. Файл не обработан.'