from time import sleep
from json import dumps
from kafka import KafkaProducer


def produce_msg():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    print("---------------- produced message by kafkamq producer ------------")
    for e in range(3):
        import json
        data = json.dumps({"number" : e})
        print(data)
        producer.send('sazzad_topic', value=data)
        sleep(1)


produce_msg()


