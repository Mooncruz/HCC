# Determinar la densidad de un gel formado por dos segmentos #
El primer script entrega la densidad de segmentos en capas concéntricas del nanogel teniendo en 
cuenta su centro de masa del mismo.A continuación se mencionan con una breve explicación las funciones 
presentes en los scripts discretizacion_radial.py y den-sep-L146.py

-def reader_outgro(filename): Lee desde un file.gro que contiene todas las configuraciones de la
simulación y guarda en una lista de lista cada una de ellas y en otra variable, la longitud de un
lado de la caja. Imprime en pantalla la cantidad de segmentos por configuración, la longitud de un
lado de la caja y el número de configuraciones presentes en el archivo input.

-def reader_frames(frames): De cada configuración se almacena en directorios la identidad de los
segmentos y esto queda guardado en una lista denominada block. Los directorios son: system, typ,
id, coorx, coory, coorz.

-def centro_de_masa(block): Determina el centro de masa de cada eje de cada configuración y obtiene
las nuevas coordenadas x,y,z a partir del centro de masa.

-def new_block(x new, y new, z new, block): Reemplaza las coordenadas de ’x’ , ’y’, ’z’ por las
nuevas ’x new’,’y new’,’z new’ en la variable block.

-def discretizar(block): En este código se extrae las coordenadas de ’x’,’y’,’z’ en tuplas de cada
configuración y se organizan en una lista de lista para cada tipo de segmento.

-def radio_gel_por_frame(coordinateL6,coordinateL4,coordinateL1): Aunque utilizamos la herramienta gmx 
gyrate de Gromacs, teniendo la información de las coordenadas de los segmentos en esta función se 
determina el radio del gel de cada configuración.

-def matriz_L6(coordinateL6, size L6, frames gro, num columns,side box): El gel se divide en varias
capas concéntricas (num columns) y se ubica cada segmentos de L6 en la capa que corresponda.
Esta información se guarda en una matriz que esta formado por filas que corresponde a cada
segmento de todos las configuraciones y las columnas corresponden a cada capa. Esta función se
repite para cada tipo de segmento.

-def densidad_L6(matrizL6,frames gro, intervalo,side box): Se toma la matriz correspondiente al tipo
de segmento y para cada configuración se suma la cantidad de segmentos presentes en cada capa y se
divide con el volumen de la capa. Al finalizar se calcula la densidad promedio de las configuraciones
y esta información se guarda en un archivo en dos columnas. La primera, el volumen de la capa y
la segunda la densidad promedio. Esta función se repite para cada tipo de segmento.

-def sum_L14(meanL1,meanL4,delta2): Se suma la densidad promedio de los segmentos L1 y L4 y
se genera un archivo con el mismo formato anterior.

-densepL146.py Script que genera un gráfico con 3 subgráficos donde se puede comparar el comportamiento 
de un gel a tres temperaturas diferentes, dos externas y una intermedia.
