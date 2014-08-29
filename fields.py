# -*- coding: utf-8 -*-

import pytils

list_fields = [
    u'Папка',
    u'Файл',
    u'Регион',

    u'Наименование',
    u'Полное наименование',
    u'Краткое наименование',
    u'Руководитель',
    u'Должность руководителя',
    u'Дата регистрации',
    u'Юридический Адрес',
    u'Фактический адрес',
    u'Телефон',
    u'Веб-сайт',
    u'E-mail',
    u'ОКАТО',
    u'Отрасль',
    u'ОKВЭД',
    u'ОКПО',
    u'ИНН',
    u'ОГРН',
    u'КПП',
]

#for l in list_fields:
#    print u"\t'%s': unicode," % pytils.translit.slugify(l)

#for l in list_fields:
#    print u"\t'%s': record_raw[]," % pytils.translit.slugify(l)

for l in list_fields:
    print "<dt>%s: </dt><dd>{{ item['%s'] }}</dd>" % (l, pytils.translit.slugify(l))