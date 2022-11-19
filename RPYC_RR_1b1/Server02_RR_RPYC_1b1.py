import rpyc
from rpyc.utils.server import ThreadedServer
import math
import numpy as np
rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

@rpyc.service
class Primer_SV_02(rpyc.Service):

    def __init__(self):
        self.prime_list = []
        self.extra_prime_list = []

        # determine a number is prime
    @rpyc.exposed
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

    # identical to the SV 01
    @rpyc.exposed
    def findNextPrime_RR(self, x):
        self.number: int = x + 4;
        while not self.isPrime(self.number):
            self.number += 4;
        return self.number;

    
    @rpyc.exposed
    def findPrimeUntilDesired_SV_02(self, num1, num2):
        # SV_01 and SV_02 will each get half of computation
        # when 0 or 1, start from 2
        if num1 == 0 or num1 == 1 or num1 == 2:
            num1 = 3

        # when even number except 2, make it odd number
        elif num1 % 2 == 0:
            num1 += 3

        else:
            num1 += 2

        # record starting time to calculate the process time
        while not num2 == len(self.prime_list):

            if self.isPrime(num1) and num1 == 2:
                self.prime_list.append(num1)
                num1 = self.findNextPrime_RR(num1+1)

            elif self.isPrime(num1):
                self.prime_list.append(num1)
                num1 = self.findNextPrime_RR(num1)

            elif not self.isPrime(num1):
                num1 = self.findNextPrime_RR(num1)

        return np.array(self.prime_list)

    @rpyc.exposed
    def balancer(self, outcome_01_last, outcome_02_last):
        indicator = 0

        # 1 : extra_prime_list is the complement for outcome_02
        # 2 : extra_prime_list is the complement for outcome_01

        if outcome_01_last > outcome_02_last:
            # try to find the next prime
            num1 = outcome_02_last + 4 
            # to inform which condition
            indicator = 2 # << extra_prime_list is the complement of outcome_02

            while outcome_01_last > num1:
                if self.isPrime(num1) and num1 == 2:
                    self.extra_prime_list.append(num1)
                    num1 = self.findNextPrime_RR(num1+1)

                elif self.isPrime(num1):
                    self.extra_prime_list.append(num1)
                    num1 = self.findNextPrime_RR(num1)

                elif not self.isPrime(num1):
                    num1 = self.findNextPrime_RR(num1)

        elif outcome_01_last < outcome_02_last:
            # try to find the next prime
            num1 = outcome_01_last + 4
            # to inform which condition 
            indicator = 1 # << extra_prime_list is the complement of outcome_01

            while num1 < outcome_02_last:
                if self.isPrime(num1) and num1 == 2:
                    self.extra_prime_list.append(num1)
                    num1 = self.findNextPrime_RR(num1+1)

                elif self.isPrime(num1):
                    self.extra_prime_list.append(num1)
                    num1 = self.findNextPrime_RR(num1)

                elif not self.isPrime(num1):
                    num1 = self.findNextPrime_RR(num1)

        return np.array(self.extra_prime_list)


print("Listening on port 8105...")

if __name__ == "__main__":
    server = ThreadedServer(Primer_SV_02, port = 8105)
    server.start()