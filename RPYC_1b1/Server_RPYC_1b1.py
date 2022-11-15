# Title : Server_RPYC_1b1.py
# Author : Youngmin Lee
# Date : Nov 14 2022
# Description : A Server that keeps receiving single positive ineger from a Client and sending back to the Client
# if the integer is a prime number. The Client and the Server interact for each integer

import rpyc
from rpyc.utils.server import ThreadedServer
import math

@rpyc.service
class Primer(rpyc.Service):

    def __init__(self):
        self.prime_list = []

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
    def findNextPrime(self, number):
        # # original  :  num1 = 0, num2 = 100000 -> 14.44417s
        # self.number += 1;

        # # optimized :  num1 = 0, num2 = 100000 -> 13.95051s
        number += 2

        while not self.isPrime(number):
        
            number += 2

        return number;


print("Listening on port 8103...")

if __name__ == "__main__":
    server = ThreadedServer(Primer, port = 8103)
    server.start()

