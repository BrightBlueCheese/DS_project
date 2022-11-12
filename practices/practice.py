import time


start_time = time.time()

num : int = 0
for i in range(1000):
    num += i

process_time = time.time() - start_time

print(f'{process_time:.5f}')