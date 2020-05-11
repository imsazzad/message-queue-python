# work on message bus in local machine

    We will cover the following
        - install kafka
        - create producer&consumer in kafka
        - install rabbitmq
        - create producer&consumer in rabbitmq
    

## install kafka

Docker is the fastest way to get your hands dirty with new software. I installed kafka in my local machine using docker image following [this tutorial](https://docs.confluent.io/current/quickstart/ce-docker-quickstart.html)
To save our time. follow these instructions

- Clone the confluentinc/cp-all-in-one GitHub repository and check out the 5.5.0-post branch.
    
        git clone https://github.com/confluentinc/cp-all-in-one
        cd cp-all-in-one
        git checkout 5.5.0-post

- Navigate to /cp-all-in-one/cp-all-in-one directory.

        cd cp-all-in-one/
 
 - Start Confluent Platform specifying two options: (-d) to run in detached mode and (--build) to build the Kafka Connect image with the source connector kafka-connect-datagen from Confluent Hub.
 
        docker-compose up -d --build
    output should be
        
        Creating network "cp-all-in-one_default" with the default driver
        Creating zookeeper ... done
        Creating broker    ... done
        Creating schema-registry ... done
        Creating rest-proxy      ... done
        Creating connect         ... done
        Creating ksql-datagen    ... done
        Creating ksql-server     ... done
        Creating control-center  ... done
        Creating ksqldb-cli      ... done
        
- Optional: Run this command to verify that the services are up and running.

        docker-compose ps

You should see the following:

     Name                    Command               State                Ports
    broker            /etc/confluent/docker/run        Up      0.0.0.0:29092->29092/tcp, 0.0.0.0:9092->9092/tcp
    connect           /etc/confluent/docker/run        Up      0.0.0.0:8083->8083/tcp,                                                              9092/tcp
    control-center    /etc/confluent/docker/run        Up      0.0.0.0:9021->9021/tcp
    ksqldb-cli        ksql http://localhost:8088       Up
    ksqldb-datagen    bash -c echo Waiting for K ...   Up
    ksqldb-server     /etc/confluent/docker/run        Up      0.0.0.0:8088->8088/tcp
    rest-proxy        /etc/confluent/docker/run        Up      0.0.0.0:8082->8082/tcp
    schema-registry   /etc/confluent/docker/run        Up      0.0.0.0:8081->8081/tcp
    zookeeper         /etc/confluent/docker/run        Up      0.0.0.0:2181->2181/tcp,
                                                               2888/tcp, 3888/tcp
If the state is not Up, rerun the docker-compose up -d command.

if you are restarting your docker run this command
    
    docker-compose up -d

You should see now your kafka web interface [here](http://localhost:9021/ ) 

- create your own topic. I created a topic with name 'sazzad_topic'

### create and run kafka consumer 
   create a __kafka-consumer.py__ file with this content and run it. It will then wait for message to consume.
   
    from kafka import KafkaConsumer
    from json import loads
    
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
            print(message)
    consume_msg()


### create and run kafka producer 
   create a __kafka-producer.py__ file with this content and run it. It will then produce message and the above consumer will consume message.
   
    from time import sleep
    from json import dumps
    from kafka import KafkaProducer
    
    
    def produce_msg():
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))
    
        print("---------------- produced message by kafkamq producer ------------")
        for e in range(10):
            data = {'number' : e}
            print(data)
            producer.send('sazzad_topic', value=data)
            sleep(1)
    
    
    produce_msg() 


- if you run both produer and consumer output will be 

        ---------------- consumed message by kafkamq consumer ------------
        {'number': 0}
        {'number': 1}
        {'number': 2}
        {'number': 3}
        {'number': 4}
        {'number': 5}
        {'number': 6}
        {'number': 7}
        {'number': 8}
        {'number': 9}

## install rabbitmq

Here’s the command to get RabbitMQ 3 with Management UI running and ports 5672 and 15672 exposed:

    docker run -d --hostname my-rabbit -p 15672:15672 -p 5672:5672 --name rabbit-server -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password rabbitmq:3-management

Now open in your browser localhost:15672. The username is user and the password is password. You should see you rabbitmq server.

If you are running your container 2nd time command will be  
    
    docker start **CONTAINER ID**  
    
create your own queue. I created my_app. 


### create and run rabbitmq consumer 
   create a __rabbbitmq-consumer.py__ file with this content and run it. It will then wait for message to consume.

    import pika
    
    
    def consume_msg():
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials("user", "password")))
        channel = connection.channel()
    
    
        def callback(ch, method, properties, body):
            print(f'{body} is received')
    
    
        channel.basic_consume(queue="my_app", on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    
    consume_msg()
### create and run rabbitmq producer 
   create a __rabbbitmq-producer.py__ file with this content and run it. It will then wait for message to consume.

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
    
    RabbitMqProducer().produce_msg()
    
- if you run both produer and consumer output will be 

        b"{'body': 'this is body', 'other_prop': 'asas'}" is received
        
   
## Advanced
