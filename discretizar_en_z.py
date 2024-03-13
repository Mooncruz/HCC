import matplotlib.pyplot as plt
import numpy as np


def reader_outgro(filename):
    # Esto permite leer el archivo simu.xtc y dividir por la cantidad de configuraciones guardadas. Tener en cuenta que cada archivo de sumi.gro (una configuracion) esta formado por 3 lineas, inicial, nombre del Gel, segunda cantidad de segmentos y 1 final con las dimensiones de la caja/
    frames=[]
    current_frame=[]
    with open (filename, 'r') as file:
        lines =[]
        contador=0
        for line in file:
            line=line.split()
            lines.append(line)
        length_file=(len(lines))
        length_one_frame=67569
        #Este valor corresponde a la cantidad total de líneas escritas en gro
        
        for line in lines:
            current_frame.append(line)
            contador +=1
            if contador == length_one_frame:
                frames.append(current_frame)
                current_frame=[]
                contador=0

    return frames

def reader_frames(frames):
    #Con esto se organizará la informacion en cada frame obtenido en la función anterior y se organizarán en directorios.Solo se tendrá en cuenta los datos de los segmentos. Las primeras dos filas y la última de cada frame se descarta.
    
    block=[]

    for frame in frames:
        current_block = []
        segments = frame[2:]
        #se toman los datos desde la 3 linea que en python es 2
        for i, line in enumerate(segments):
            #Debido a que después del segmento 9999 (python sería 9998) la columna de typ y la id se unen, debo generar dos formas de guardar la información. El primer if corresponde a los segmentes que no se unen.
            if i <= 9998:
                try:
                    l = {'system': line[0], 'typ': line[1], 'id': int(line[2]), 'coorx': float(line[3]),'coory': float(line[4]), 'coorz': float(line[5])}
                    current_block.append(l)
                     
                except (ValueError, IndexError):
                    print("Error en el bloque:", current_block)

            # Este elif va a tomar el segundo dato por línea y lo separará en dos partes para distinguir el nombre del segmento y el número del mismo. y se organizan en los directorios
            elif i >= 9999:
                parte=line[1]
                parte1 = parte[:2]
                parte2 = parte[2:]
                
                try:
                    l = {'system': line[0], 'typ': parte1, 'id': int(parte2), 'coorx': float(line[2]),'coory': float(line[3]), 'coorz': float(line[4])}
                    #print(l)
                          
                    if len(l) ==3:
                        raise IndexError('Se terminó')
                    current_block.append(l)

                except (ValueError):
                    print('Fin de frame')
                
        block.append(current_block)
        #guardo los directorios de cada frames en listas individuales
    return block

def discretiza(block):
    

    coordinate_z_L6=[]
    coordinate_z_L4=[]
    coordinate_z_L1=[]
    count1=0
    count2=0
    count3=0

    for frame in block:
        coordinate_L6= []
        coordinate_L4= []
        coordinate_L1= []
        for index,seg in enumerate(frame):
            if seg['typ'] == 'L6':
                count1 += 1
                coordinate_L6.append(seg['coorz'])
        
            elif seg['typ'] == 'L4':
                count2 += 1
                coordinate_L4.append(seg['coorz'])
        
            elif seg['typ'] == 'L1':
                count3 += 1
                coordinate_L1.append(seg['coorz'])

            
        count1 = 0
        coordinate_z_L6.append(coordinate_L6)
        count2 = 0
        coordinate_z_L4.append(coordinate_L4)
        count3 = 0
        coordinate_z_L1.append(coordinate_L1)

        size_L6=sum(len(frame)for frame in coordinate_z_L6)
        size_L4=sum(len(frame)for frame in coordinate_z_L4)
        size_L1=sum(len(frame)for frame in coordinate_z_L1)
        frames_gro=len(coordinate_z_L1)
        
    return coordinate_z_L6, coordinate_z_L4, coordinate_z_L1, size_L6, size_L4,size_L1, frames_gro


