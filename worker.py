import pika
import json
import requests

# 🔁 Process each message
def callback(ch, method, properties, body):
    log = json.loads(body)

    # retry count from headers
    headers = properties.headers or {}
    retry_count = headers.get("x-retry", 0)

    print(f"\n🚀 [WORKER] Received (retry={retry_count}):", log)

    try:
        # 📡 Send to .NET API
        res = requests.post(
            "http://localhost:5124/api/Logs",
            json=log,
            timeout=5
        )

        if res.status_code == 200:
            print("📡 [WORKER] Success → saved to DB")
            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            raise Exception(f"API failed with {res.status_code}")

    except Exception as e:
        print("❌ [WORKER] Error:", e)

        if retry_count >= 5:
            print("💀 [WORKER] Max retries → sending to DLQ")

            ch.basic_publish(
                exchange='',
                routing_key='dead_logs_queue',
                body=body
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            print("🔁 [WORKER] Retrying...")

            ch.basic_publish(
                exchange='',
                routing_key='logs_queue',
                body=body,
                properties=pika.BasicProperties(
                    headers={"x-retry": retry_count + 1},
                    delivery_mode=2  # persistent
                )
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    # 🔌 Connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    # ✅ IMPORTANT: declare SAME config as producer
    channel.queue_declare(
        queue='dead_logs_queue',
        durable=True
    )

    channel.queue_declare(
        queue='logs_queue',
        durable=True,
        arguments={
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": "dead_logs_queue"
        }
    )

    print("🟢 [WORKER] Waiting for messages...")

    # process 1 message at a time (safe)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue='logs_queue',
        on_message_callback=callback
    )

    channel.start_consuming()


if __name__ == "__main__":
    start_worker()