from kafka import KafkaConsumer
from json import loads


import pika


class RabbitMqProducer:
    def produce_msg(self, msg = None):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('user', 'password')))
        channel = connection.channel()
        if not msg:
            msg = {"body": "this is body",
                     "other_prop": "asas"
                     }

        channel.basic_publish(exchange='my_exchange', routing_key='test', body=str(msg))

        connection.close()
        print("done!!")


def consume_msg():

    consumer = KafkaConsumer(
        'sazzad_topic',
         bootstrap_servers=['localhost:9092'],
         auto_offset_reset='earliest',
         enable_auto_commit=True,
         group_id='my-group',
         value_deserializer=lambda x: loads(x.decode('utf-8')))

    print("---------------- consumed message by kafkamq consumer ------------")
    for message in consumer:
        message = message.value
        import json
        # print(json.dumps(message))
        print(message)
        RabbitMqProducer().produce_msg(json.dumps(message))

consume_msg()



