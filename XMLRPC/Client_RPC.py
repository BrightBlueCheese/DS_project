import xmlrpc.client
import time

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

    prime_list1 = []

    outcome = proxy.findPrimeUntilDesired(num1, num2, prime_list1)

    

    process_time = time.time() - time_start
    print(f'outcomes : {outcome}')
    print(f'{process_time : .5f}')
# python Client_RPC.py