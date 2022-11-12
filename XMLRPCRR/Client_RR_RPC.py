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

prime_list_01 = []
prime_list_02 = []

with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy_01:
    

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

with xmlrpc.client.ServerProxy("http://localhost:8001/") as proxy_02:
    

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

final_outcome = outcome_01 + outcome_02

print(f'outcomes : {final_outcome}')

process_time = time.time() - time_start
print(f'{process_time : .5f}')