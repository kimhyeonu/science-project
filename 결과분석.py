import matplotlib.pyplot as plt
import math
import numpy as np

g_f=[[42,60,74,84,94,102,108], 
    [54,74,91,102,115,126,138],
    [60,94,114,132,146,161,179],
    [85,115,144,167,188,202,220],
    [135,193,231,267,296,322,349],
    [186,264,319,366,404,445,475]]

u_f=[[179,243,305,360],
     [123,176,214,246],
     [161,217,270,308],
     [185,261,319,369]]

g_ld=[0.008983333,0.00589,0.00362,0.002276667,0.000876667,0.00047]
u_ld=[0.000473333,0.000933333,0.000696667,0.000403333]

g=9.8
length=0.39

def guitar():
    f=[]
    t=[i+1 for i in range(len(g_f[0]))]
    for i in range(len(g_ld)):
        f.append([(1/(2*length))*math.sqrt(g*x/g_ld[i])for x in t])

    for i in g_f:
        plt.plot(t, i, color="red", linewidth=3, marker="o", markersize=5)

    for i in f:
        plt.plot(t, i, color="blue", linewidth=1, marker="o", markersize=3)

def uk():
    f=[]
    t=[i+1 for i in range(len(u_f[0]))]
    for i in range(len(u_ld)):
        f.append([(1/(2*length))*math.sqrt(g*x/u_ld[i])for x in t])

    for i in u_f:
        plt.plot(t, i, color="red", linewidth=3, marker="o", markersize=5)

    for i in f:
        plt.plot(t, i, color="blue", linewidth=1, marker="o", markersize=3)

def guitar_in(n):
    t=[i+1 for i in range(len(g_f[0]))]
    f=[(1/(2*length))*math.sqrt(g*x/g_ld[n-1])for x in t]

    plt.plot(t, g_f[n-1], color="red", linewidth=3, marker="o", markersize=5, label = "experimental value")


    plt.plot(t, f, color="blue", linewidth=1, marker="o", markersize=3, label = "theoretical value")

def uk_in(n):
    t=[i+1 for i in range(len(u_f[0]))]
    f=[(1/(2*length))*math.sqrt(g*x/u_ld[n-1])for x in t]

    plt.plot(t, u_f[n-1], color="red", linewidth=3, marker="o", markersize=5)


    plt.plot(t, f, color="blue", linewidth=1, marker="o", markersize=3)



def root_g():
    f=[]
    t=[i+1 for i in range(len(g_f[0]))]
    
    for i in g_f:
        f.append([2*x/i[3] for x in i])

    for i in f:
        plt.plot(t, i, color="blue", linewidth=1, marker="o", markersize=3)

    plt.plot(np.linspace(min(t), max(t), 500), [math.sqrt(i) for i in np.linspace(min(t), max(t), 500)], color="red", linewidth=5, label="root")



def root_u():
    f=[]
    t=[i+1 for i in range(len(u_f[0]))]
    for i in u_f:
        f.append([2*x/i[3] for x in i])
        

    for i in f:
        plt.plot(t, i, color="blue", linewidth=1, marker="o", markersize=3, label="ukulele")
        
    plt.plot(np.linspace(min(t), max(t), 500), [math.sqrt(i) for i in np.linspace(min(t), max(t), 500)], color="red", linewidth=5, label="root")
    plt.xticks(t)



# root_g()
# guitar()
# uk()
root_u()


plt.grid(True, linestyle='--', alpha=0.6)
# plt.legend(fontsize=12)

plt.show()