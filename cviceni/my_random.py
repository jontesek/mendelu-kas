import time
import random

print random.getrandbits(100)


bits_count = 1000*8

unix_time = timestamp = int(time.time())

bits = []

for i in range(0,bits_count):
    bit = int(i+unix_time % 2)
    bits.append(bit)

print bits




