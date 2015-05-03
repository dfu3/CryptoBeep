import audioop
import binascii

__author__ = 'dfu3'

import pyaudio
import wave
import sys
from pylab import *
import struct
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf

#------------------------------------------------------
#reading sound from mic
#------------------------------------------------------

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 30
WAVE_OUTPUT_FILENAME = "input.wav"
THRES = 5000

if sys.platform == 'darwin':
    CHANNELS = 1

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []
bCOunt = 0
sCount = 0
chunkCount = 0
setBit = 0
firstBit = False
bitList = ""

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)  #width=2 for format=paInt16
    frames.append(data)

    if(rms > THRES and (not firstBit)):
        print("found first bit")
        firstBit = True

    if(firstBit):

        chunkCount +=1

        if(chunkCount == 1):
            if(rms < THRES):    #------silence
                setBit = 0
            else:               #------beep
                setBit = 1


        if(chunkCount == 13):
            if(setBit == 0):
                bitList += "0"
            else:
                bitList += "1"

            chunkCount = 0


bitList = bitList[1:]
ind = len(bitList) - 1

while(bitList[ind] == "0"):
    ind -= 1

bitList = bitList[:ind]

#----------------------------------
import subprocess
cmd = ['ssh', 'root@69.28.93.232', 'cat', 'output/dir/cipher.txt']
ssh = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in ssh.stdout:
    key = line
#----------------------------------

binVal = int(bitList, 2) ^ int(key, 2)

hexString = ""
hexString += (hex(binVal)[2:-1])

decryptMess = binascii.unhexlify(hexString)

print("original text: " +decryptMess)

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
#-------------------------- ----------------------------
#plotting sound below
#------------------------------------------------------

spf = wave.open('input.wav','r')

signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()

#If Stereo
if spf.getnchannels() == 2:
    print 'Just mono files'
    sys.exit(0)

Time=np.linspace(0, len(signal)/fs, num=len(signal))

plt.figure(1)
plt.title('Signal Wave')
plt.plot(Time,signal)
plt.show()

