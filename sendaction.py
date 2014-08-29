# -*- coding: utf-8 -*-

import pika
import json

from settings import jinja_env

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='oblachko_queue')


def send_html_mail(email, subject, template_name, context):
    send_mail_by_queue(email, subject, jinja_env.get_template(template_name).render(context))

def send_mail_by_queue(email, subject, body, files=[]):
    channel.basic_publish(exchange='',
                          routing_key='oblachko_queue',
                          body=json.dumps({ 'action': 'send_mail',
                                            'data': {
                                                        'email': email,
                                                        'subject': subject,
                                                        'body': body,
                                                        'files': files,
                                                    }}))


def check_text_on_unique(db_name, object_id, text):
    channel.basic_publish(exchange='',
                          routing_key='oblachko_queue',
                          body=json.dumps({ 'action': 'check_text_on_unique',
                                            'data': {
                                                        'db_name': db_name,
                                                        'object_id': object_id,
                                                        'text': text,
                                                    }}))

def send_export(filter_dict, email):
    channel.basic_publish(exchange='',
                          routing_key='oblachko_queue',
                          body=json.dumps({ 'action': 'send_export',
                                            'data': {
                                                        'email': email,
                                                        'filter_dict': filter_dict,
                                                    }}))