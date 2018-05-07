import pyaudio
import wave
import time
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 20000
CHUNK = 512
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "file.wav"
 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
frames = []

# data = stream.read(CHUNK)

# for i in data:
#     print(i)

'''
for a in data:
    print(a)

print('data size:' , len(data))

frames.append(data)
print(len(frames[0]))
data = stream.read(CHUNK)
frames.append(data)
print(len(frames))
'''

t = time.clock()

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print(time.clock() - t)
print(len(frames))
print(len(frames[0]))

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
 
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()