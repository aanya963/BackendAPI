import pika
import json

connection = None
channel = None


def init_rabbitmq():
    global connection, channel

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )

    channel = connection.channel()

    channel.queue_declare(
        queue='logs_queue',
        durable=True,
        arguments={
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": "dead_logs_queue"
        }
    )

    channel.queue_declare(queue='dead_logs_queue', durable=True)

    print("🐰 RabbitMQ initialized")


def publish_log(log):
    if not channel:
        raise Exception("RabbitMQ not initialized")

    channel.basic_publish(
        exchange='',
        routing_key='logs_queue',
        body=json.dumps(log),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    print("📤 [PRODUCER] Sent:", log)