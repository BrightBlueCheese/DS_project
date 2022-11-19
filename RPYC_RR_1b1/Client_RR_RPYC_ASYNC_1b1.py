import rpyc
import time
import math
import numpy as np
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

conn_01 = rpyc.connect('localhost', 8104)
conn_02 = rpyc.connect('localhost', 8105)

# prompt the user for the input
num1: int = int(input('Enter the start number:'))

while num1 < 0:
    print('Negative integer ins not valid. Please try again.')
    num1: int = int(input('Enter the start number:'))

num2: int = int(input('Enter the amount of prime numbers:'))

while num2 <= 0:
    print('Please enter a valid number.')
    num2: int = int(input('Enter the amount of prime numbers:'))

# Start to record time
time_start = time.time()

# a list to store the prime numbers and extras

extra_prime_list = []

def spliter(num2):
    # when get the input num2, condition: num2 >= 1

    if num2 == 1:
        return 1, 0

    elif num2 % 2 == 1:
        num_to_SV_01 = math.ceil(num2/2)
        num_to_SV_02 = math.floor(num2/2)
        return num_to_SV_01, num_to_SV_02

    elif num2 % 2 == 0:
        num_to_SV_01 = int(num2/2)
        num_to_SV_02 = int(num2/2)
        return num_to_SV_01, num_to_SV_02

num2_SV_01, num2_SV_02 = spliter(num2)



# #####################
# # Get the outcomes from SV_01 and SV_02
#     # All case can handle the case of num1 == 0 or 1 or 2 as well!
# # outcome_01 = {There exist Z such that 3 + 4x where x is positive integers}
# # outcome_02 = {There exist Z such that 5 + 4x where x is positive integers}
# outcome_01 = list(conn_01.root.findPrimeUntilDesired_SV_01(num1, num2_SV_01))
# print(time.time() - time_start)
# outcome_02 = list(conn_02.root.findPrimeUntilDesired_SV_02(num1, num2_SV_02))
# print(time.time() - time_start)
# ##################


async_02_isPrime = rpyc.async_(conn_02.root.isPrime)
async_01_findNextPrime_RR = rpyc.async_(conn_01.root.findNextPrime_RR)
async_02_findNextPrime_RR = rpyc.async_(conn_02.root.findNextPrime_RR)

# num1_02 : int = 0

# when 0 or 1, start from 2

def findPrimeUntilDesired_RR_1b1(num1, num2):
    prime_list_01 = np.array([])
    prime_list_02 = np.array([])

    if num1 == 0 or num1 == 1:
        num1 = 2
        num1_02 = num1 + 1

    elif num1 == 2:
        num1_02 = num1 + 1

    # when even number except 2, make it odd number
    elif num1 != 2 and num1 % 2 == 0:
        num1 += 1
        num1_02 = num1 + 2

    else:
        num1_02 = num1 + 2



    while (((num2/2) >= (len(prime_list_01))) and ((num2/2) >= (len(prime_list_02)))):

        if async_02_isPrime(num1).value and num1 == 2:
            prime_list_01 = np.append(prime_list_01, num1)
            prime_list_02 = np.append(prime_list_02, num1_02)
            num1_raw = async_01_findNextPrime_RR(num1-1)
            num1_02_raw = async_02_findNextPrime_RR(num1_02)
            # num1_raw.wait()
            # num1_02_raw.wait()
            num1 = num1_raw.value
            num1_02 = num1_02_raw.value
            prime_list_01 = np.append(prime_list_01, num1)
            prime_list_02 = np.append(prime_list_02, num1_02)

        else:
            num1_raw = async_01_findNextPrime_RR(num1)
            num1_02_raw = async_02_findNextPrime_RR(num1_02)
            # num1_raw.wait()
            # num1_02_raw.wait()
            num1 = num1_raw.value
            num1_02 = num1_02_raw.value
            prime_list_01 = np.append(prime_list_01, num1)
            prime_list_02 = np.append(prime_list_02, num1_02)

    return prime_list_01, prime_list_02





###
# This part Actually does not need for RPYC_RR_1b1
# But I left it for the fault tolerance for JUST IN CASE
###
outcome_01, outcome_02 = findPrimeUntilDesired_RR_1b1(num1, num2)

# Get the last(== biggest) prime number of each list 
# Then find is there any hidden prime number b/w two lists
outcome_01_last = int(outcome_01[-1])
outcome_02_last = int(outcome_02[-1])

# if maximum prime number is greater than 2
if max(np.concatenate((outcome_01, outcome_02), axis=None)) > 2:

    # balancer will returns (extra_prime_list, indicator)
    # This one does not need an Async process
    if outcome_01_last > outcome_02_last:
        # call SV_02
        extra_outcome = np.array(conn_02.root.balancer(outcome_01_last, outcome_02_last)) # we don't need the indicator actually - just to check
    
    elif outcome_01_last < outcome_02_last:
        # call SV_01
        # extra_outcome = list(conn_01.root.balancer(outcome_01_last, outcome_02_last)[0])
        extra_outcome = np.array(conn_01.root.balancer(outcome_01_last, outcome_02_last))


# print(f'{outcome_01_last} , {outcome_02_last}')
# print(f'extra : {extra_outcome}')
# print(time.time() - time_start)

# Put the hidden prime number and take any remnant prime number out
# final_outcome = sorted(outcome_01 + outcome_02 + extra_outcome)[:num2]
final_outcome = sorted(np.concatenate((outcome_01, outcome_02, extra_outcome), axis=None))[:num2]
process_time = time.time() - time_start

# change data type to int
# final_outcome = final_outcome.astype('int')

print(f'len : {len(final_outcome)} , outcomes : {final_outcome}')
print(f'{process_time : .5f}')