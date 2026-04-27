import pika
import json
import requests

import time

def callback(ch, method, properties, body):
    log = json.loads(body)

    # get retry count from headers
    headers = properties.headers or {}
    retry_count = headers.get("x-retry", 0)

    print(f"\n🚀 [WORKER] Received (retry={retry_count}):", log)

    try:
        res = requests.post(
            "http://localhost:5124/api/Logs",
            json=log
        )

        if res.status_code == 200:
            print("📡 Success")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            raise Exception("API failed")

    except Exception as e:
        print("❌ Error:", e)

        if retry_count >= 5:
            print("💀 Max retries reached → sending to DLQ")

            ch.basic_publish(
                exchange='',
                routing_key='dead_logs_queue',
                body=body
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            print("🔁 Retrying...")

            ch.basic_publish(
                exchange='',
                routing_key='logs_queue',
                body=body,
                properties=pika.BasicProperties(
                    headers={"x-retry": retry_count + 1}
                )
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    # same queue name
    channel.queue_declare(queue='logs_queue', durable=True)

    print("🟢 [WORKER] Waiting for messages...")

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue='logs_queue',
        on_message_callback=callback
    )

    channel.start_consuming()


if __name__ == "__main__":
    start_worker()