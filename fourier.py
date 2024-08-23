import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import ShortTimeFFT
from scipy.signal.windows import gaussian, hann
from scipy.io.wavfile import write, read
from scipy.ndimage import uniform_filter1d
import math


samplerate, x0=read("sound\piano.wav")
x=x0[:, 0]
x=x[30000:50000]
T_x = 1 / samplerate
N = x.shape[0]

win_size = 4096
w = hann(win_size, sym=True)
SFT = ShortTimeFFT(w, hop=100, fs=1/T_x, scale_to='magnitude')
Sx = SFT.spectrogram(x)  # perform the STFT
# Sx = np.abs(SFT.stft(x))
Sx=Sx[:, 100:180]

av_Sx = uniform_filter1d(Sx, size=10)
av_Sx_dB = 10 * np.log10(np.fmax(av_Sx, 1e-2))  # limit range to -40 dB

def max_return():
    sx_av=[sum(i)/len(i) for i in av_Sx]
    max_av = []
    # plt.plot([SFT.delta_f*i for i in range(len(sx_av))], sx_av)
    for a in range(len(sx_av)-4):
        if a*SFT.delta_f < 300:
            continue
        if max(sx_av[a-2], sx_av[a-1], sx_av[a], sx_av[a+1], sx_av[a+2]) == sx_av[a] and len(max_av) < 20 and sx_av[a]>1:
            max_av.append(a)
            # plt.plot(SFT.delta_f*a, sx_av[a], color="red", linestyle="", marker="o")
    return max_av


def phase():
    max_av = max_return()
    Sx = SFT.stft(x)
    phase_list = []
    for i in max_av:
        phase_list.append(np.angle(Sx[i][100]))
    phase=np.angle(Sx[max_av[0]])
    plt.plot(phase)


fig1, ax1 = plt.subplots(figsize=(6., 4.))  # enlarge plot a bit
def spec():
    t_lo, t_hi = SFT.extent(N)[:2]  # time range of plot
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

def base():
    f, pxx=signal.welch(x, samplerate, nperseg=8192)
    l_max=[]
    l_max_av=[]
    for i in range(3, len(pxx)):
        if i == 3 or i==len(pxx):
            pass
        else:
            if pxx[i]>pxx[i-1] and pxx[i]>pxx[i+1]:
                if pxx[i]>0.3 and len(l_max)<7:
                    l_max.append(f[i])
                    # plt.plot(Sx[int(f[i]/SFT.delta_f)], label=f[i])
                    # plt.plot(f[i], pxx[i], color="red", linestyle="", marker="o")


    for a, b in enumerate(l_max):
        l_max_av.append(b/(a+1))
    base_f=sum(l_max_av)/len(l_max_av)
    # for i in range(7):
        # plt.plot(Sx[int((i+1)*base_f/SFT.delta_f)], label=(i+1)*base_f)

    plt.semilogy(f, pxx)
    plt.legend()


def aver():
    sx_av=[sum(i)/len(i) for i in av_Sx]
    plt.plot([SFT.delta_f*x for x in range(len(sx_av))], sx_av)
    max_av = max_return()
    for a in max_av:
        plt.plot(SFT.delta_f*a, sx_av[a], color="red", linestyle="", marker="o")
    plt.ylabel("Average Sound Pressure", fontsize=14)
    plt.xlabel("Frequency(hz)", fontsize=14)



def aver_show():
    p=[]
    max_av = max_return()
    for i in max_av:
        sx_means=np.mean(av_Sx[i-math.ceil(20/SFT.delta_f):i+math.ceil(20/SFT.delta_f)+1], axis=0)
        plt.plot([SFT.delta_t*a for a in range(len(av_Sx[0]))], sx_means, label=math.floor(i*SFT.delta_f))
    plt.legend()
    plt.xlabel("time", fontsize=14)
    plt.ylabel("Average Sound Pressure", fontsize=14)

def aver_per():
    
    sx_means = []
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
        plt.plot(p_per[a], label=a+1)
    plt.legend()

    p_per_av = []

    for i in p_per:
        p_per_av.append(sum(i)/len(i))
    return p_per_av

        
    




# plt.semilogy(f, pxx)

# plt.plot(av_Sx_dB[:,1200])
# plt.plot(av_Sx_dB[:,200])

# plt.ylim(-100,100)

# base()
# spec()
# aver_per()
aver_show()
# aver()
# phase()
# max_return()

fig1.tight_layout()
plt.show()