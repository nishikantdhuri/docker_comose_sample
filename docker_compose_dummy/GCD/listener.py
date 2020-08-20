import pika
import time
import os
conn=None
import requests
import logging

def connect():
    credentials = pika.PlainCredentials('testuser', 'pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host'),credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('sender_queue'),durable=True)
    return channel


if __name__=='__main__':
    # os.environ['mq_host'] = '192.168.99.100'
    # os.environ['tracer_ip'] = '127.0.0.1'
    # os.environ['sleep_time'] = str(60)
    # os.environ['receiver_queue'] = 'gcd1'
    # os.environ['sender_queue'] = 'gcd2'
    # os.environ['src_system'] = 'gcd'
    time.sleep(20)
    logging.basicConfig(filename=str(os.environ.get('src_system')) + '.log', filemode='w',
                        format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info('connecting to mq ' + str(os.environ.get('receiver_queue')))
    credentials = pika.PlainCredentials('testuser', 'pass')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ.get('mq_host'),credentials=credentials,heartbeat=120))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get('receiver_queue'),durable=True)


    def sleep():
        time.sleep(int(os.environ.get('sleep_time')))

    def callback(ch, method, properties, body):
        logging.info('messag received')
        dictToSend = {'status': os.environ.get('src_system')}
        requests.post('http://'+str(os.environ.get('tracer_ip'))+':'+str(5000)+'/soc', json=dictToSend)
        logging.info('Processing..')
        sleep()
        logging.info('Processing completed')
        logging.info('Sending message to ' + str(os.environ.get('sender_queue')) + 'from ' + str(
            os.environ.get('src_system')))
        conn = connect()
        conn.basic_publish(body=os.environ.get('src_system'), exchange='', routing_key=os.environ.get('sender_queue'))
        conn.close()

    channel.basic_consume(queue =os.environ.get('receiver_queue'),auto_ack = True,on_message_callback = callback)
    logging.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()