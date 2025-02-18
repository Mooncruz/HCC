import os 
import matplotlib.pyplot as plt
import numpy as np
import math
   
def reader_outgro(filename):
    # Esto permite leer el archivo simu.xtc y dividir por la cantidad de configuraciones guardadas. Tener en cuenta que cada archivo de sumi.gro (una configuracion) esta formado por 3 lineas, inicial, nombre del Gel, segunda cantidad de segmentos y 1 final con las dimensiones de la caja/
    frames=[]
    current_frame=[]
    with open (filename, 'r') as file:
        lines =[]
                
        for line in file:
            line=line.split()
            lines.append(line)
        
        length_file=(len(lines))
        nseg=int(lines[1][0])
        length_one_frame= nseg + 3
        print(length_one_frame)
        side_box= float(lines[-1][0])
        print(side_box)
        print(length_file)
        print(length_file/length_one_frame)
        #Este valor corresponde a la cantidad total de líneas escritas en gro

        # Si hay más de 200 frames, empezamos desde el frame que está 200 posiciones antes del final
        start_index=10*length_one_frame
        for line in lines[start_index:]:
            current_frame.append(line)
            
            if len(current_frame) == length_one_frame:
                frames.append(current_frame)
                current_frame=[]
            
                
        print(len(frames))

    return frames, length_one_frame,side_box

def reader_frames(frames):
              
    #Con esto se organizará la informacion en cada frame obtenido en la función anterior y se organizarán en directorios.Solo se tendrá en cuenta los datos de los segmentos. Las primeras dos filas y la última de cada frame se descarta.
              
    block=[]

    #frames_to_read = frames[-100:]
    #for frame in frames_to_read: 
    for frame in frames:
        current_block = []
        segments = frame[2:-1]
        #se toman los datos desde la 3 linea que en python es 2
        for i,line in enumerate(segments):
            #Debido a que después del segmento 9999 (python sería 9998) la columna de typ y la id se unen, debo generar dos formas de guardar la información. El primer if corresponde a los segmentes que no se unen.
            try:
                l = {'typ': line[1], 'id': int(line[0]), 'coorx': float(line[2]),'coory': float(line[3]), 'coorz': float(line[4])}
                current_block.append(l)
                
                #if line(-1) == 2:
                #    raise IndexError("termina")
                #current_block.append(l)

            except (ValueError, IndexError):
                print("Error en el bloque:", i )

        block.append(current_block)
        #guardo los directorios de cada frames en listas individuales 

    return block
              
def centro_de_masa(block):
    #en esta función se determinará el centro de masa para cada eje y se ajustarán las coordenadas en x,y,z a partir del centro de masa nuevo. 
    
    x=[]
    y=[]
    z=[]
   
    for frame in block:
        x_frame=[]
        y_frame=[]
        z_frame=[]
      
        for index,seg in enumerate(frame):
            x_frame.append(seg['coorx'])
            y_frame.append(seg['coory'])
            z_frame.append(seg['coorz'])
        x.append(x_frame)
        y.append(y_frame)
        z.append(z_frame)

    x_cm=[sum(i) / len(i) for i in x]
    y_cm=[sum(i) / len(i) for i in y]
    z_cm=[sum(i) / len(i) for i in z]
             
    x_new=[[seg - center for seg in inner_x] for inner_x , center in zip(x, x_cm)]
    y_new=[[seg - center for seg in inner_y] for inner_y , center in zip(y, y_cm)]
    z_new=[[seg - center for seg in inner_z] for inner_z , center in zip(z, z_cm)]

    return x_new , y_new , z_new 

def new_block(x_new, y_new, z_new, block):
    #Se reemplazan las coordenadas de 'x' , 'y', 'z' por las nuevas obtenidas en la funcion anterior 'x_new','y_new','z_new' en la variable block que contiene todos los frames ordenada su informacion en directorios

    for i, frame in enumerate(block):
        for j,seg in enumerate(frame):
            seg['coorx'] = x_new[i][j]
            seg['coory'] = y_new[i][j]
            seg['coorz'] = z_new[i][j]

    return block

