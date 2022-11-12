from practice_spliter import spliter
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from XMLRPC.Server_RPC import isPrime, findNextPrime


print(spliter(3))



def findNextPrime_RR(x):
    number: int = x + 4;
    while not isPrime(number):
        number += 4;
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


def findPrimeUntilDesired_SV_01(num1, num2, prime_list=list()):
    # SV_01 and SV_02 will each get half of computation
    # when 0 or 1, start from 2
    if num1 == 0 or num1 == 1:
        num1 = 2
    # when even number, make it odd number
    elif num1 != 2 and num1 % 2 == 0:
        num1 += 1
    while not num2 == len(prime_list):

        if isPrime(num1) and num1 == 2:
            prime_list.append(num1)
            num1 = findNextPrime_RR(num1-1)

        elif isPrime(num1):
            prime_list.append(num1)
            num1 = findNextPrime_RR(num1)

        elif not isPrime(num1):
            num1 = findNextPrime_RR(num1)

    return prime_list
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

print(findPrimeUntilDesired(2, 8))
print(findPrimeUntilDesired_SV_01(2, 4))
print(findPrimeUntilDesired_SV_02(2, 4))

# 2, 3, 5, 7, 11, 13, 17, 19