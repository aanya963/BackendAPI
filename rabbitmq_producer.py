import pika
import json

def publish_log(log):
    # 🔌 Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    # 📦 Create queue (safe if already exists)
    channel.queue_declare(
        queue='logs_queue',
        durable=True,
        arguments={
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": "dead_logs_queue"
        }
    )

    # also create DLQ
    channel.queue_declare(queue='dead_logs_queue', durable=True)

    # 📤 Send message
    channel.basic_publish(
        exchange='',
        routing_key='logs_queue',
        body=json.dumps(log),
        properties=pika.BasicProperties(
            delivery_mode=2  # makes message persistent
        )
    )
    

    print("📤 [PRODUCER] Sent:", log)

    connection.close()