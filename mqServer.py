# Server for messaging prime number server
# Author: Dr. Jan Woerner
# CSC 444 Distributed Systems
# Creation date: 09/15/2022

# imports
import math
import pika
from pika.adapters.blocking_connection import BlockingChannel

# declare variables
reconnect_on_failure = True # with this it is controlled whether the server reconnects on failure to RabbitMQ


# determine a number is prime
def isPrime(number):
    i: int = 0;
    for i in range(2, int(math.sqrt(number)) + 1):
        if (number % i) == 0:
            return False;
    return True;


# find the next prime number
def findNextPrime(x):
    number: int = x + 1;
    while not isPrime(number):
        number += 1;
    return number;


def consumer(connection, channel):
   # channel.exchange_declare(exchange='findPrimeIn', exchange_type='direct')
   # result = channel.queue_declare(queue='fPrimeIn', exclusive=True)
   # channel.queue_bind(exchange='findPrimeIn', queue='fPrimeIn')
    print(' [*] Waiting for findPrimeIn. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print('Server was called with: {}'.format(body.decode()))
        primenum:str = str(findNextPrime(int(body.decode())))
        print('Server puts {} into the fPrimeOut queue ...'.format(primenum))
        # return the found prime number by putting it into the out-queue
        ch.basic_publish(exchange='findPrimeOut', routing_key='primeOut', body=primenum)
        # print('yes')

    channel.basic_consume(queue='fPrimeIn', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def getConnectionAndChannel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('jan', 'Crypto007')))
    ch = connection.channel()
    return connection,ch

def startServer(reconnect_on_failure):
    connection, channel = getConnectionAndChannel()
    # start the server's consumer to listen to the fPrimeIn-queue
    consumer(connection, channel)
    if reconnect_on_failure:
        # close the connection and channel if something is broken
        if not connection.is_closed():
            connection.close()
        if not channel.is_close():
            channel.close()
        # reestablish the connection!
        startServer(reconnect_on_failure)


print('Server started ... \n')
startServer(reconnect_on_failure)