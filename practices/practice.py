import time
import numpy as np

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

print(max(list_01 + list_02))

print(sorted(list_03)[:6])

print(list_01 + list_02)


print(np.array(list_01))
print(max(np.concatenate((list_01, list_02), axis=None)))


np_01 = np.array(list_01)
np_01 = np.append(np_01, 1)
print(np_01)

print(np.array([]))