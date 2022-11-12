from xmlrpc.server import SimpleXMLRPCServer
import math
import time

# determine a number is prime
def isPrime(number):
    i: int = 0;
    # 1 is not a prime number
    if number == 1:
        return False
    else:    
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

def findPrimeUntilDesired(num1, num2, prime_list=list()):

    # record starting time to calculate the process time

    while not num2 == len(prime_list):

        if isPrime(num1):
            prime_list.append(num1)
            num1 = findNextPrime(num1)

        elif not isPrime(num1):
            num1 = findNextPrime(num1)

    return prime_list

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")

server.register_function(isPrime, "isPrime")
server.register_function(findNextPrime, "findNextPrime")
server.register_function(findPrimeUntilDesired, "findPrimeUntilDesired")

if __name__ == '__main__':
    try:
        print('Serving...')
        server.serve_forever()
    
    except KeyboardInterrupt:
        print('Exiting')


# python Server_RPC.py