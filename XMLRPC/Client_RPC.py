import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        # prompt the user for the input
    num1: int = int(input('Enter the start number:'))
    num2: int = int(input('Enter the amount of prime numbers:'))

    # Have to assign empty list for every trial
    # Otherwise, the server will save the previous list data 
    # And call the previouus if num2 is the same as the previous
    # By the algorithm of function findPrimeUntilDesired
    prime_list1 = []

    print(f'outcomes : {proxy.findPrimeUntilDesired(num1, num2, prime_list1)}')

# python Client_RPC.py