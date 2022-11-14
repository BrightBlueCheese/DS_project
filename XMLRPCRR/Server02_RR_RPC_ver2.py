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

# Identical to the one in the Server02 - This system has to find the prime numbers at the server side
# The function to find any valid (hidden) prime number b/w outcome_01[-1] and outcome_02[-1]
def balancer(outcome_01_last, outcome_02_last, extra_prime_list=list()):

    indicator = 0 
    # 1 : extra_prime_list is the complement for outcome_02
    # 2 : extra_prime_list is the complement for outcome_01

    if outcome_01_last > outcome_02_last:
        # try to find the next prime
        num1 = outcome_02_last + 4 
        # to inform which condition
        indicator = 2 # << extra_prime_list is the complement of outcome_02

        while outcome_01_last > num1:
            if isPrime(num1) and num1 == 2:
                extra_prime_list.append(num1)
                num1 = findNextPrime_RR(num1+1)

            elif isPrime(num1):
                extra_prime_list.append(num1)
                num1 = findNextPrime_RR(num1)

            elif not isPrime(num1):
                num1 = findNextPrime_RR(num1)

    elif outcome_01_last < outcome_02_last:
        # try to find the next prime
        num1 = outcome_01_last + 4
        # to inform which condition 
        indicator = 1 # << extra_prime_list is the complement of outcome_01

        while num1 < outcome_02_last:
            if isPrime(num1) and num1 == 2:
                extra_prime_list.append(num1)
                num1 = findNextPrime_RR(num1+1)

            elif isPrime(num1):
                extra_prime_list.append(num1)
                num1 = findNextPrime_RR(num1)

            elif not isPrime(num1):
                num1 = findNextPrime_RR(num1)

    return extra_prime_list, indicator

server = SimpleXMLRPCServer(("localhost", 8012))
print("Listening on port 8012...")

server.register_function(isPrime, "isPrime")
server.register_function(findNextPrime_RR, "findNextPrime_RR")
# server.register_function(findPrimeUntilDesired_SV_01, "findPrimeUntilDesired_SV_01")
server.register_function(findPrimeUntilDesired_SV_02, "findPrimeUntilDesired_SV")
server.register_function(balancer, 'balancer')

if __name__ == '__main__':
    try:
        print('Serving...')
        server.serve_forever()
    
    except KeyboardInterrupt:
        print('Exiting')


# python Server_RPC.py