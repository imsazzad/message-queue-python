# rabbbitmq-producer.py
# This script will publish MQ message to my_exchange MQ exchange

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
        import json
        print(json.dumps(msg))
        channel.basic_publish(exchange='my_exchange', routing_key='test', body=json.dumps(msg))

        connection.close()
        print("done!!")

if __name__ == "__main__":
    RabbitMqProducer().produce_msg()

# docker run -d --hostname my-rabbit -p 15672:15672 -p 5672:5672 --name rabbit-server -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management
# docker start **CONTAINER ID**  - second time
