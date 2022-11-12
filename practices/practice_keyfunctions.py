import math

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
        
print(isPrime(1))

# find the next prime number
def findNextPrime(x):
    number: int = x + 1;
    while not isPrime(number):
        number += 1;
    return number;

# def findPrimeUntilDesired(num1, num2, prime_list = []):
#     while num2 == len(prime_list):
#         print('entered')
#         if isPrime(num1):
#             prime_list.append(num1)
#             findNextPrime(num1)
#             print(f'{num1} : {isPrime(num1)}')
#             num1 = findNextPrime(num1)

#     print(f'{num2} prime numbers started from {num1} are {prime_list}')


def findPrimeUntilDesired(num1, num2, prime_list=list()):
    while not num2 == len(prime_list):
        print(f'{num1} : {isPrime(num1)}')
        if isPrime(num1):
            prime_list.append(num1)
            num1 = findNextPrime(num1)
        elif not isPrime(num1):
            num1 = findNextPrime(num1)

    return prime_list

print(findPrimeUntilDesired(4, 5))

# num1 = 2
# num2 = 3

# prime_list = []
# while not num2 == len(prime_list):
#     print('entered')
#     if isPrime(num1):
#         prime_list.append(num1)
#         findNextPrime(num1)
#         print(f'{num1} : {isPrime(num1)}')
#         num1 = findNextPrime(num1)

# def isPrime(number):
#     i: int = 0;
#     # # 1 is not a prime number
#     # if number == 1:
#     #     return False

#     for i in range(2, int(math.sqrt(number)) + 1):
#         if (number % i) == 0:
#             return False;
#     return True;

# isPrime(4)

# number = 5
# TF = ''
# # for i in range(2, int(math.sqrt(number)) + 1):
# #     if (number % i) == 0:
# #         TF = False
# #     else:
# #         TF = True
# #     print(f'{TF}')

# print(isPrime(3))