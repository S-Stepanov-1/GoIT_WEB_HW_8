import pika
from faker import Faker
import random

from models import MyContacts

# connect to RabbitMQ cloud
credentials = pika.PlainCredentials('krtqqhgg', 'qsovfvrnb6nkHUyjVUSe9wWeMv8g-79p')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='cow.rmq2.cloudamqp.com', port=5672, credentials=credentials,
                              virtual_host='krtqqhgg'))
channel = connection.channel()

# declare exchange and queue
channel.exchange_declare(exchange='Message Handler', exchange_type='direct')
channel.queue_declare(queue='Email', durable=True)  # Email queue
channel.queue_declare(queue='SMS', durable=True)  # SMS queue

channel.queue_bind(exchange='Message Handler', queue='Email')  # bind queue 'Email' and exchange
channel.queue_bind(exchange='Message Handler', queue='SMS')  # bind queue 'SMS' and exchange


def put_into_queue(contact):
    if contact.preferred_sending == "Email":
        channel.basic_publish(exchange="Message Handler", routing_key="Email", body=str(contact.id).encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))

    elif contact.preferred_sending == "SMS":
        channel.basic_publish(exchange="Message Handler", routing_key="SMS", body=str(contact.id).encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))


def generate_contacts():
    fake = Faker()

    # generate 100 contacts and save them to DB
    for _ in range(10):
        new_contact = MyContacts(fullname=fake.name(), email=fake.email(), message=fake.text(),
                                 preferred_sending=random.choice(["Email", "SMS"]))
        new_contact.save()
        put_into_queue(new_contact)  # put a contact_id in RabbitMQ queue

    connection.close()  # close connection with RabbitMQ


def main():
    generate_contacts()


if __name__ == '__main__':
    main()
