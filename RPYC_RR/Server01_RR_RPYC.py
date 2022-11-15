import rpyc
from rpyc.utils.server import ThreadedServer
import math

@rpyc.service
class Primer_SV_01(rpyc.Service):

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

    @rpyc.exposed
    def findNextPrime_RR(self, x):
        self.number: int = x + 4;
        while not self.isPrime(self.number):
            self.number += 4;
        return self.number;

    @rpyc.exposed
    # def findPrimeUntilDesired(self, num1, num2, prime_list=list()):
    #     self.prime_list = []
    def findPrimeUntilDesired_SV_01(self, num1, num2):
        # SV_01 and SV_02 will each get half of computation
        # when 0 or 1, start from 2
        if num1 == 0 or num1 == 1:
            num1 = 2
        # when even number except 2, make it odd number
        elif num1 != 2 and num1 % 2 == 0:
            num1 += 1

        # record starting time to calculate the process time
        while not num2 == len(self.prime_list):

            if self.isPrime(num1) and num1 == 2:
                self.prime_list.append(num1)
                num1 = self.findNextPrime_RR(num1-1)

            elif self.isPrime(num1):
                self.prime_list.append(num1)
                num1 = self.findNextPrime_RR(num1)

            elif not self.isPrime(num1):
                num1 = self.findNextPrime_RR(num1)

        return self.prime_list


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

        return self.extra_prime_list, indicator


print("Listening on port 8101...")

if __name__ == "__main__":
    server = ThreadedServer(Primer_SV_01, port = 8101)
    server.start()