import os
import matplotlib.pyplot as plt

def plotcomparative_density( lmbd,intervalo, filename1, filename2, directories):
    
    densityL6  = [[],[],[]]
    densityL14 = [[],[],[]]
  
    for l, lbd in enumerate(lmbd):
        os.chdir(directories[l])
        with open (filename1,'r') as file:
            for line in file:
                if not line.startswith('#'):
                    densityL6[l].append(float(line.split()[1]))
        with open(filename2,'r') as file:
            for line in file:
                if not line.startswith('#'):
                    densityL14[l].append(float(line.split()[1]))
        os.chdir('..')
    os.chdir('..')
    
    x=[i * intervalo for i in range(201)]
    x.pop(0)

    densityL6_0=densityL6[0].copy()
    print(len(densityL6_0))
    densityL6_1=densityL6[1].copy()
    print(len(densityL6_1))
    densityL6_2=densityL6[2].copy()
    print(len(densityL6_2))
    densityL14_0=densityL14[0].copy()
    print(len(densityL14_0))
    densityL14_1=densityL14[1].copy()
    print(len(densityL14_1))
    densityL14_2=densityL14[2].copy()
    print(len(densityL14_2))

    #Crear una fila con tres paneles

    fig , axs = plt.subplots (1,3,figsize=(10,8), sharex=True, sharey=True)
    
    # Gráfica 1
    axs[0].plot(x,densityL6_0,color='red',label='L6 λ=0.1')
    axs[0].plot(x,densityL14_0,color='blue',label='L14 λ=0.1')
    axs[0].set_ylabel('Densidad (segmentos \ nm^3)')
    
    # Gráfica 2
    axs[1].plot(x,densityL6_1,color='red',label='L6 λ=0.6')
    axs[1].plot(x,densityL14_1,color='blue',label='L14 λ=0.6')

    # Gráfica 3
    axs[2].plot(x,densityL6_2,color='red', label='L6 λ=1.0')
    axs[2].plot(x,densityL14_2,color='blue',label='L14 λ=1.0')

    for ax in axs:
        ax.set_xlim(intervalo,130) #esto se pone para definir donde inicia y termina el eje x
        ax.set_xlabel('Radio del gel (nm)')
        ax.legend(fontsize=8)

    fig.suptitle('Densidades comparativas', fontsize=16)
    plt.tight_layout() #Ajusta automáticamente los subgráficos haciendo que no se superpongan y que el espacio entre ellas sea uniforme
    plt.savefig('Densidad_comparativa_sep')
    plt.show()

  
#Llamar la función

lmbd = ['0.1', '0.6', '1.0']
directories = ['surface-' + l for l in lmbd]
plotcomparative_density(lmbd,1.5375, 'densityL6_radial.dat','densityL14_radial.dat' , directories)
