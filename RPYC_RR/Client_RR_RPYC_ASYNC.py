import rpyc
import time
import math
import numpy as np
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

conn_01 = rpyc.connect('localhost', port = 8101, config = rpyc.core.protocol.DEFAULT_CONFIG)
conn_02 = rpyc.connect('localhost', port = 8102, config = rpyc.core.protocol.DEFAULT_CONFIG)

# my_list = []

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
# ##################
outcome_01_raw = rpyc.async_(conn_01.root.findPrimeUntilDesired_SV_01)(num1, num2_SV_01)
outcome_02_raw = rpyc.async_(conn_02.root.findPrimeUntilDesired_SV_02)(num1, num2_SV_02)


# Change rpyc return value into list takes dramatic times
# So had to convert numpy instead of list
outcome_02 = np.array(outcome_02_raw.value)
outcome_01 = np.array(outcome_01_raw.value)
# assigning one of these outcome values into another variables will cause error related to numpy


# # # # #
# Challenge : This is not yet completed
# The code will ruin when num2 becomes large
# Ex
# prime numbers when num1 = 5, num2 =32 -> 
# [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
# However, 
# SV_01 -> [5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 109, 113, 137, 149]
# SV_02 -> [7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83, 103, 107, 127]
# Since we don't know the distribution of prime number with
# Z_01 that 3 + 4x where x are positive Z
# Z_02 that 5 + 4x where x are positive Z
# Should be able to deal with the case of num1 = 0, 1, 2
# Thus, somehow, we have to do some engineering
# To check whether the SV_02 has any additional prime number which are smaller than the biggest number of SV_01
# And vice versa

# Get the last(== biggest) prime number of each list 
# Then find is there any hidden prime number b/w two lists
outcome_01_last = int(outcome_01_raw.value[-1])
outcome_02_last = int(outcome_02_raw.value[-1])

# extra_outcome = []

# To find the hidden prime numbers in between outcome_01_last and outcome_02_last
# if maximum prime number is greater than 2
if max(np.concatenate((outcome_01, outcome_02), axis=None)) > 2:

    # balancer will returns (extra_prime_list, indicator)
    if outcome_01_last > outcome_02_last:
        extra_outcome_raw = rpyc.async_(conn_02.root.balancer)(outcome_01_last, outcome_02_last)
        extra_outcome = np.array(extra_outcome_raw.value)

    elif outcome_01_last < outcome_02_last:
        # call SV_01
        extra_outcome_raw = rpyc.async_(conn_01.root.balancer)(outcome_01_last, outcome_02_last)
        extra_outcome = np.array(extra_outcome_raw.value)


# print(extra_outcome)

# Correct the prime number list
final_outcome = sorted(np.concatenate((outcome_01, outcome_02, extra_outcome), axis=None))[:num2]

# print(num2)
process_time = time.time() - time_start
print(f'len : {len(final_outcome)} , outcomes : {final_outcome}')
print(f'{process_time : .5f}')