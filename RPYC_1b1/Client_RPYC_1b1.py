# Title : Client_RPYC_1b1.py
# Author : Youngmin Lee
# Date : Nov 14 2022
# Description : A Client that keeps sending positive integer to a Server and getting back prime numbers
#   which are confirmed by the Server. The Client and the Server interact for each integer

import rpyc
import time


conn = rpyc.connect('localhost', 8103)

# prompt the user for the input
num1: int = int(input('Enter the start number:'))

while num1 < 0:
    print('Negative integer ins not valid. Please try again.')
    num1: int = int(input('Enter the start number:'))

num2: int = int(input('Enter the amount of prime numbers:'))

while num2 <= 0:
    print('Please enter a valid number.')
    num2: int = int(input('Enter the amount of prime numbers:'))

# time recording start
time_start = time.time()

# a list to store the prime numbers
prime_list = []


def findPrimeUntilDesired_1b1(num1, num2):
    # case for num1 == 0, 1
    if num1 == 0 or num1 == 1:
        num1 = 2

    # case for even num1 except 2
    elif num1 != 2 and num1 % 2 == 0:
        num1 += 1

    # Sending num1 to the Server and save it until reaching to len(prime_list) == num2
    while not num2 == len(prime_list):
        
        if conn.root.isPrime(num1) and num1 == 2:
            prime_list.append(num1)
            num1 = conn.root.findNextPrime(num1-1)

        elif conn.root.isPrime(num1):
            prime_list.append(num1)
            num1 = conn.root.findNextPrime(num1)

        elif not conn.root.isPrime(num1):
            num1 = conn.root.findNextPrime(num1)

    return prime_list



# outcome = conn.root.findPrimeUntilDesired(num1, num2, prime_list)
outcome = findPrimeUntilDesired_1b1(num1, num2)
# outcome = conn.root.isPrime(3)
# print(f'len : {len(outcome)}, outcomes : {outcome}')
process_time = time.time() - time_start
print(f'len : {len(outcome)} , outcomes : {outcome}')
print(f'{process_time : .5f}')




# 0, 100000 -> 22.99800s