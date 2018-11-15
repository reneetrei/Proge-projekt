import pyaudio
import numpy as np

p = pyaudio.PyAudio()
fs = 44100
# alustab salvestust
sisend = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
# test
tulemused = np.array([], dtype=np.int16)
# alustab salvestamist, kuni vajutatakse kas CTRL + C või siis Del klahvi
print("Time to stop")
try:
    while True:
        print("CTRL+C lõpetab salvestamise")
        andmed = sisend.read(1024)
        uuedAndmed = np.frombuffer(andmed, dtype=np.int16)
        tulemused = np.append(tulemused, uuedAndmed)
except KeyboardInterrupt:
    print("Salvestus lõppenud")

sisend.stop_stream()
sisend.close()
p.terminate()

# ühetasandiliseks listiks tegemine
ajutine = np.fft.fft(tulemused.ravel())
# põhivõnkesageduse leidmine
pohiVonkeSagedus = np.argmax(abs(ajutine[:int(ajutine.size/2)]))
# numpy Fourier sageduse funktsioon
sagedused = np.fft.fftfreq(len(ajutine))
# tegeliku sageduse leidmine
tuvastatudSagedus = sagedused[pohiVonkeSagedus]*fs
# selle väljastamine
print(tuvastatudSagedus)




