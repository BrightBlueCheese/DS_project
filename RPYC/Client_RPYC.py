import rpyc

conn = rpyc.connect('localhost', 8100)

# prompt the user for the input
num1: int = int(input('Enter the start number:'))
num2: int = int(input('Enter the amount of prime numbers:'))

# prime_list = []


# outcome = conn.root.findPrimeUntilDesired(num1, num2, prime_list)
outcome = conn.root.findPrimeUntilDesired(num1, num2)
# outcome = conn.root.isPrime(3)
# print(f'len : {len(outcome)}, outcomes : {outcome}')
print(f'outcomes : {outcome}')