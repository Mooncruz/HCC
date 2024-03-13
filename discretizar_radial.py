import matplotlib.pyplot as plt
import numpy as np
import math
import os


def reader_outgro(filename):
    
    # Esto permite leer el archivo simu.xtc y dividirlo por la cantidad de configuraciones guardadas. Tener en cuenta que cada configuraciòn del simu.gro esta formado por 3 lineas iniciales, nombre del Gel, cantidad de segmentos y 1 final con las dimensiones de la caja/

    frames=[] # Lista que contendrà todas las configuraciones 
    current_frame= []# Lista que contendrà una sola configuraciòn 
    with open (filename, 'r') as file:
        lines =[]
        
        for line in file:
            lines.append(line.split())
            
        length_file=(len(lines))
        nseg=int(lines[1][0])
        length_one_frame= nseg + 3
        print(length_one_frame) #Este valor corresponde a la cantidad total de líneas escritas en una configuracion
        
        side_box= float(lines[-1][0])
        print(side_box)
        
        start_index=max(0,length_file - (300 * length_one_frame)) #Esta variable genera un indice. Se da la opcion de escoger cuantas configuraciones se guardaràn en la lista de frames. La funciòn max escoge el nùmero màs grande de los dos argumentos que se le den. 
        for line in lines[start_index:]: # Este bucle iniciarà desde la configuraciòn dada por el indice en la variable start_index hasta la ùltima. 
            current_frame.append(line)
            
            if len(current_frame) == length_one_frame: #Cuando la lista actual tenga la misma longitud que un frames definido arriba se guardarà en la lista frames y de abrirà uno nuevo. n
                frames.append(current_frame)
                current_frame=[]
                                
        print(len(frames))

    return frames, side_box

def reader_frames(frames):
              
    #Con esto se organizará en directorios los datos de los segmentos de cada configuraciòn obtenido en la función anterior. Las primeras dos filas y la última de cada current_frame se descartan.
              
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
                        #Cuando llega a la lìnea que tiene definiado los lados de la caja, guarda los directorios en una lista denominada current_block
                        raise IndexError('Se terminó')
                    current_block.append(l)

                except (ValueError):
                    print("Fin bloque")
                
        block.append(current_block)
        #guardo los directorios de cada frames en listas individuales 

    return block
              
def centro_de_masa(block):
    #en esta función se determinará el centro de masa de cada eje de cada configuraciòn y se ajustarán las coordenadas en x,y,z a partir del centro de masa nuevo. 
    
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

    #Se obtiene el centro de masa de cada eje en cada configuraciòn
    x_cm=[sum(i) / len(i) for i in x]
    y_cm=[sum(i) / len(i) for i in y]
    z_cm=[sum(i) / len(i) for i in z]

    #Se obtiene la nueva coordenada de cada segmento 
    x_new=[[seg - center for seg in inner_x] for inner_x , center in zip(x, x_cm)]
    y_new=[[seg - center for seg in inner_y] for inner_y , center in zip(y, y_cm)]
    z_new=[[seg - center for seg in inner_z] for inner_z , center in zip(z, z_cm)]

    return x_cm , x_new , y_cm , y_new , z_cm , z_new

def new_block(x_new, y_new, z_new, block):
    #Se reemplazan las coordenadas de 'x' , 'y', 'z' por las nuevas obtenidas en la funcion anterior 'x_new','y_new','z_new' en la variable block que contiene todos las configuraciones ordenada en directorios

    for i, frame in enumerate(block):
        for j,seg in enumerate(frame):
            seg['coorx'] = x_new[i][j]
            seg['coory'] = y_new[i][j]
            seg['coorz'] = z_new[i][j]

    return block

def discretizar(block):
    #En este codigo se extrae las coordenadas de 'x','y','z' en tuplas de cada frame y se organizan en una lista de lista para cada tipo de segmento.
       
    coordinateL6=[]
    coordinateL4=[]
    coordinateL1=[]
    
    for frame in block:
        coordinate_L6=[]
        coordinate_L4=[]
        coordinate_L1=[]
        for index,seg in enumerate(frame):
            if seg['typ'] == 'L6':
                coordinate_L6.append((seg['coorx'], seg['coory'], seg['coorz']))

            elif seg['typ'] == 'L4':
                coordinate_L4.append((seg['coorx'], seg['coory'], seg['coorz']))

            elif seg ['typ'] == 'L1':
                coordinate_L1.append((seg['coorx'], seg['coory'], seg['coorz']))
            
        coordinateL6.append(coordinate_L6)
        coordinateL4.append(coordinate_L4)
        coordinateL1.append(coordinate_L1)
        
        size_L6=sum(len(frame)for frame in coordinateL6)
        size_L4=sum(len(frame)for frame in coordinateL4)
        size_L1=sum(len(frame)for frame in coordinateL1)
        
        frames_gro=len(coordinateL6)

    return coordinateL6, size_L6, frames_gro, coordinateL4, coordinateL1, size_L4, size_L1

