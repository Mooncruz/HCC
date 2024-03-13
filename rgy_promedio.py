import os
import matplotlib.pyplot as plt
from scipy.interpolate import splrep, splev

lmbd=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8']
rgy=[[],[],[],[],[],[],[],[]]
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









    

            
    
