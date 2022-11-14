import math

# @rpyc.service
class Primer():

    def __init__(self):
        self.prime_list = []

        # determine a number is prime
    # @rpyc.exposed
    def isPrime(self, number):
        self.i: int = 0;
        # 1 is not a prime number
        if number == 1:
            return False
        else:    
            for i in range(2, int(math.sqrt(number)) + 1):
                    if (number % i) == 0:
                        return False;
        return True;

    # @rpyc.exposed
    def findNextPrime(self, x):
        self.number: int = x + 1;
        while not self.isPrime(self.number):
            self.number += 1;
        return self.number;

    # @rpyc.exposed
    def findPrimeUntilDesired(self, num1, num2, prime_list=list()):
        self.prime_list = prime_list
        # record starting time to calculate the process time
        while not num2 == len(self.prime_list):

            if self.isPrime(num1):
                self.prime_list.append(num1)
                num1 = self.findNextPrime(num1)

            elif not self.isPrime(num1):
                num1 = self.findNextPrime(num1)

        return self.prime_list


sip = Primer()

x = sip.findPrimeUntilDesired(2, 10)
print(x)