def discretizarL601(block):
    #En este codigo se extrae las coordenadas de 'x','y','z' en tuplas de cada frame y se organizan en una lista de lista para cada tipo de segmento. 
       
    coordinateL6=[]
    coordinateL0=[]
    coordinateL1=[]
    countL6=0
    countL0=0
    countL1=0

    for frame in block:
        coordinate_L6=[]
        coordinate_L0=[]
        coordinate_L1=[]
        for index,seg in enumerate(frame):
            if seg['typ'] == 'L6':
                countL6+= 1
                coordinate_L6.append((seg['coorx'], seg['coory'], seg['coorz']))

            elif seg['typ'] == 'L0':
                countL0 += 1
                coordinate_L0.append((seg['coorx'], seg['coory'], seg['coorz']))

            elif seg ['typ'] == 'L1':
                countL1 += 1
                coordinate_L1.append((seg['coorx'], seg['coory'], seg['coorz']))

        countL6=0
        countL0=0
        countL1=0
        coordinateL6.append(coordinate_L6)
        coordinateL0.append(coordinate_L0)
        coordinateL1.append(coordinate_L1)
        
        size_L6=sum(len(frame)for frame in coordinateL6)
        size_L0=sum(len(frame)for frame in coordinateL0)
        size_L1=sum(len(frame)for frame in coordinateL1)
        
        frames_gro=len(coordinateL6)
        print(frames_gro)

    return coordinateL6, size_L6, frames_gro, coordinateL0, coordinateL1, size_L0, size_L1


def discretizarL60(block):
    #En este codigo se extrae las coordenadas de 'x','y','z' en tuplas de cada frame y se organizan en una lista de lista para cada tipo de segmento. 
       
    coordinateL6=[]
    coordinateL0=[]
    
    countL6=0
    countL0=0
   

    for frame in block:
        coordinate_L6=[]
        coordinate_L0=[]
        
        for index,seg in enumerate(frame):
            if seg['typ'] == 'L6':
                countL6+= 1
                coordinate_L6.append((seg['coorx'], seg['coory'], seg['coorz']))

            elif seg['typ'] == 'L0':
                countL0 += 1
                coordinate_L0.append((seg['coorx'], seg['coory'], seg['coorz']))

            
        countL6=0
        countL0=0
        coordinateL6.append(coordinate_L6)
        coordinateL0.append(coordinate_L0)
               
        size_L6=sum(len(frame)for frame in coordinateL6)
        size_L0=sum(len(frame)for frame in coordinateL0)
                
        frames_gro=len(coordinateL6)
        print(frames_gro)

    return coordinateL6, size_L6, frames_gro, coordinateL0, size_L0

def radio_gel_por_frameL601(coordinateL6,coordinateL0,coordinateL1):
    #Aunque utilizamos la herramienta gmx gyrate de Gromacs, teniendo la informaciòn de las coordenadas de los segmentos en esta funciòn se determina el radio del gel en cada configuraciòn. 

    L6=[]
    
    for frame in coordinateL6:
        l6=[]
        for tupla in frame:
            x,y,z = tupla
            distancia_euclidiana=(math.sqrt(x**2 + y**2 + z**2))
            l6.append(distancia_euclidiana)          
        L6.append(l6)

    L0=[[math.sqrt(x**2 + y**2 + z**2) for x,y,z in frame]for frame in coordinateL0]
    L1=[[math.sqrt(x**2 + y**2 + z**2) for x,y,z in frame]for frame in coordinateL1]
        
    rL6 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L6]
    rL0 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L0]
    rL1 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L1]

    radio_promedio = [(l6 + l0 + l1) / 3 for l6, l0, l1 in zip (rL6, rL0, rL1)]

    with open ('radio_promedio.dat','w') as file:
        for i , r in enumerate(radio_promedio):
            file.write(f'{i * 10 }\t{r}\n')

    return radio_promedio

def radio_gel_por_frameL60(coordinateL6,coordinateL0):
    #Aunque utilizamos la herramienta gmx gyrate de Gromacs, teniendo la informaciòn de las coordenadas de los segmentos en esta funciòn se determina el radio del gel en cada configuraciòn. 

    L6=[]
        
    for frame in coordinateL6:
        l6=[]
        for tupla in frame:
            x,y,z = tupla
            distancia_euclidiana=(math.sqrt(x**2 + y**2 + z**2))
            l6.append(distancia_euclidiana)          
        L6.append(l6)

    L0=[[math.sqrt(x**2 + y**2 + z**2) for x,y,z in frame]for frame in coordinateL0]
            
    rL6 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L6]
    rL0 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L0]
    
    radio_promedio = [(l6 + l0) / 2 for l6, l0 in zip (rL6, rL0)]

    with open ('radio_promedio.dat','w') as file:
        for i , r in enumerate(radio_promedio):
            file.write(f'{i * 10 }\t{r}\n')

    return radio_promedio

