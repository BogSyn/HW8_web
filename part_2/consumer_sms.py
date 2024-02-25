import pika
import json
import os
import sys
from mongoengine import connect
from models import Contact


def main():
    # Підключення до RabbitMQ
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue', durable=True)    # Черга

    # Функція зворотного виклику для обробки повідомлень від RabbitMQ
    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        contact_id = message['contact_id']

        # Отримання контакту з MongoDB
        contact = Contact.objects.get(id=contact_id)
        print(f"Received message for contact {contact.name}")

        # Імітація відправлення електронної пошти (заглушка)
        print(f"Sending sms to {contact.phone}")

        # Оновлення поля контакту після відправлення sms
        contact.sms_sent = True
        contact.save()

        print(f"SMS sent to {contact.phone}. Contact updated.")

    # Опрацювання повідомлень з RabbitMQ
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages...')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)