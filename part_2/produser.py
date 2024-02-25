import pika

import json
from faker import Faker

from models import Contact


# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Оголошення біржі та черг
channel.exchange_declare(exchange='send_exchange', exchange_type='direct')     # Біржа

queues = ['email_queue', 'sms_queue']
for queue_name in queues:
    channel.queue_declare(queue=queue_name, durable=True)                   # Черга
    channel.queue_bind(exchange='email_exchange', queue=queue_name)         # З'єднуємо біржу та черги (біндінг)


# Генерація фейкових контактів та публікація повідомлень в RabbitMQ
fake = Faker('uk-Ua')


if __name__ == '__main__':
    for _ in range(20):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        contact = Contact(name=name, email=email, phone=phone)
        contact.save()

        message = {'contact_id': str(contact.id)}

        for queue_name in queues:
            channel.basic_publish(exchange='email_exchange', routing_key=queue_name, body=json.dumps(message).encode())
            print(f"Sent message for contact {name}")

    connection.close()