def matriz_L6(coordinateL6, size_L6, frames_gro, num_columns,side_box):
    #divido en varias shells (num_columns) el gel teniendo en cuenta el radio obtenido dividiendo el side_box en dos y ubico cada segmentos de L6 en el shell que corresponda poniendo un 1. Guardo esta información en la variable matrizL6 que estará formado por filas que corresponde a cada segmento de este tipo de todos los frames y las columnas corresponden a cada shell.

    num_rows= size_L6
    r=side_box/2
    intervalo= r / num_columns
    delta=[i * intervalo for i in range(num_columns)]
    

    matrizL6=np.zeros((num_rows,num_columns),dtype=float)

    for index,value in enumerate(delta):
        t_actual=0
        for frame in coordinateL6:
            for tupla in frame:
                x,y,z = tupla
                r_tupla=math.sqrt(x**2 + y**2 + z**2)
                if value <= r_tupla < value + intervalo and np.sum(matrizL6[t_actual,:])==0:
                    matrizL6[t_actual,index] +=1
                t_actual += 1

    for i in range(size_L6):
        suma_filas = np.sum(matrizL6[i,:])
        if suma_filas > 1.0:
             print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')

    return matrizL6, intervalo

def matriz_L0(coordinateL0, size_L0, frames_gro, num_columns,side_box):
    #divido en varias shells (num_columns) el gel teniendo en cuenta el radio obtenido dividiendo el side_box en dos y ubico cada segmentos de L4 en el shell que corresponda poniendo un 1. Guardo esta información en la variable matrizL4 que estará formado por filas que corresponde a cada segmento de este tipo de todos los frames y las columnas corresponden a cada shell.
    
    num_rows= size_L0
    r=side_box/2
    intervalo= r / num_columns
    delta=[i * intervalo for i in range(num_columns)]
    
    matrizL0=np.zeros((num_rows,num_columns),dtype=float)

    for index,value in enumerate(delta):
        t_actual=0
        for frame in coordinateL0:
            for tupla in frame:
                x,y,z = tupla
                r_tupla=math.sqrt(x**2+y**2+z**2)
                if value <= r_tupla < value + intervalo and np.sum(matrizL0[t_actual,:])==0:
                    matrizL0[t_actual,index] +=1
                t_actual += 1

    for i in range(size_L0):
        suma_filas = np.sum(matrizL0[i,:])
        if suma_filas > 1.0:
             print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')

    return matrizL0, intervalo

def matriz_L1(coordinateL1, size_L1, frames_gro, num_columns,side_box):
    #divido en varias shells (num_columns) el gel teniendo en cuenta el radio obtenido dividiendo el side_box en dos y ubico cada segmentos de L1 en el shell que corresponda poniendo un 1. Guardo esta información en la variable matrizL1 que estará formado por filas que corresponde a cada segmento de este tipo de todos los frames y las columnas corresponden a cada shell.
    
    num_rows= size_L1
    r=side_box/2
    intervalo= r / num_columns
    delta=[i * intervalo for i in range(num_columns)]
    
    matrizL1=np.zeros((num_rows,num_columns),dtype=float)

    for index,value in enumerate(delta):
        t_actual=0
        for frame in coordinateL1:
            for tupla in frame:
                x,y,z = tupla
                r_tupla=math.sqrt(x**2+y**2+z**2)
                if value <= r_tupla < value + intervalo and np.sum(matrizL1[t_actual,:])==0:
                    matrizL1[t_actual,index] +=1
                t_actual += 1

    for i in range(size_L1):
        suma_filas = np.sum(matrizL1[i,:])
        if suma_filas > 1.0:
             print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')

    return matrizL1, intervalo



def densidad_L6(matrizL6,frames_gro, intervalo,side_box):
    #tomo la matriz correspondiente y para cada frames sumo la cantidad de segmentos presentes en cada shell 

    r=side_box/2
    rango_volumen=intervalo + 1
    delta=[i *(r/intervalo) for i in range(rango_volumen)]
    delta2=list(delta)
    delta2.pop(0)
    
    volumen=[(4/3)*math.pi * i**3 for i in delta] #volumen del gel desde el centro hasta donde indica el radio (delta)
    
    diferencias_volumen=np.diff(volumen)

    densidadL6=[]
    meanL6=[]

    rows,columns = matrizL6.shape
    num_groups= rows // frames_gro 
    
    for i in range(frames_gro):
        inicio = i * num_groups
        fin = (i + 1) * num_groups
        
        # Seleccionar el grupo de filas
        grupo_filas = matrizL6[inicio:fin, :]
                
        # Calcular la suma de las filas en el grupo
        suma_filas = np.sum(grupo_filas, axis=0)
        #print(f'Suma {i + 1}',np.sum(suma_filas))
        
        # Calcular la densidad para el grupo de filas
        densidad_grupo = np.divide(suma_filas, diferencias_volumen)
        
        # Agregar el resultado a la lista de densidades
        densidadL6.append(np.column_stack((delta2, densidad_grupo)))

    #hallar el promedio de las densidades en cada grupo
    meanL6=np.mean(densidadL6,axis=0)

    promedio=meanL6[:,1]

           
    np.savetxt('densityL6_radial.dat', meanL6,delimiter='\t',header='Columna 1\t\tColumna 2')
    print("Archivo guardado con éxito")

    return densidadL6 , meanL6

