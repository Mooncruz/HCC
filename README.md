Perfiles de densidad en geles formado por varios segmento


A partir de redes copolim'ericas obtenidas por medio de simulaciones computacionales, se determina los perfiles de densidad de cada segmento por coronas dentro del sistema.

El script (discretizar_radial_lammps.py) entrega la densidad de segmentos en capas concéntricas del nanogel teniendo en cuenta su centro de masa del mismo. Este script está formado por varias funciones que a partir de un archivo de formato GRO que contiene la estructura del sistema, incluyendo tipos de elementos que forman el sistema y sus coordenadas espaciales en cada marco de la simulación.

Este script requiere de la siguiente información al momento de ejecutar las funciones:

Archivo file.gro en la función reader_outgro('file.gro')
número de coronas que será dividido el sistema (intervalo) en las funciones matriz_L(typ) y densidadL(typ).
También se incluye el script (density_profile.py) para graficar estos perfiles en sistemas funcionalizados según la distribución de la unidad funcional.

Debido a las restricciones de tamaño en GitHub, las carpetas necesarias para correr estos script están almacenados en Google Drive.  
[Descargar archivos aquí] (https://drive.google.com/drive/folders/15GbhjBRgu9hWeCfbLHgeRqTgo6t4aFb-?usp=drive_link)  