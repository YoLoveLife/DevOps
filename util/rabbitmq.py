# -*- coding: utf-8 -*-
import pika
credentials = pika.PlainCredentials('QbPre','QB24Hour')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.200.76.36',8081,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='testHA',durable=True,exclusive=False, auto_delete=False)

#生产者
channel.basic_publish(exchange='',
                  routing_key='hello',
                  body='Hello World!')
print("开始队列")
connection.close()

# 消费者
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % body)
#
# channel.basic_consume(callback,
#                       queue='testHA',
#                       no_ack=True)
# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()