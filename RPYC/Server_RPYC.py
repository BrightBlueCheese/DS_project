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
        # # original  :  num1 = 0, num2 = 10000 -> 14.44417s
        # self.number += 1;

        # # optimized :  num1 = 0, num2 = 10000 -> 13.82599
        number += 2

        while not self.isPrime(number):
        
            number += 2

        return number;

    @rpyc.exposed
    def findPrimeUntilDesired(self, num1, num2):

        if num1 == 0 or num1 == 1:
            num1 = 2
        # when even number except 2, make it odd number
        elif num1 != 2 and num1 % 2 == 0:
            num1 += 1

        # record starting time to calculate the process time
        while not num2 == len(self.prime_list):

            if self.isPrime(num1) and num1 == 2:
                self.prime_list.append(num1)
                num1 = self.findNextPrime(num1-1)

            elif self.isPrime(num1):
                self.prime_list.append(num1)
                num1 = self.findNextPrime(num1)

            elif not self.isPrime(num1):
                num1 = self.findNextPrime(num1)

        return self.prime_list


print("Listening on port 8100...")

if __name__ == "__main__":
    server = ThreadedServer(Primer, port = 8100)
    server.start()

# date_time = datetime.datetime.now()

# class MonitorService(rpyc.Service):
#     def on_connect(self, conn):
#         print(f'connected on {date_time}')

#     def on_disconnect(self, conn):
#         print(f'connected on {date_time}')


# if __name__ == '__main__':
#     t = ThreadedServer(MonitorService, port=8100)
#     t.start()