import rpyc
import time
import math

conn_01 = rpyc.connect('localhost', 8101)
conn_02 = rpyc.connect('localhost', 8102)

# prompt the user for the input
num1: int = int(input('Enter the start number:'))
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
# outcome_01 = list(conn_01.root.findPrimeUntilDesired_SV_01(num1, num2_SV_01))
# print(time.time() - time_start)
# outcome_02 = list(conn_02.root.findPrimeUntilDesired_SV_02(num1, num2_SV_02))
# print(time.time() - time_start)
# ##################


outcome_01_raw = rpyc.async_(conn_01.root.findPrimeUntilDesired_SV_01)(num1, num2_SV_01)
print(f'1 : {time.time() - time_start}')


outcome_02_raw = rpyc.async_(conn_02.root.findPrimeUntilDesired_SV_02)(num1, num2_SV_02)
print(f'2 : {time.time() - time_start}')


# wait until the processes are done
outcome_01_raw.wait()
outcome_02_raw.wait()
print(f'len: {len(list(outcome_02_raw.value))} - {outcome_02_raw.value}')
print(f'{type(list(outcome_02_raw.value))}')
print(f'3 : {time.time() - time_start}')

# change the data type as list
outcome_01 = list(outcome_01_raw.value)
outcome_02 = list(outcome_02_raw.value)
print(f'4 : {time.time() - time_start}')

# # # # #
# Challenge : This is not yet completed
# The code will ruin when num2 becomes large
# Ex
# prime numbers when num1 = 2, num2 =32 -> 
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]
# However, 
# SV_01 -> [5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 109, 113, 137, 149]
# SV_02 -> [7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 79, 83, 103, 107, 127]
# Since we don't know the distribution of prime number with
# Z_01 that 1 + 4x where x are positive Z
# Z_02 that 3 + 4x where x are positive Z
# Thus, somehow, we have to do some engineering
# To check whether the SV_02 has any additional prime number which are smaller than the biggest number of SV_01
# And vice versa

# Get the last(== biggest) prime number of each list 
# Then find is there any hidden prime number b/w two lists
outcome_01_last = outcome_01[-1]
outcome_02_last = outcome_02[-1]
print(f'5 : {time.time() - time_start}')
# if maximum prime number is greater than 2
if max(outcome_01 + outcome_02) > 2:
    
    # balancer will returns (extra_prime_list, indicator)
    # This does not need an Async process
    if outcome_01_last > outcome_02_last:
        # call SV_02
        # extra_outcome = list(conn_02.root.balancer(outcome_01_last, outcome_02_last)[0])
        extra_outcome_raw = rpyc.async_(conn_02.root.balancer)(outcome_01_last, outcome_02_last)
        extra_outcome = list(extra_outcome_raw.value[0])
    
    elif outcome_01_last < outcome_02_last:
        # call SV_01
        extra_outcome = list(conn_01.root.balancer(outcome_01_last, outcome_02_last)[0])

print(f'5 : {time.time() - time_start}')


# Put the hidden prime number and take any remnant prime number out
final_outcome = sorted(outcome_01 + outcome_02 + extra_outcome)[:num2]

process_time = time.time() - time_start
print(f'len : {len(final_outcome)} , outcomes : {final_outcome}')
# print(f'{extra_outcome}')
print(f'{process_time : .5f}')