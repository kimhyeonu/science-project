import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import ShortTimeFFT
from scipy.signal.windows import gaussian, hann
from scipy.io.wavfile import write, read
from scipy.ndimage import uniform_filter1d
import math
import os

def max_return(n):
    sx_av=[sum(i)/len(i) for i in av_Sx]
    max_av = []
    # plt.plot([SFT.delta_f*i for i in range(len(sx_av))], sx_av)
    for a in range(len(sx_av)-4):
        if a*SFT.delta_f < appro_min_fre[n]:
            continue
        if max(sx_av[a-2], sx_av[a-1], sx_av[a], sx_av[a+1], sx_av[a+2]) == sx_av[a] and len(max_av) < 20 and sx_av[a]>appro_min[n]:
            max_av.append(a)
    #         plt.plot(SFT.delta_f*a, sx_av[a], color="red", linestyle="", marker="o")
    # plt.show() 
    return max_av



fig1, ax1 = plt.subplots(figsize=(6., 4.))  # enlarge plot a bit
def spec(name):
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
    plt.title(name)
    plt.show()



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
    # plt.legend()
    plt.xlabel("time", fontsize=14)
    plt.ylabel("Average Sound Pressure", fontsize=14)

def aver_per(name, n):
    
    sx_means = []
    p_per=[]
    per_list = []
    max_av = max_return(n)

    for i in max_av:
        sx_means.append(np.mean(av_Sx[i-math.ceil(20/SFT.delta_f):i+math.ceil(20/SFT.delta_f)+1], axis=0))


    for a, b in enumerate(sx_means):
        per_list=[]
        for c, d in enumerate(b):
            per_list.append(d/sx_means[0][c])
        p_per.append(per_list)
        # plt.plot(p_per[a], label=a+1)

    p_per_av = []

    for i in p_per:
        p_per_av.append(sum(i)/len(i))
    bar_width = (max(max_av)-min(max_av))*SFT.delta_f/40
    plt.bar([a*SFT.delta_f for a in max_av], p_per_av, width=bar_width, linewidth=0)
    ff = str(int(np.floor(max_av[0]*SFT.delta_f)))
    plt.xlabel("frequency")
    plt.ylabel("ratio(Fundamental=1)")

    # plt.legend()
    plt.title(str(name)+" , Fundamental frequency : "+ff)
    # print(SFT.delta_f*max_av[p_per_av.index(max(p_per_av))])
    plt.show()

    return p_per_av

        
folder_path = 'guitar_har'

# 폴더 내의 파일 목록 가져오기
files = sorted(os.listdir(folder_path))


# appro_min_fre = [300, 200, 150, 120, 80, 70, 130, 120, 200 , 230, 100, 200]
# appro_min = [25, 6.9, 6, 11, 40, 70, 100, 200, 15, 50, 20, 20]
appro_min_fre = [624, 600, 450, 400, 350, 350, 250, 250, 160, 160, 130, 130] 
appro_min = [8, 40, 14, 10, 5, 30, 15, 20, 20, 32, 40, 200]

# print(f"파일 이름: {files[i]}")

for i in range(len(files)):

    file_path = os.path.join(folder_path, files[i])
    samplerate, x0 = read(file_path)
    # samplerate, x0=read("sound\piano.wav")
    # x=x0[:, 0]
    x=x0
    x=x[20000:40000]
    T_x = 1 / samplerate
    N = x.shape[0]

    win_size = 4096
    w = hann(win_size, sym=True)
    SFT = ShortTimeFFT(w, hop=100, fs=1/T_x, scale_to='magnitude')
    # Sx = SFT.spectrogram(x)  # perform the STFT
    Sx = np.abs(SFT.stft(x))
    Sx=Sx[:, 100:180]

    av_Sx = uniform_filter1d(Sx, size=10)
    av_Sx_dB = 10 * np.log10(np.fmax(av_Sx, 1e-2))  # limit range to -40 dB
    # max_return(i)
    aver_per({files[i]}, i)
    # spec({files[i]})



# base()
# spec()
# aver_per()
# aver_show()
# aver()
# phase()
# max_return()

# fig1.tight_layout()
# plt.show()