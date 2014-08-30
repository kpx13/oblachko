# -*- coding: utf-8 -*-

import pika
import json
import logging
import sys
import smtplib, os
sys.path.append('/var/www/ann/data/oblachko')
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import xlsxwriter
from models.record import RecordDB
from datetime import datetime


def send_mail(email, subject, text):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('noreply@webgenesis.ru', 'noreply13')
    msg = MIMEText(text.encode('utf-8'), 'html')
    msg['Subject'] = subject.encode('utf-8')
    msg['From'] = 'oblachko'
    msg['To'] = email
    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    
def send_mail_with_attach(email, subject, text, files=[]):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('noreply@webgenesis.ru', 'noreply13')
        
    msg = MIMEMultipart()
    msg['From'] = 'oblachko'
    msg['To'] = email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject.encode('utf-8')

    msg.attach( MIMEText(text.encode('utf-8'), 'html') )

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(f, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)

    s.sendmail(msg['From'], [msg['To']], msg.as_string())
    s.close()


PER_FILE = 1000

def get_list_for_export(filter_dict, page):
    "Возращает отпагинированный список для модели db_model и страницы page_num"
    cursor = RecordDB.get_id_cursor(filter_dict)
    items = [RecordDB.get_middle(x.id) for x in cursor.skip(page * PER_FILE).limit(PER_FILE)]
    return items

def export_list_to_excel(list_, filename_base, page):
    filename = '/var/www/ann/data/oblachko/media/%s_%d.xlsx' % (filename_base, page)
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    worksheet.write(0, 0, u'Наименование', bold)
    worksheet.write(0, 1, u'Полное наименование', bold)
    worksheet.write(0, 2, u'Краткое наименование', bold)
    worksheet.write(0, 3, u'Руководитель', bold)
    worksheet.write(0, 4, u'Должность руководителя', bold)
    worksheet.write(0, 5, u'Дата регистрации', bold)
    worksheet.write(0, 6, u'Регион', bold)
    worksheet.write(0, 7, u'Юридический Адрес', bold)
    worksheet.write(0, 8, u'Фактический Адрес', bold)
    worksheet.write(0, 9, u'Телефон', bold)
    worksheet.write(0, 10, u'Веб-сайт', bold)
    worksheet.write(0, 11, u'E-mail', bold)
    worksheet.write(0, 12, u'ОКАТО', bold)
    worksheet.write(0, 13, u'Отрасль', bold)
    worksheet.write(0, 14, u'ОKВЭД', bold)
    worksheet.write(0, 15, u'ОКПО', bold)
    worksheet.write(0, 16, u'ИНН', bold)
    worksheet.write(0, 17, u'ОГРН', bold)
    worksheet.write(0, 18, u'КПП', bold)

    for i in range(0, len(list_)):
        worksheet.write(i + 1, 0, list_[i]['naimenovanie'])
        worksheet.write(i + 1, 1, list_[i]['polnoe-naimenovanie'])
        worksheet.write(i + 1, 2, list_[i]['kratkoe-naimenovanie'])
        worksheet.write(i + 1, 3, list_[i]['rukovoditel'])
        worksheet.write(i + 1, 4, list_[i]['dolzhnost-rukovoditelya'])
        worksheet.write(i + 1, 5, list_[i]['data-registratsii'])
        worksheet.write(i + 1, 6, list_[i]['region'])
        worksheet.write(i + 1, 7, list_[i]['yuridicheskij-adres'])
        worksheet.write(i + 1, 8, list_[i]['fakticheskij-adres'])
        worksheet.write(i + 1, 9, list_[i]['telefon'])
        worksheet.write(i + 1, 10, list_[i]['veb-sajt'])
        worksheet.write(i + 1, 11, list_[i]['e-mail'])
        worksheet.write(i + 1, 12, list_[i]['okato'])
        worksheet.write(i + 1, 13, list_[i]['otrasl'])
        worksheet.write(i + 1, 14, list_[i]['okved'])
        worksheet.write(i + 1, 15, list_[i]['okpo'])
        worksheet.write(i + 1, 16, list_[i]['inn'])
        worksheet.write(i + 1, 17, list_[i]['ogrn'])
        worksheet.write(i + 1, 18, list_[i]['kpp'])


    workbook.close()
    return filename

def send_export(filter_dict, email):
    count_all = RecordDB.get_count(filter_dict)
    pages_all = count_all / PER_FILE + 1
    filenames = []
    filename_base = 'base_' + datetime.now().strftime('%d.%m.%Y _%H:%M')
    for p in range(0, pages_all):
        filenames.append(export_list_to_excel(get_list_for_export(filter_dict, p), filename_base, p))

    body = ""
    if 'papka' in filter_dict:
        body = body + u'Регион: %s<br />' % filter_dict['papka']['$regex'][2:-2]
    if 'okved' in filter_dict:
        body = body + u'ОКВЭД: %s<br />' % filter_dict['okved']['$regex'][2:-2]
    if 'otrasl' in filter_dict:
        body = body + u'Отрасль: %s<br />' % filter_dict['otrasl']['$regex'][2:-2]
    body = body + u'Файлы во вложении.'

    send_mail_with_attach(email,
                        u'База',
                        body,
                        filenames)



def callback(ch, method, properties, body):
    logging.debug(" [x] Received")
    event = json.loads(body)
    if event['action'] == 'send_mail':
        data = event['data']
        if data['files']:
            send_mail_with_attach(data['email'], data['subject'], data['body'], data['files'])
        else:
            send_mail(data['email'], data['subject'], data['body'])
        logging.debug('MAIL SENT to %s' % event['data']['email'])
    elif event['action'] == 'send_export':
        data = event['data']
        send_export(data['filter_dict'], data['email'])
        logging.debug('EXPORT SENT to %s' % data['email'])


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='oblachko_queue')

print ' [*] Waiting for messages. To exit press CTRL+C'
    
channel.basic_consume(callback, queue='oblachko_queue', no_ack=True)
channel.start_consuming()