def radio_gel_por_frame(coordinateL6,coordinateL4,coordinateL1):
    #Aunque utilizamos la herramienta gmx gyrate de Gromacs, teniendo la informaciòn de las coordenadas de los segmentos en esta funciòn se determina el radio del gel en cada configuraciòn. 

    L6=[]
    L4=[]
    L1=[]

    for frame in coordinateL6:
        l6=[]
        for tupla in frame:
            x,y,z = tupla
            distancia_euclidiana=(math.sqrt(x**2 + y**2 + z**2))
            l6.append(distancia_euclidiana)          
        L6.append(l6)

    L4=[[math.sqrt(x**2 + y**2 + z**2) for x,y,z in frame]for frame in coordinateL4]
    L1=[[math.sqrt(x**2 + y**2 + z**2) for x,y,z in frame]for frame in coordinateL1]
        
    rL6 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L6]
    rL4 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L4]
    rL1 = [math.sqrt(sum(distancia**2 for distancia in frame) / len(frame)) for frame in L1]

    radio_promedio = [(l6 + l4 + l1) / 3 for l6, l4, l1 in zip (rL6, rL4, rL1)]

    with open ('radio_promedio.dat','w') as file:
        for r , s in zip (radio_promedio, range(0,(len(radio_promedio)+10),10)):
            file.write(f'{s}\t{r}\n')

    return radio_promedio

def matriz_L6(coordinateL6, size_L6, frames_gro, num_columns,side_box):
    #divido en varias capas (num_columns) el gel teniendo en cuenta el radio obtenido dividiendo el side_box en dos y ubico cada segmentos de L6 en la capas que corresponda poniendo un 1. Guardo esta información en la variable matrizL6 que estará formado por filas que corresponde a cada segmento de este tipo de todos los frames y las columnas corresponden a cada capa.

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
                #calcula la distancia euclidiana desde el origen hasta un punto en el espacio tridimensional 
                if value <= r_tupla < value + intervalo and np.sum(matrizL6[t_actual,:])==0:
                    # compara la distancia euclidiana de la tupla con el valor de la capa que se està iterando y con la siguiente capa para definir a donde pertenece ese segmento. 
                    matrizL6[t_actual,index] +=1
                t_actual += 1

    for i in range(size_L6):
        #Este bucle confirmarà si la matriz guardò para cada segmento una ùnica ubicaciòn en una capa dentro del gel.  
        suma_filas = np.sum(matrizL6[i,:])
        if suma_filas > 1.0:
             print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')

    #np.savetxt('matrizL6_radial.dat',matrizL6, fmt='%d',delimiter=',')

    return matrizL6

def matriz_L4(coordinateL4, size_L4, frames_gro, num_columns,side_box):
    #divido en varias capas (num_columns) el gel teniendo en cuenta el radio obtenido dividiendo el side_box en dos y ubico cada segmentos de L6 en la capas que corresponda poniendo un 1. Guardo esta información en la variable matrizL6 que estará formado por filas que corresponde a cada segmento de este tipo de todos los frames y las columnas corresponden a cada capa.
    
    num_rows= size_L4
    r=side_box/2
    intervalo= r / num_columns
    delta=[i * intervalo for i in range(num_columns)]
   
    matrizL4=np.zeros((num_rows,num_columns),dtype=float)

    for index,value in enumerate(delta):
        t_actual=0
        for frame in coordinateL4:
            for tupla in frame:
                x,y,z = tupla
                r_tupla=math.sqrt(x**2+y**2+z**2)
                if value <= r_tupla < value + intervalo and np.sum(matrizL4[t_actual,:])==0:
                    matrizL4[t_actual,index] +=1
                t_actual += 1

    for i in range(size_L4):
        suma_filas = np.sum(matrizL4[i,:])
        if suma_filas > 1.0:
             print(f'la suma de la fila {i +1} es mayor que 1.0:{suma_filas}')
        elif suma_filas < 1.0:
            print(f'la suma de la fila {i +1} es menor que 1.0:{suma_filas}')

    #np.savetxt('matrizL4_radial.dat',matrizL4, fmt='%d',delimiter=',')

    return matrizL4

