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

proxy_01 = xmlrpc.client.ServerProxy("http://localhost:8001/")
proxy_02 = xmlrpc.client.ServerProxy("http://localhost:8002/")

outcome_01 = proxy_01.findPrimeUntilDesired_SV_01(num1, num2_SV_01, prime_list_01)
outcome_02 = proxy_02.findPrimeUntilDesired_SV_02(num1, num2_SV_02, prime_list_02)


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



outcome_01_last = outcome_01[-1]
outcome_02_last = outcome_02[-1]
extra_prime_list = []

# if maximum prime number is greater than 2
if max(outcome_01 + outcome_02) > 2:
    # Call Server02
    if outcome_01_last > outcome_02_last:
        extra_outcome = proxy_02.balancer(outcome_01_last, outcome_02_last, extra_prime_list)[0] # we don't need the indicator actually - just to check
    
    elif outcome_01_last < outcome_02_last:
        # Call Server01
        extra_outcome = proxy_01.balancer(outcome_01_last, outcome_02_last, extra_prime_list)[0]



# print(f'extra_outcomes : {extra_outcome}')



# final outcome, only valid primes
final_outcome = sorted(outcome_01 + outcome_02 + extra_outcome)[:num2]
process_time = time.time() - time_start
print(f'outcomes : {final_outcome}')
print(f'{process_time : .5f}')