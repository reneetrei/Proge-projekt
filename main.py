import pyaudio
import numpy as np

def genereerisagedus(noot):
    sagedus = np.power(np.power(2, 1/12),noot-49)*440 #A4, 49. noot, sagedus 440Hz
    return sagedus

def genereerihääl(sagedused, kestus=10):
    p = pyaudio.PyAudio()
    volume = 0.5
    fs = 44100

    samples = (np.sin(2*np.pi*np.arange(fs*kestus)*sagedused[0]/fs)).astype(np.float32)/len(sagedused)
    if len(sagedused) > 1:
        for i in range(len(sagedused)-1):
            s = (np.sin(2*np.pi*np.arange(fs*kestus)*sagedused[i+1]/fs)).astype(np.float32)/len(sagedused)
            samples=samples + s

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()

    p.terminate()

genereerihääl([genereerisagedus(49), genereerisagedus(53), genereerisagedus(56)]) #Mitu nooti korraga
#genereerihääl([genereerisagedus(61)]) #Üksik noot