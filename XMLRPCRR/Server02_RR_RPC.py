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
def findNextPrime_RR(x):
    number: int = x + 4;
    while not isPrime(number):
        number += 4;
    return number;


    # if start from or more than from 3
# SV_01 3 7 11 15 19 23 27 31
# SV_02 5 9 13 17 21 25 29 33

    # if start from 2 or less than from 2
# SV_01 2 5 9 13 17 21 25 29 33
# SV_02 3 7 11 15 19 23 27 31



def findPrimeUntilDesired_SV_02(num1, num2, prime_list=list()):
    # SV_01 and SV_02 will each get half of computation
    # either 0 or 1 or 2, start from 3
    if num1 == 0 or num1 == 1 or num1 == 2:
        num1 = 3
    # when even number, make it odd number
    elif num1 % 2 == 0:
        num1 += 3
    else:
        num1 += 2
    # find NextPrime을 고쳐야 할 듯
    while not num2 == len(prime_list):

        if isPrime(num1) and num1 == 2:
            prime_list.append(num1)
            num1 = findNextPrime_RR(num1+1)

        elif isPrime(num1):
            prime_list.append(num1)
            num1 = findNextPrime_RR(num1)

        elif not isPrime(num1):
            num1 = findNextPrime_RR(num1)

    return prime_list

server = SimpleXMLRPCServer(("localhost", 8001))
print("Listening on port 8001...")

server.register_function(isPrime, "isPrime")
server.register_function(findNextPrime_RR, "findNextPrime_RR")
# server.register_function(findPrimeUntilDesired_SV_01, "findPrimeUntilDesired_SV_01")
server.register_function(findPrimeUntilDesired_SV_02, "findPrimeUntilDesired_SV_02")

if __name__ == '__main__':
    try:
        print('Serving...')
        server.serve_forever()
    
    except KeyboardInterrupt:
        print('Exiting')


# python Server_RPC.py