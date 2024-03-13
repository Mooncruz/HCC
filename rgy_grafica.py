import os
import matplotlib.pyplot as plt
import numpy as np


lmbd=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']
rgy=[[],[],[],[],[],[],[],[],[],[]]
promedio=[]

for l,lbd in enumerate(lmbd):

    directorio='surface25-'+lbd
    os.chdir(directorio)
    with open('gyrate.xvg','r') as gyrt:
        for linea in gyrt:
            if not linea.startswith('#') and not linea.startswith('@'):
                rgy[l].append(float(linea.split()[1]))
    os.chdir('..')
    promedio.append(sum(rgy[l])/len(rgy[l]))
print(promedio)


plt.plot(lmbd,promedio,color='red',label='Surfacegel30-25')
plt.xlabel('λ')
plt.ylabel('Radius of gyration (nm)')
plt.legend()
plt.savefig('gyrate25_nipam30.png')
plt.show()






    

            
    
