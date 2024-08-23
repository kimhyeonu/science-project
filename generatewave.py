import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import ShortTimeFFT
from scipy.signal.windows import gaussian
from scipy.io.wavfile import write, read


samplerate=44100
T_x, N = 1 / samplerate, samplerate*2  # 20 Hz sampling rate for 50 s signal
t_x = np.arange(N) * T_x  # time indexes for signal
# f_i=0 * t_x + 440
# x=1*np.sin(2*np.pi*np.cumsum(f_i)*T_x)
f_i = []
# mul = [1, 0.1, 1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01]
mul = [1, 10, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.01, 0.01, 0.01, 0.01, 0.01]
phase = [0, 0, 0, 0, 0, 0 ,0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0]
fre = [441.4306640625, 882.861328125, 1324.2919921875, 1765.72265625, 2217.919921875, 2670.1171875, 3122.314453125, 3585.2783203125, 4048.2421875, 4521.97265625, 5006.4697265625, 5490.966796875, 5792.431640625]
x=0

for i in range(len(mul)):
    f_i.append(0 * t_x + (i+1)*440)  # varying frequency    
    # f_i.append(0 * t_x + fre[i])  # varying frequency    


for i in range(len(mul)):
    x += mul[i]*np.sin(2*np.pi*(np.cumsum(f_i[i]))*T_x+phase[i])*np.exp(-1*t_x)
x /= np.max(np.abs(x))*5

    # x += 0.01*mul[i]*np.sin(2*np.pi*(np.cumsum(f_i[i]))*T_x)

write("test.wav", samplerate, x.astype(np.float32))