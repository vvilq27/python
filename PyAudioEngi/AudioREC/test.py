'''
Created on 7 maj 2018

@author: arkadiusz.zelazowski
'''
import time

t = time.clock()
for i in range(1000000):
    a = 5+3
print(time.clock() - t)

buffer = []

data1 = [1 ,2 ,3 ,4 ]
data2 = [5,6, 7 ,8 ]

buffer.append(data1)
print(buffer)
buffer.append(data2)
buffer.append(data1)
print(buffer[1])