def matriz_z(coordinate_z_L6, coordinate_z_L4, coordinate_z_L1, size_L6, size_L4, size_L1):
    
    num_rowsL6= size_L6
    num_rowsL4= size_L4
    num_rowsL1= size_L1
    num_columns=50
    intervalo=12.3
    values = [round(i * intervalo,2) for i in range(num_columns)]

    matriz_L6=np.zeros((num_rowsL6,num_columns),dtype=float)
    matriz_L4=np.zeros((num_rowsL4,num_columns),dtype=float)
    matriz_L1=np.zeros((num_rowsL1,num_columns),dtype=float)

    
    for x,value in enumerate(values):
        t_actual=0
        for frame in coordinate_z_L6:
            for i in frame:
                if value <= i < value + intervalo and np.sum(matriz_L6[t_actual,:])==0:
                    matriz_L6[t_actual,x] += 1
                t_actual += 1

        t_actual=0
        for frame in coordinate_z_L4:
            for i in frame:
                if value <= i <= value + intervalo and np.sum(matriz_L4[t_actual,:])==0:
                    matriz_L4[t_actual,x] += 1
                t_actual += 1

        t_actual=0
        for frame in coordinate_z_L1:
            for i in frame:
                if value <= i <= value + intervalo and np.sum(matriz_L1[t_actual,:])==0:
                    matriz_L1[t_actual,x] += 1
                t_actual += 1

    for i in range(size_L6):
        suma_filas=np.sum(matriz_L6[i,:])
        if suma_filas > 1.0:
            print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')
    for i in range(size_L4):
        suma_filas=np.sum(matriz_L4[i,:])
        if suma_filas > 1.0:
            print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')
    for i in range(size_L1):
        suma_filas=np.sum(matriz_L1[i,:])
        if suma_filas > 1.0:
            print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')

    np.savetxt('matriz_L6_all.dat',matriz_L6, fmt='%d',delimiter=',')
    np.savetxt('matriz_L4_all.dat',matriz_L4, fmt='%d',delimiter=',')
    np.savetxt('matriz_L1_all.dat',matriz_L1, fmt='%d',delimiter=',')

    return matriz_L6, matriz_L4, matriz_L1, values

def densidad_L6(matriz_L6,values,frames_gro):

    volumen_slide = 12.3 *615 *615 
    densidad_L6=[]
    mean_L6=[]

    rows , columns = matriz_L6.shape
    num_groups= rows // frames_gro 
    

    for i in range(frames_gro):
        inicio = i * num_groups
        fin = (i + 1) * num_groups
        
        # Seleccionar el grupo de filas
        grupo_filas = matriz_L6[inicio:fin, :]

                
        # Calcular la suma de las filas en el grupo
        suma_filas = np.sum(grupo_filas, axis=0)
        print(f'Suma {i + 1}',np.sum(suma_filas))
        
        # Calcular la densidad para el grupo de filas
        densidad_grupo = np.divide(suma_filas, volumen_slide)
        
        # Agregar el resultado a la lista de densidades
        densidad_L6.append(np.column_stack((values, densidad_grupo)))

    #hallar el promedio de las densidades en cada grupo
    mean_L6=np.mean(densidad_L6,axis=0)

    promedio=mean_L6[:,1]

    integral_L6=np.trapz(promedio)
    print(integral_L6)

    np.savetxt('densityL_6np.dat', mean_L6,delimiter='\t',header='Columna 1\t\tColumna 2')
    print("Archivo guardado con éxito")

    return densidad_L6, mean_L6, integral_L6

def graficar_densidadL6(mean_L6):
    
    plt.plot(mean_L6[:,0],mean_L6[:,1])
    plt.show()

    return ()
    
     
frames = reader_outgro('out.gro')

block =reader_frames(frames)

coordinate_z_L6 , coordinate_z_L4 , coordinate_z_L1 , size_L6 , size_L4, size_L1 , frames_gro= discretiza(block)

matriz_L6 , matriz_L4 , matriz_L1, values= matriz_z(coordinate_z_L6 , coordinate_z_L4 , coordinate_z_L1 , size_L6 , size_L4, size_L1)

densidad_L6, mean_L6, integral_L6= densidad_L6( matriz_L6, values, frames_gro )

graficar_densidadL6(mean_L6)
              


