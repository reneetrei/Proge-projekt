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

def tuvastasagedus():
    p = pyaudio.PyAudio()
    fs = 44100
    # alustab salvestust
    sisend = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=1024)
    # test
    tulemused = np.array([], dtype=np.int16)
    # alustab salvestamist, kuni vajutatakse kas CTRL + C või siis Del klahvi
    # print("Time to stop")
    # try:
    #     while True:
    #         print("CTRL+C lõpetab salvestamise")
    #         andmed = sisend.read(1024)
    #         uuedAndmed = np.frombuffer(andmed, dtype=np.int16)
    #         tulemused = np.append(tulemused, uuedAndmed)
    # except KeyboardInterrupt:
    #     print("Salvestus lõppenud")
    andmed = sisend.read(1024*50)
    tulemused = np.frombuffer(andmed, dtype=np.int16)

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
    return(tuvastatudSagedus)

def tuvastanoot(sagedus): #väljastab sisendi erinevuse A4-st centides (1 pooltoon = 100ct)
    noot = int(np.round(1200*np.log(sagedus/440)/np.log(2)))
    return noot

def võrdlenoote(cent1, cent2):
    erinevus = (cent1-cent2) % 1200
    if erinevus > 600:
        erinevus-=1200
    return erinevus

def noodinimi(noot):
    noodinimed = ["G#","A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G"]
    nimi = noodinimed[noot%12]
    return nimi

def võrdle(minimum=40, maximum=61): #genereerib sageduse ning väljastab kasutaja sisendi erinevuse tegelikkusest
    noot = np.random.randint(minimum, maximum)
    sagedus = genereerisagedus(noot)
    print("Kuula nooti:")
    genereerihääl([sagedus])
    print("Korda nooti:")
    sisend = tuvastasagedus()
    while sisend == 0.0:
        print("Palun korda:")
        sisend = tuvastasagedus()
    erinevus = võrdlenoote(tuvastanoot(sisend), tuvastanoot(sagedus))
    return (erinevus)

def kordanooti():
    print("Järgnevalt kuuled nooti, mida pead järgi kordama. Kui oled valmis, vajuta ENTER.")
    input()
    print ("Noodi ja sinu hääle erinevus oli", võrdle()/100, "pooltooni.")

def arvanoot(minimum=40, maximum=61):
    print("Järgnevalt kuuled nooti, mille pead ära tuvastama ning seejärel noodinime esitama. Kui oled valmis, vajuta ENTER.")
    input()

    noot = np.random.randint(minimum, maximum)
    sagedus = genereerisagedus(noot)
    print("Kuula nooti:")
    genereerihääl([sagedus])
    nimi = noodinimi(noot)

    pakkumine = input("Sisesta noodinimi:")
    if pakkumine == nimi:
        print("Õige, noot oli tõesti", nimi)
    else:
        print("Õige noot oli hoopis", nimi)


def ui():
    print("")
    print("#####################")
    print("# 1) Korda nooti    #")
    print("# 2) Arva noot      #")
    print("# 3) Välju          #")
    print("#####################")
    print("")
    valik = int(input())
    if valik == 1:
        kordanooti()
        ui()
    elif valik == 2:
        arvanoot()
        ui()
    elif valik == 3:
        print("#####################")
        print("#                   #")
        print("#    Nägemiseni!    #")
        print("#                   #")
        print("#####################")
#genereerihääl([genereerisagedus(49), genereerisagedus(53), genereerisagedus(56)]) #Mitu nooti korraga
#genereerihääl([genereerisagedus(61)]) #Üksik noot
#print(tuvastanoot(284.81))
#võrdle()
#arvanoot()
ui()