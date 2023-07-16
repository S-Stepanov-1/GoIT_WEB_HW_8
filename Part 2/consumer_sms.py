import sys
import time
import pika

from models import MyContacts


def callback(ch, method, properties, body):
    contact_id = body.decode()

    contact = MyContacts.objects(id=contact_id, is_received=False).first()
    if contact:
        time.sleep(0.1)
        contact.update(set__is_received=True)
        print(f" [✔️] SMS is sent to {contact.fullname}")  # simulating of sending of an email message

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # connect to RabbitMQ cloud
    credentials = pika.PlainCredentials('krtqqhgg', 'qsovfvrnb6nkHUyjVUSe9wWeMv8g-79p')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='cow.rmq2.cloudamqp.com', port=5672, credentials=credentials,
                                  virtual_host='krtqqhgg'))
    channel = connection.channel()

    channel.queue_declare(queue='SMS', durable=True)  # connect to queue

    channel.basic_qos(prefetch_count=1)  # consumer should only request one message at any given time before processing it
    channel.basic_consume(queue='SMS', on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
