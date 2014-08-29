#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='lr_dev_queue')

channel.basic_publish(exchange='',
                      routing_key='lr_dev_queue',
                      body='Hello World!')
print " [x] Sent 'Hello World!'"

