import xmlrpc.client
import time
import math

# prompt the user for the input

    # Have to 
num1: int = int(input('Enter the start number:'))
num2: int = int(input('Enter the amount of prime numbers:'))

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

# have to clear the lists for every request
prime_list_01 = []
prime_list_02 = []

with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy_01:
    

    # # Have to assign empty list for every trial
    # # Otherwise, the server will save the previous list data 
    # # And call the previouus if num2 is the same as the previous
    # # By the algorithm of function findPrimeUntilDesired
    
    # # record starting time to calculate the process time
    # time_start = time.time()



    # # split num2 to pass to each Server
    # # When num2 is odd, then SV_01 will take bigger number
    # # ex) if num2 = 3 -> num2_SV_01 = 2, num2_SV_02 = 1
    



    outcome_01 = proxy_01.findPrimeUntilDesired_SV_01(num1, num2_SV_01, prime_list_01)
    # outcome_02 = proxy.findPrimeUntilDesired_SV_02(num1, num2_SV_02, prime_list_02)

    # final_outcome = outcome_01 + outcome_02

    # print(f'outcomes : {final_outcome}')

    # process_time = time.time() - time_start
    # print(f'{process_time : .5f}')
# python Client_RPC.py
print(f'after server01 : {time.time() - time_start}')
with xmlrpc.client.ServerProxy("http://localhost:8002/") as proxy_02:
    

    # # Have to assign empty list for every trial
    # # Otherwise, the server will save the previous list data 
    # # And call the previouus if num2 is the same as the previous
    # # By the algorithm of function findPrimeUntilDesired
    
    # # record starting time to calculate the process time
    # time_start = time.time()



    # # split num2 to pass to each Server
    # # When num2 is odd, then SV_01 will take bigger number
    # # ex) if num2 = 3 -> num2_SV_01 = 2, num2_SV_02 = 1
    



    # outcome_01 = proxy_01.findPrimeUntilDesired_SV_01(num1, num2_SV_01, prime_list_01)
    outcome_02 = proxy_02.findPrimeUntilDesired_SV_02(num1, num2_SV_02, prime_list_02)

#     final_outcome = outcome_01 + outcome_02

#     print(f'outcomes : {final_outcome}')

#     process_time = time.time() - time_start
#     print(f'{process_time : .5f}')
# # python Client_RPC.py


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

# Solution - function 'balancer'

print(f'after server02 : {time.time() - time_start}')

outcome_01_last = outcome_01[-1]
outcome_02_last = outcome_02[-1]
extra_prime_list = []

# if maximum prime number is greater than 2
if max(outcome_01 + outcome_02) > 2:
    # Call Server02
    if outcome_01_last > outcome_02_last:
        with xmlrpc.client.ServerProxy("http://localhost:8002/") as proxy_02:
            extra_outcome = proxy_02.balancer(outcome_01_last, outcome_02_last, extra_prime_list)[0] # we don't need the indicator actually - just to check
    
    elif outcome_01_last < outcome_02_last:
        # Call Server01
        with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy_01:
            extra_outcome = proxy_01.balancer(outcome_01_last, outcome_02_last, extra_prime_list)[0]



# print(f'extra_outcomes : {extra_outcome}')



# final outcome, only valid primes
final_outcome = sorted(outcome_01 + outcome_02 + extra_outcome)[:num2]
process_time = time.time() - time_start
print(f'len : {len(final_outcome)} , outcomes : {final_outcome}')
print(f'{process_time : .5f}')


# single : 2 , 100,000 -> 13.12s
# RR : 2, 10,000 -> 20.83819
#  sigle / RR ratio  = 1 : 1.59


# single : 2 , 200,000 -> 33.73542
# RR : 2, 20,000 -> 49.62175
#  sigle : RR ratio  = 1 : 1.47

# single : 2 , 300,000 -> 60.45121
# RR : 2, 30,000 ->  86.97157
#  sigle / RR ratio  = 1 : 1.44

# single : 2 , 400,000 -> 92.03900
# RR : 2, 30,000 ->  86.97157
#  sigle / RR ratio  = 1 : 1.44