def matriz_L1(coordinateL1, size_L1, frames_gro, num_columns,side_box):
    #divido en varias capas (num_columns) el gel teniendo en cuenta el radio obtenido dividiendo el side_box en dos y ubico cada segmentos de L6 en la capas que corresponda poniendo un 1. Guardo esta información en la variable matrizL6 que estará formado por filas que corresponde a cada segmento de este tipo de todos los frames y las columnas corresponden a cada capa.
    
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

    #np.savetxt('matrizL1_radial.dat',matrizL1, fmt='%d',delimiter=',')

    return matrizL1

def densidad_L6(matrizL6,frames_gro, intervalo,side_box):
    #tomo la matriz correspondiente para el tipo de segmento y para cada configuración  sumo la cantidad de segmentos presentes en cada capa y se divide con el volumen de la capa. Al finalizar se sacará el promedio por cada capa de cada configuración y se obtendrá densidad promedio de las configuraciones abordadas. 

    r=side_box/2
    rango_volumen=intervalo + 1
    # Agrego un rango màs para determinar el volumen de la ùltima capa
    delta=[i *(r/intervalo) for i in range(rango_volumen)]
    delta2=list(delta)
    delta2.pop(0)
    #Es el tamaño de la lista para poder coincidir con la lista diferencias_volumen 
    
    volumen=[(4/3)*math.pi * i**3 for i in delta]
    #volumen del gel desde el centro hasta donde indica el radio (delta)
    
    diferencias_volumen=np.diff(volumen)
    #se determina el valor del volumen de cada capa sin incluir a las anteriores si tiene. 

    densidadL6=[]
    meanL6=[]

    rows,columns = matrizL6.shape
    num_groups= rows // frames_gro
    #Indico la cantidad de segmentos que hay por configuraciòn 
    
    for i in range(frames_gro):
    #Indico cual es el inicio y final de cada configuracion.
        inicio = i * num_groups
        fin = (i + 1) * num_groups

        grupo_filas = matrizL6[inicio:fin, :]
        #Selecciono las filas por configuración
                
        suma_filas = np.sum(grupo_filas, axis=0)
        # sumo las columnas de cada una de las filas
        
        densidad_grupo = np.divide(suma_filas, diferencias_volumen)
        # Calculo la densidad de cada capa concénctrica dividiendo el resulado de segmentos por fila por el volumen respectivo. 

        densidadL6.append(np.column_stack((delta2, densidad_grupo)))
        #Guardo el resultado en la lista en dos columnas. La primera representa la distancia radial de la capa y el segundo la densidad.
    
    meanL6=np.mean(densidadL6,axis=0)
    # Hallo el promedio de las densidades de todas las configuraciones

    np.savetxt('densityL6_radialg.dat', meanL6,delimiter='\t',header='Radius\t\tDensity')
    #Escribo un archivo con los promedios de las densidades.
    #print("Archivo guardado con éxito")

    return densidadL6 , meanL6

def densidad_L4(matrizL4,frames_gro,intervalo,side_box):
    
    r=side_box/2
    rango_volumen=intervalo + 1
    delta=[i *(r/intervalo) for i in range(rango_volumen)]
    delta2=list(delta)
    delta2.pop(0)
    
    volumen=[(4/3)*math.pi * i**3 for i in delta]
        
    diferencias_volumen=np.diff(volumen)
    densidadL4=[]
    meanL4=[]

    rows,columns = matrizL4.shape
    num_groups= rows // frames_gro 
    
    for i in range(frames_gro):
        inicio = i * num_groups
        fin = (i + 1) * num_groups
        
        suma_filas = np.sum(matrizL4[inicio:fin,:], axis=0)
                
        densidad_grupo = np.divide(suma_filas, diferencias_volumen)
        
        densidadL4.append(np.column_stack((delta2, densidad_grupo)))

    meanL4=np.mean(densidadL4,axis=0)

    np.savetxt('densityL4_radialp.dat', meanL4,delimiter='\t',header='Radius\t\tDensity')
    
    return densidadL4 , meanL4

def densidad_L1(matrizL1,frames_gro,intervalo,side_box):

    r=side_box/2
    rango_volumen=intervalo + 1
    delta=[i *(r/intervalo) for i in range(rango_volumen)]
    delta2=list(delta)
    delta2.pop(0)
    
    volumen=[(4/3)*math.pi * i**3 for i in delta] 
    
    diferencias_volumen=np.diff(volumen)
    
    densidadL1=[]
    meanL1=[]

    rows,columns = matrizL1.shape
    num_groups= rows // frames_gro 
    
    for i in range(frames_gro):
        inicio = i * num_groups
        fin = (i + 1) * num_groups
        
        suma_filas = np.sum(matrizL1[inicio:fin, :], axis=0)
                        
        densidad_grupo = np.divide(suma_filas, diferencias_volumen)
                
        densidadL1.append(np.column_stack((delta2, densidad_grupo)))
                
    meanL1=np.mean(densidadL1,axis=0)
    
    np.savetxt('densityL1_radial.dat', meanL1,delimiter='\t',header='Radius\t\tDensity')
    
    return densidadL1 , meanL1, delta2

