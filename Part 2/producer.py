import pika
import configparser
from faker import Faker
from mongoengine import connect

from models import MyContacts

# connect to RabbitMQ cloud
credentials = pika.PlainCredentials('krtqqhgg', 'qsovfvrnb6nkHUyjVUSe9wWeMv8g-79p')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='cow.rmq2.cloudamqp.com', port=5672, credentials=credentials,
                              virtual_host='krtqqhgg'))
channel = connection.channel()

# declare exchange and queue
channel.exchange_declare(exchange='Message Handler', exchange_type='direct')
channel.queue_declare(queue='Email', durable=True)
channel.queue_bind(exchange='Message Handler', queue='Email')  # bind queue and exchange


def connect_to_db():
    config = configparser.ConfigParser()
    config.read("../Part 1/config.ini")

    mongo_user = config.get('DB', 'user')
    mongodb_pass = config.get('DB', 'pass')
    db_name = "hw08_part2"

    connect(db=db_name,
            host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@stepanovdb.codnmzv.mongodb.net/?retryWrites=true&w=majority",
            ssl=True)


def put_into_queue(contact):
    channel.basic_publish(exchange="Message Handler", routing_key="Email", body=str(contact).encode(),
                          properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))


def generate_contacts():
    fake = Faker()

    # generate and save 100 contacts
    for _ in range(100):
        new_contact = MyContacts(fullname=fake.name(), email=fake.email())
        new_contact.save()

        contact_id = new_contact.id
        put_into_queue(contact_id)  # put a contact_id in RabbitMQ queue
    connection.close()  # close connection with RabbitMQ


def main():
    connect_to_db()
    generate_contacts()


if __name__ == '__main__':
    main()
