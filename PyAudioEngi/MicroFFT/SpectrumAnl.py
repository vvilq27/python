'''
Created on 7 maj 2018

@author: arkadiusz.zelazowski
'''
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
# from chunk import Chunk

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
# RATE = 44100
RATE = 20000

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK 
)

fig, (ax, ax2) = plt.subplots(2, figsize=(15,8))

x = np.arange(0, 2 *CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)
line, = ax.plot(x,  np.random.rand(CHUNK))
line_fft, = ax2.plot(x_fft, np.random.rand(CHUNK), '-', lw=2 )
ax.set_ylim(0, 255)
ax.set_xlim(0, CHUNK)
ax2.set_xlim(20, RATE/2)
plt.show(block = False)


# save voice to file and display it
while True:
    data = stream.read(CHUNK)
#     data_int = struct.unpack(str(2*CHUNK) +'B', data)
    data_int = np.array(struct.unpack(str(2*CHUNK) +'B', data), dtype='b')[::2] + 128
    
    y_fft = fft(data_int)
    line_fft.set_ydata(np.abs(y_fft[0:CHUNK]) * 2 /  (256 * CHUNK) )
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()


    
    
    
    

# ax.plot(data_int, '-')
# plt.show()