def densidad_L0(matrizL0,frames_gro,intervalo,side_box):
    
    r=side_box/2
    rango_volumen=intervalo + 1
    delta=[i *(r/intervalo) for i in range(rango_volumen)]
    delta2=list(delta)
    delta2.pop(0)
    
    volumen=[(4/3)*math.pi * i**3 for i in delta] #volumen del gel desde el centro hasta donde indica el radio (delta)
    
    diferencias_volumen=np.diff(volumen)
    densidadL0=[]
    meanL0=[]

    rows,columns = matrizL0.shape
    num_groups= rows // frames_gro 
    
    for i in range(frames_gro):
        inicio = i * num_groups
        fin = (i + 1) * num_groups
        
        # Seleccionar el grupo de filas
        grupo_filas = matrizL0[inicio:fin, :]
                
        # Calcular la suma de las filas en el grupo
        suma_filas = np.sum(grupo_filas, axis=0)
        #print(f'Suma {i + 1}',np.sum(suma_filas))
        
        # Calcular la densidad para el grupo de filas
        densidad_grupo = np.divide(suma_filas, diferencias_volumen)
        
        # Agregar el resultado a la lista de densidades
        densidadL0.append(np.column_stack((delta2, densidad_grupo)))

    #hallar el promedio de las densidades en cada grupo
    meanL0=np.mean(densidadL0,axis=0)

    promedio=meanL0[:,1]

    np.savetxt('densityL0_radial.dat', meanL0,delimiter='\t',header='Columna 1\t\tColumna 2')
    print("Archivo guardado con éxito")

    return densidadL0 , meanL0

def densidad_L1(matrizL1,frames_gro,intervalo,side_box):

    r=side_box/2
    rango_volumen=intervalo + 1
    delta=[i *(r/intervalo) for i in range(rango_volumen)]
    delta2=list(delta)
    delta2.pop(0)
    
    volumen=[(4/3)*math.pi * i**3 for i in delta] #volumen del gel desde el centro hasta donde indica el radio (delta)
    
    diferencias_volumen=np.diff(volumen)
    densidadL1=[]
    meanL1=[]

    rows,columns = matrizL1.shape
    num_groups= rows // frames_gro 
    
    for i in range(frames_gro):
        inicio = i * num_groups
        fin = (i + 1) * num_groups
        
        # Seleccionar el grupo de filas
        grupo_filas = matrizL1[inicio:fin, :]
                
        # Calcular la suma de las filas en el grupo
        suma_filas = np.sum(grupo_filas, axis=0)
        #print(f'Suma {i + 1}',np.sum(suma_filas))
        
        # Calcular la densidad para el grupo de filas
        densidad_grupo = np.divide(suma_filas, diferencias_volumen)
        
        # Agregar el resultado a la lista de densidades
        densidadL1.append(np.column_stack((delta2, densidad_grupo)))

    #hallar el promedio de las densidades en cada grupo
    meanL1=np.mean(densidadL1,axis=0)

    promedio=meanL1[:,1]

    np.savetxt('densityL1_radial.dat', meanL1,delimiter='\t',header='Columna 1\t\tColumna 2')
    print("Archivo guardado con éxito")

    return densidadL1 , meanL1

system= ['surface-','random-','core-']    
lmbd = ['0.0','0.7','1.2']

for sys in system:
    for lbd in lmbd:
        os.chdir(sys+lbd)
    
        frames,length_one_frame,side_box = reader_outgro('out.gro')
        block = reader_frames(frames)
        x_new , y_new , z_new=centro_de_masa(block)
        block=new_block(x_new,y_new,z_new,block)
        coordinateL6, size_L6, frames_gro, coordinateL0, coordinateL1, size_L0, size_L1=discretizarL601(block)
        matrizL6, intervalo =matriz_L6(coordinateL6, size_L6, frames_gro,200,side_box)
        densidadL6,meanL6 = densidad_L6(matrizL6,frames_gro,200,side_box)
        del matrizL6, densidadL6, meanL6, coordinateL6,size_L6
        matrizL0,intervalo=matriz_L0(coordinateL0, size_L0, frames_gro,200,side_box)
        densidadL0,meanL0 = densidad_L0(matrizL0,frames_gro,200,side_box)
        del matrizL0, densidadL0, meanL0, coordinateL0,size_L0,intervalo
        matrizL1,intervalo=matriz_L1(coordinateL1, size_L1, frames_gro,200,side_box) 
        densidadL1,meanL1 = densidad_L1(matrizL1,frames_gro,200,side_box)
        del matrizL1, densidadL1, meanL1, coordinateL1, size_L1,intervalo

        os.chdir('..')


