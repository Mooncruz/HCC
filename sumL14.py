import os
import numpy as np

#cargas los datos de densidad de L1 y L4

lmdb=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']

x=[i * 2.3925 for i in range(201)]
x.pop(0)
densityL4=[[]for _ in range(10)]
densityL1=[[]for _ in range(10)]
densityL14=[[]for _ in range(10)]

for l,lbd in enumerate (lmdb):
    os.chdir('surface50-'+ lbd)
    with open ('densityL4_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                densityL4[l].append(float(line.split()[1]))
    with open ('densityL1_radial.dat','r') as file:
        for line in file:
            if not line.startswith('#'):
                densityL1[l].append(float(line.split()[1]))

    densityL14 = [L1 + L4 for L1, L4 in zip(densityL1[l], densityL4[l])]

    with open ('densityL14_radial.dat','w') as file:
        for radio,densidad in zip(x,densityL14):
            file.write(f'{radio}\t{densidad}\n')
                      
        
    os.chdir('..')

    
