import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import ShortTimeFFT
from scipy.signal.windows import hann
from scipy.io.wavfile import write, read
from scipy.ndimage import uniform_filter1d
import math
import os

def max_return():
    sx_av=[sum(i)/len(i) for i in av_Sx]
    max_av = []
    for a in range(len(sx_av)-4):
        if a*SFT.delta_f < 300:
            continue
        if max(sx_av[a-2], sx_av[a-1], sx_av[a], sx_av[a+1], sx_av[a+2]) == sx_av[a] and len(max_av) < 25 and sx_av[a]>1:
            max_av.append(a)
    fre = [a*SFT.delta_f for a in max_av]
    return max_av


def phase():
    max_av = max_return()
    phase_list = []
    for i in max_av:
        phase_list.append(np.angle(Sx[i][40]))
    phase=np.angle(Sx[max_av[0]])

    return phase_list


fig1, ax1 = plt.subplots(figsize=(6., 4.)) 
def spec():
    t_lo, t_hi = SFT.extent(N)[:2] 
    ax1.set_title(rf"Spectrogram ({SFT.m_num*SFT.T:g}$\,s$ Hann " +
                rf"window)")
    ax1.set(xlabel=f"Time $t$ in seconds ({SFT.p_num(N)} slices, " +
                rf"$\Delta t = {SFT.delta_t:g}\,$s)",
            ylabel=f"Freq. $f$ in Hz ({SFT.f_pts} bins, " +
                rf"$\Delta f = {SFT.delta_f:g}\,$Hz)",
            xlim=(t_lo, t_hi))

    im1 = ax1.imshow(av_Sx_dB, origin='lower', aspect='auto', extent=SFT.extent(N), cmap='magma')
    fig1.colorbar(im1, label='Power Spectral Density ' +
                            r"$20\,\log_{10}|S_x(t, f)|$ in dB")



def aver_per():
    
    sx_means = []
    p=[]
    p_per=[]
    per_list = []
    max_av = max_return()

    for i in max_av:
        sx_means.append(np.mean(av_Sx[i-math.ceil(20/SFT.delta_f):i+math.ceil(20/SFT.delta_f)+1], axis=0))


    for a, b in enumerate(sx_means):
        per_list=[]
        for c, d in enumerate(b):
            per_list.append(d/sx_means[2][c])
        p_per.append(per_list)

    p_per_av = []

    for i in p_per:
        p_per_av.append(sum(i)/len(i))
    return p_per_av
        
def generate(n):
    samplerate=44100
    T_x, N = 1 / samplerate, samplerate*2 
    t_x = np.arange(N) * T_x 
    f_i = []
    mul = aver_per()
    max_av = max_return()
    fre = [a*SFT.delta_f for a in max_av]
    gen_phase = phase()
    x=0

    print(mul)
    print(fre)


    for i in range(len(mul)):
        f_i.append(0 * t_x + fre[i])


    for i in range(len(mul)):
        x += mul[i]*np.sin(2*np.pi*(np.cumsum(f_i[i]))*T_x+gen_phase[i])*np.exp(-2*t_x)
    x /= np.max(np.abs(x))*10


    write(f"test\test{n}.wav", samplerate, x.astype(np.float32))

# for i in range(15):
#     samplerate, x=read(f"sound\{i}.wav")
#     # x=x0[:, 0]
#     x=x[20000:40000]
#     T_x = 1 / samplerate
#     N = x.shape[0]

#     win_size = 4096
#     w = hann(win_size, sym=True)
#     SFT = ShortTimeFFT(w, hop=100, fs=1/T_x, scale_to='magnitude')
#     Sx = np.abs(SFT.stft(x))
#     Sx=Sx[:, 100:180]

#     av_Sx = uniform_filter1d(Sx, size=10)
#     av_Sx_dB = 10 * np.log10(np.fmax(av_Sx, 1e-2)) 


#     # spec()
#     generate(i)


samplerate, x0=read("sound\piano.wav")
x=x0[:, 0]
x=x[20000:40000]
T_x = 1 / samplerate
N = x.shape[0]

win_size = 4096
w = hann(win_size, sym=True)
SFT = ShortTimeFFT(w, hop=100, fs=1/T_x, scale_to='magnitude')
Sx = np.abs(SFT.stft(x))
print(SFT.stft(x))
Sx=Sx[:, 100:180]

av_Sx = uniform_filter1d(Sx, size=10)
av_Sx_dB = 10 * np.log10(np.fmax(av_Sx, 1e-2)) 


# spec()
generate(111)
plt.show()

