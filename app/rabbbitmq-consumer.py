# rabbbitmq-consumer.py
# Consume RabbitMQ queue
from json import dumps
from time import sleep

import pika
from kafka import KafkaProducer


class MyKafkaProducer:
    def produce_msg(self, data):

        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))

        print("---------------- produced message by kafkamq producer ------------")
        if data is None:
            for e in range(10):
                data = {'number' : e}
                print(data)
                producer.send('sazzad_topic', value=data)
                sleep(1)
        else:
            print("got data from Rabbitmq consumer " ,data)
            producer.send('sazzad_topic', value=data)
            sleep(1)


def consume_msg():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
    channel = connection.channel()


    def callback(ch, method, properties, body):
        string = body##.decode('utf-8')
        print(string)
        import json
        msg = json.loads(string)
        print( msg, ' is received from rabbitmq producer')
        MyKafkaProducer().produce_msg(msg)
        # print(f'{body} is received')


    channel.basic_consume(queue="my_app", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

consume_msg()