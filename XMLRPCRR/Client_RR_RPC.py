import xmlrpc.client
import time
import math

with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        # prompt the user for the input
    num1: int = int(input('Enter the start number:'))
    num2: int = int(input('Enter the amount of prime numbers:'))

    # Have to assign empty list for every trial
    # Otherwise, the server will save the previous list data 
    # And call the previouus if num2 is the same as the previous
    # By the algorithm of function findPrimeUntilDesired
    
    # record starting time to calculate the process time
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

    # split num2 to pass to each Server
    num2_SV_01, num2_SV_02 = spliter(num2)

    prime_list_01 = []
    prime_list_02 = []



    outcome_01 = proxy.findPrimeUntilDesired(num1, num2_SV_01, prime_list_01)
    outcome_02 = proxy.findPrimeUntilDesired(num1, num2_SV_02, prime_list_02)

    print(f'outcomes : {outcome_01}')

    process_time = time.time() - time_start
    print(f'{process_time : .5f}')
# python Client_RPC.py