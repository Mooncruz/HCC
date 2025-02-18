import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import Akima1DInterpolator




lmbd=['0.0','0.7','1.2']



surfaceL6=[[],[],[]]
surfaceL1=[[],[],[]]
randomL6=[[],[],[]]
randomL1=[[],[],[]]
coreL6=[[],[],[]]
coreL1=[[],[],[]]

for l,lbd in enumerate (lmbd):
    os.chdir('surface-'+lbd)
    with open ('densityL6_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                surfaceL6[l].append(float(line.split()[1]))
    with open ('densityL1_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                surfaceL1[l].append(float(line.split()[1]))
    os.chdir('..')


for l,lbd in enumerate (lmbd):
    os.chdir('random-'+lbd)
    with open ('densityL6_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                randomL6[l].append(float(line.split()[1]))
    with open('densityL1_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                randomL1[l].append(float(line.split()[1]))
    os.chdir('..')


for l,lbd in enumerate (lmbd):
    os.chdir('core-'+lbd)
    with open ('densityL6_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                coreL6[l].append(float(line.split()[1]))
    with open('densityL1_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                coreL1[l].append(float(line.split()[1]))
    os.chdir('..')




with open("core-0.0/densityL6_radial.dat", "r") as data:
    for line in data:
        if not line.startswith("#"):  
            intervalo = float(line.split()[0])  # Extraer el primer número
            break  # Solo necesitamos el primero

print(f"Primer número: {intervalo}")
    
x=[i* intervalo for i in range (201)]
x.pop(0)

#Se realiza una spline para hacer la curva más suave. 

spline1=Akima1DInterpolator(x,surfaceL6[0])
spline2=Akima1DInterpolator(x,surfaceL6[1])
spline3=Akima1DInterpolator(x,surfaceL6[2])
spline4=Akima1DInterpolator(x,surfaceL1[0])
spline5=Akima1DInterpolator(x,surfaceL1[1])
spline6=Akima1DInterpolator(x,surfaceL1[2])

x_i=np.linspace(0,80,1000)

surfaceL6_0=spline1(x_i)
surfaceL6_1=spline2(x_i)
surfaceL6_2=spline3(x_i)
surfaceL1_0=spline4(x_i)
surfaceL1_1=spline5(x_i)
surfaceL1_2=spline6(x_i)

spline7=Akima1DInterpolator(x,randomL6[0])
spline8=Akima1DInterpolator(x,randomL6[1])
spline9=Akima1DInterpolator(x,randomL6[2])
spline10=Akima1DInterpolator(x,randomL1[0])
spline11=Akima1DInterpolator(x,randomL1[1])
spline12=Akima1DInterpolator(x,randomL1[2])

randomL6_0=spline7(x_i)
randomL6_1=spline8(x_i)
randomL6_2=spline9(x_i)
randomL1_0=spline10(x_i)
randomL1_1=spline11(x_i)
randomL1_2=spline12(x_i)

spline13=Akima1DInterpolator(x,coreL6[0])
spline14=Akima1DInterpolator(x,coreL6[1])
spline15=Akima1DInterpolator(x,coreL6[2])
spline16=Akima1DInterpolator(x,coreL1[0])
spline17=Akima1DInterpolator(x,coreL1[1])
spline18=Akima1DInterpolator(x,coreL1[2])

coreL6_0=spline13(x_i)
coreL6_1=spline14(x_i)
coreL6_2=spline15(x_i)
coreL1_0=spline16(x_i)
coreL1_1=spline17(x_i)
coreL1_2=spline18(x_i)

#Se realliza un gráfico con 9 subgráficas. Tres filas y tres columnas. Las filas indican la funcionalizacion del sistema y las columnas, el lambda analizado

fig,(axs1,axs2,axs3)= plt.subplots (3,3,figsize=(8,8),sharex=True)

x_major_ticks=(10,20,30,40,50,60,70,80)
x_minor_ticks=(5,15,25,35,45,55,65,75)
y_major_ticks0=(0.0,0.02,0.04,0.06,0.08,0.10,0.12,0.14)
y_minor_ticks0=(0.01,0.03,0.05,0.07,0.09,0.11,0.13)
y_major_ticks1=(0.0,0.02,0.04,0.06,0.08)
y_minor_ticks1=(0.01,0.03,0.05,0.07,0.09)
y_major_ticks2=(0.0,0.2,0.4,0.6,0.8)
y_minor_ticks2=(0.1,0.3,0.5,0.7,0.9)

# gráfica 1,0
axs1[0].plot(x_i,randomL6_0,color='red')
axs1[0].plot(x_i,randomL1_0,color='blue')
axs1[0].set_xticks(x_major_ticks)
axs1[0].set_xticks(x_minor_ticks,minor=True)
axs1[0].set_yticks(y_major_ticks1)
axs1[0].set_yticks(y_minor_ticks1,minor=True)
axs1[0].set_ylabel('RF\n'r' Density (seg/nm$^3$)',fontsize=12)
axs1[0].set_ylim(0, 0.095)
axs1[0].set_title('25°C',fontsize=12)


# gráfica 1,1
axs1[1].plot(x_i,randomL6_1,color='red')
axs1[1].plot(x_i,randomL1_1,color='blue')
axs1[1].set_xticks(x_major_ticks)
axs1[1].set_xticks(x_minor_ticks,minor=True)
axs1[1].set_yticklabels([])
axs1[1].set_yticks(y_major_ticks1)
axs1[1].set_yticks(y_minor_ticks1,minor=True)
axs1[1].set_ylim(0, 0.095)
axs1[1].set_title('32°C',fontsize=12)

# gráfica 1,2
axs1[2].plot(x_i,randomL6_2,color='red',label='NIPAm')
axs1[2].plot(x_i,randomL1_2,color='blue',label='EG')
axs1[2].set_xticks(x_major_ticks)
axs1[2].set_xticks(x_minor_ticks,minor=True)
axs1[2].set_yticklabels([])
axs1[2].set_yticks(y_major_ticks1)
axs1[2].set_yticks(y_minor_ticks1,minor=True)
axs1[2].set_ylim(0, 0.095)
axs1[2].set_title('37°C',fontsize=12)
axs1[2].legend(fontsize=10, frameon=False, loc='upper right')

# gráfica 2,0
axs2[0].plot(x_i,coreL6_0,color='red')
axs2[0].plot(x_i,coreL1_0,color='blue')
axs2[0].set_xticks(x_major_ticks)
axs2[0].set_xticks(x_minor_ticks,minor=True)
axs2[0].set_yticks(y_major_ticks2)
axs2[0].set_yticks(y_minor_ticks2,minor=True)
axs2[0].set_ylabel('CF\n'r' Density (seg/nm$^3$)',fontsize=12,labelpad=11)
axs2[0].set_ylim(0, 1.0)

# gráfica 2,1
axs2[1].plot(x_i,coreL6_1,color='red')
axs2[1].plot(x_i,coreL1_1,color='blue')
axs2[1].set_xticks(x_major_ticks)
axs2[1].set_xticks(x_minor_ticks,minor=True)
axs2[1].set_yticklabels([])
axs2[1].set_yticks(y_major_ticks2)
axs2[1].set_yticks(y_minor_ticks2,minor=True)
axs2[1].set_ylim(0, 1.0)

# gráfica 2,2
axs2[2].plot(x_i,coreL6_2,color='red')
axs2[2].plot(x_i,coreL1_2,color='blue')
axs2[2].set_xticks(x_major_ticks)
axs2[2].set_xticks(x_minor_ticks,minor=True)
axs2[2].set_yticklabels([])
axs2[2].set_yticks(y_major_ticks2)
axs2[2].set_yticks(y_minor_ticks2,minor=True)
axs2[2].set_ylim(0, 1.0)

# gráfica 2,0
axs3[0].plot(x_i,surfaceL6_0,color='red')
axs3[0].plot(x_i,surfaceL1_0,color='blue')
axs3[0].set_xticks(x_major_ticks)
axs3[0].set_xticks(x_minor_ticks,minor=True)
axs3[0].set_yticks(y_major_ticks0)
axs3[0].set_yticks(y_minor_ticks0, minor=True)
axs3[0].set_ylabel('SF\n'r'Density (seg/nm$^3$)',fontsize=12)
axs3[0].set_xlabel('r (nm)',fontsize=12)
axs3[0].set_ylim(0, 0.145)
axs3[0].set_xlim(1,80)

# gráfica 2,1
axs3[1].plot(x_i,surfaceL6_1,color='red')
axs3[1].plot(x_i,surfaceL1_1,color='blue')
axs3[1].set_xticks(x_major_ticks)
axs3[1].set_xticks(x_minor_ticks,minor=True)
axs3[1].set_yticklabels([])
axs3[1].set_yticks(y_major_ticks0)
axs3[1].set_yticks(y_minor_ticks0,minor=True)
axs3[1].set_ylim(0, 0.145)
axs3[1].set_xlabel('r (nm)',fontsize=12)
axs3[1].set_xlim(1,80)

# gráfica 2,2
axs3[2].plot(x_i,surfaceL6_2,color='red',label='NIPAm')
axs3[2].plot(x_i,surfaceL1_2,color='blue',label='EG')
axs3[2].set_xticks(x_major_ticks)
axs3[2].set_xticks(x_minor_ticks,minor=True)
axs3[2].set_yticklabels([])
axs3[2].set_yticks(y_major_ticks0)
axs3[2].set_yticks(y_minor_ticks0,minor=True)
axs3[2].set_ylim(0, 0.145)
axs3[2].set_xlabel('r (nm)',fontsize=12)
axs3[2].set_xlim(1,80)

# Función para personalizar los ejes
def setup(ax):
    ax.tick_params(axis='y',which='both',left=True,right=True,direction='in')
    ax.tick_params(axis='x',which='both',bottom=True,top=True,direction='in')
    ax.tick_params(width=1.5,length=4,labelsize=10)
    ax.tick_params(which='minor',length=3,width=1.5)
    ax.tick_params(axis='both',which='major')
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
   
    
# Aplicar la configuración a cada subgráfico
setup(axs1[0])
setup(axs1[1])
setup(axs1[2])
setup(axs2[0])
setup(axs2[1])
setup(axs2[2])
setup(axs3[0])
setup(axs3[1])
setup(axs3[2])

#Se realiza un inset para el sistema CF (A) para mostrar en más detalle.

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

axins = inset_axes(axs2[0], width="50%", height="50%", loc='upper right')
axins.plot(x_i,coreL6_0, 'red')
axins.plot(x_i,coreL1_0, 'blue')
axins.set_xlim(1, 50)
axins.set_ylim(0,0.1)
axins.set_xticks([10,20,30,40,50])
axins.set_xticks([15,25,35,45],minor=True)
axins.set_yticks([0,0.04,0.08])
axins.set_yticks([0.02,0.06],minor=True)
axins.tick_params(axis='y',which='both',left=True,right=False,direction='in')
axins.tick_params(axis='x',which='both',bottom=True,top=False,direction='in')
axins.tick_params(width=1.5,length=4,labelsize=10)
axins.tick_params(which='minor',length=3,width=1.5)
axins.tick_params(axis='both',which='major',labelsize=6)
axins.spines['top'].set_linewidth(1.5)
axins.spines['bottom'].set_linewidth(1.5)
axins.spines['right'].set_linewidth(1.5)
axins.spines['left'].set_linewidth(1.5)


plt.tight_layout() #ajusta los espacios entre gràficos
plt.savefig('density_profile.png',dpi=300)
plt.show()
