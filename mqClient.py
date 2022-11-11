# client for messaging prime number server
# Author: Dr. Jan Woerner
# CSC 444 Distributed Systems
# Creation date: 09/15/2022

import pika

# declare variables
reconnect_on_failure = True
i: int = 1;

# consumer of the client
def consumer(connection, channel):
    # if binding did not happen you can do that dynamically here by uncommenting the following lines:
    # channel.exchange_declare(exchange='findPrimeIn', exchange_type='direct')
    # result = channel.queue_declare(queue='fPrimeIn', exclusive=True)
    # channel.queue_bind(exchange='findPrimeIn', queue='fPrimeIn')
    print('[*] Waiting for prime numbers from the server To exit press CTRL+C\n')

    def callback(ch, method, properties, body):
        global i
        primenum = int(body)
        print('{},'.format(primenum), end=' ')
        # create a nice looking output so carriage return every 20 numbers
        if i % 20 ==0:
            print()
        primenum += 1
        primestr:str = str(primenum)
        # we only want the client to ask for the given amount of numbers after that we want the client to stop execution
        if i <= num2:
            ch.basic_publish(exchange='findPrimeIn', routing_key='primeIn', body=primestr)
        else:
            print()
            quit()
        i += 1
    # the client waits and listens for the server putting something on the out queue
    channel.basic_consume(queue='fPrimeOut', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

# establish the connection to the RabbitMQ
def getConnectionAndChannel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', 5672, '/', pika.PlainCredentials('jan', 'Crypto007')))
    ch = connection.channel()
    return connection, ch

# start the client and reestablish the connection if getting lost
def startClient(reconnect_on_failure):
    connection, channel = getConnectionAndChannel()
    # start the client consumer
    consumer(connection, channel)
    # check the reconnect
    if reconnect_on_failure:
        #  close the connection and channel and restart the client in case of broken connection
        if not connection.is_closed():
            connection.close()
        if not channel.is_close():
            channel.close()
        startClient(reconnect_on_failure)


# prompt the user for the input
num1: int = int(input('Enter the start number:'))
num2: int = int(input('Enter the amount of prime numbers:'))
# the following line wouldn't be needed if the input was changed!
numberStr:str = str(num1)

print('Establsih connection to RabbitMQ ... \n')
# open the connection, send the first number to the server and close the connection again and then start the client
connection, channel = getConnectionAndChannel()

channel.basic_publish(exchange='findPrimeIn', routing_key='primeIn', body=numberStr)
print('First message, {}, successfully put into fPrimeIn-queue ... \n'.format(numberStr))
connection.close()
print('Client starts ... \n')
startClient(reconnect_on_failure)