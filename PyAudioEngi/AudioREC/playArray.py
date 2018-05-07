'''
Created on 7 maj 2018

@author: arkadiusz.zelazowski
'''

import numpy as np
from scipy.io.wavfile import  write
import pyaudio
import struct


CHUNK = 44100 * 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK 
)


data = stream.read(CHUNK)
#     data_int = struct.unpack(str(2*CHUNK) +'B', data)
data_int = np.array(struct.unpack(str(2*CHUNK) +'B', data), dtype='b')
    
'''
sound = [None] * 44100
for a in range(44100):
    sound[a] = a % 255

scaled = np.int16(sound/np.max(np.abs(sound)) * 32767)

for a in range(len(scaled)):
    print(scaled[a])
'''

write('test3.wav', RATE, data_int)
