import math
import numpy as np
import random
from scipy.io import wavfile
from scipy.signal import periodogram
import struct

class Audio:
    def __init__(self,name,profile=None):
        self.name = name
        self.sampling_rate = 44100
        self.length = 1
        self.t = np.linspace(0.,self.length,self.length*self.sampling_rate)
        #2 channels
        self.data = np.zeros((self.sampling_rate*self.length,2))
        self.profile = profile
    
        self.create_signal()
        self.create_wav()
        self.create_payload()
    
    def create_signal(self,):
        if self.profile is None:
            f = [random.randrange(1000,10000,100) for i in range(2)]
            amp = [random.randrange(100,1000,50) for i in range(2)]
            self.profile = [(f[0],amp[0]),(f[1],amp[1])]

        
        print (f"Profiles are {self.profile}")

        #amplitude and frequency should be random
        #signals are initialized as A_rms * sin(2*pi*f*t)
        self.data[:,0] = (self.profile[0][1]) * np.sqrt(2) * np.sin( 2 * np.pi * self.profile[0][0] * self.t)
        self.data[:,1] = (self.profile[1][1]) * np.sqrt(2) * np.sin( 2 * np.pi * self.profile[1][0] * self.t)
    
    def create_wav(self,):
        wavfile.write(self.name, self.sampling_rate, self.data.astype(np.int16))

    def create_payload(self,):
        f = open(self.name,"rb")
        data = f.read()
        self.payload = struct.pack("I",len(data)) + data
        f.close()

def solver(f):
    profiles = []
    try:
        samplerate, data = wavfile.read(f)
        for i,channel in enumerate(data.T):
            f, Pxx_den = periodogram(data[:,i].astype(np.int16), samplerate,scaling='spectrum')
            #identifes the maximum frequency and the maximum PSD
            f_index,psd = np.argmax(Pxx_den),np.sqrt(Pxx_den.max())
        
            print (f"[*]Channel {i}. {f_index}:{math.ceil(psd / 50.0) * 50.0}")
            #swaps psd with frequency
            profiles.append((math.ceil(psd / 50.0) * 50.0,f_index))

        return profiles
    except:
        print(f"File is not wav.")
        return None