def sum_L14(meanL1,meanL4,delta2):
    #Suma los promedios de los segmentos L1 y L4 y escribe un texto con los nuevos resultados manteniendo el formato de los archivos anteriores. 

    meanL14 = np.column_stack((meanL1[:, 0], meanL1[:,1] + meanL4[:, 1]))
    #Suma la columna dos de todas las filas de la variable meanL1 y meanL4 y el resultado lo guarda en una nueva variable denominada meanL14 en dos columnas de nuevo, la primera con los datos de la columna uno de la matrizL1 y la segunda con la suma anterior. 

    np.savetxt('densityL14_radialp.dat',meanL14,delimiter='\t',header='Radius \t\tDensity')
    #Escribe un archivo con estos nuevos datos manteniendo el mismo formato a los anteriores. 
    
    return ()

#Llamar la funcióm

frames,side_box =reader_outgro('out.gro')
block = reader_frames(frames)
del(frames)
x_cm,x_new,y_cm,y_new,z_cm,z_new=centro_de_masa(block)
block=new_block(x_new,y_new,z_new,block)
del(x_cm,x_new,y_cm,y_new,z_cm,z_new)
coordinateL6, size_L6, frames_gro, coordinateL4, coordinateL1, size_L4, size_L1=discretizar(block)
del (block)
radio_promedio=radio_gel_por_frame(coordinateL6,coordinateL4,coordinateL1)
matrizL6=matriz_L6(coordinateL6, size_L6, frames_gro,200,side_box)
densidadL6 , meanL6= densidad_L6(matrizL6,frames_gro,200,side_box)
del(matrizL6,densidadL6,meanL6,coordinateL6,size_L6)
matrizL4=matriz_L4(coordinateL4, size_L4, frames_gro,200,side_box)
densidadL4 , meanL4= densidad_L4(matrizL4,frames_gro,200,side_box)
del(matrizL4,densidadL4,coordinateL4,size_L4)
matrizL1=matriz_L1(coordinateL1, size_L1, frames_gro,200,side_box)
densidadL1 , meanL1, delta2= densidad_L1(matrizL1,frames_gro,200,side_box)
del(matrizL1,densidadL1,coordinateL1, size_L1)
sum_L14(meanL4,meanL1,delta2)
del(meanL4,meanL1,delta2)


#llamar la función
'''
lmbd = ['0.1','0.2','0.3','0.4','0.5', '0.6','0.7','0.8','0.9','1.0']

for lbd in lmbd:
    os.chdir('surface-'+ lbd)
    #Estar segura con el nombre de las carpetas donde se hará la iteración.

    frames,side_box =reader_outgro('out.gro')
    block = reader_frames(frames)
    del(frames)
    x_cm,x_new,y_cm,y_new,z_cm,z_new=centro_de_masa(block)
    block=new_block(x_new,y_new,z_new,block)
    del(x_cm,x_new,y_cm,y_new,z_cm,z_new)
    coordinateL6, size_L6, frames_gro, coordinateL4, coordinateL1, size_L4, size_L1=discretizar(block)
    del (block)
    radio_promedio=radio_gel_por_frame(coordinateL6,coordinateL4,coordinateL1)
    matrizL6=matriz_L6(coordinateL6, size_L6, frames_gro,200,side_box)
    densidadL6 , meanL6= densidad_L6(matrizL6,frames_gro,200,side_box)
    del(matrizL6,densidadL6,meanL6,coordinateL6,sizeL6)
    matrizL4=matriz_L4(coordinateL4, size_L4, frames_gro,200,side_box)
    densidadL4 , meanL4= densidad_L4(matrizL4,frames_gro,200,side_box)
    del(matrizL4,densidadL4,coordinateL4,size_L4)
    matrizL1=matriz_L1(coordinateL1, size_L1, frames_gro,200,side_box)
    densidadL1 , meanL1, delta2= densidad_L1(matrizL1,frames_gro,200,side_box)
    del(matrizL1,densidadL1,coordinateL1, size_L1)
    sum_L14(meanL4,meanL1,delta2)
    del(meanL4,meanL1,delta2)

    os.chdir('..')
'''







