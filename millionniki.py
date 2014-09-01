# -*- coding: utf-8 -*-

import os
from bs4 import BeautifulSoup
from models.record import RecordDB

import sys

REGIONS_FOLDER = u'/var/www/ann/data/oblachko/bases/ErrorUpd'
ERRORS_FOLDER = u'/var/www/ann/data/oblachko/bases/ErrorFiles'
if len(sys.argv) == 2:
    INTERESTING_FOLDER = sys.argv[1].decode('utf-8')
else:
    INTERESTING_FOLDER = None
print INTERESTING_FOLDER

for dirname, dirnames, filenames in os.walk(REGIONS_FOLDER):
    #for subdirname in dirnames:
    #    print os.path.join(dirname, subdirname)[len(REGIONS_FOLDER) + 1:]

    for filename in filenames:
        folder_name = dirname[len(REGIONS_FOLDER) + 1:]
	if INTERESTING_FOLDER and (not folder_name.startswith(INTERESTING_FOLDER)):
            continue
        print u'Папка: ', folder_name
        file_name = filename
        print u'Файл: ', file_name

        if file_name.endswith('.html') or file_name.endswith('.htm'):
            #print u'Выполняется разбор файла...'
            soup = BeautifulSoup(open('/'.join([REGIONS_FOLDER, folder_name, file_name]), 'r').read())
	    print u"start... {'papka': '%s', 'fajl': '%s'}" % (folder_name, file_name)
	    can_remove = True
            for tr in soup.findAll('tr', attrs={'class' : 'ReportRow'}):
		try:
                    record_raw = [td.string for td in tr.findAll('td')]
		    if len(record_raw) > 25:
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
		    else:
			data = {
                    		'papka': folder_name,
                    		'fajl': file_name,
	                    	'naimenovanie': record_raw[0],
	                    	'polnoe-naimenovanie': record_raw[1],
	                    	'rukovoditel': record_raw[2],
	                    	'data-registratsii': record_raw[3],
	                    	'yuridicheskij-adres': record_raw[4],
	                    	'telefon': record_raw[5],
	                    	'region': record_raw[6],
	                    	'otrasl': record_raw[7]}
                    RecordDB.create_from_data(data)
		except:
                    print u'Ошибка в файле %s.' % u'/'.join([folder_name, file_name])
                    if not os.path.exists(u'/'.join([ERRORS_FOLDER, folder_name])):
                        os.makedirs(u'/'.join([ERRORS_FOLDER, folder_name]))
                    os.rename(u'/'.join([REGIONS_FOLDER, folder_name, file_name]), u'/'.join([ERRORS_FOLDER, folder_name, file_name]))
                    can_remove = False
                    break
	    if can_remove:
	        os.remove('/'.join([REGIONS_FOLDER, folder_name, file_name]))
	        print 'ok'
        else:
            print u'Непонятный формат. Файл не обработан.'
