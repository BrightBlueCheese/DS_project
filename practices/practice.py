import time


start_time = time.time()

num : int = 0
for i in range(1000):
    num += i

process_time = time.time() - start_time

print(f'{process_time:.5f}')

list_01 = [1, 3, 5]
list_02 = [2, 4, 6]

list_03 = list_01 + list_02

print(list_03)