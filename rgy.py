rgy=[]
rgy2=[]

 
with open('gyrate.xvg','r') as gy:
   for linea in gy:
       if not linea.startswith('#') and not linea.startswith('@'):
          rgy.append(float(linea.split()[1]))
               
for j,i in enumerate(rgy):
   if j >= 75: #tengo en cuenta que desde el paso 750 se normaliza el radio de giro por ende pongo este valor en el ìndice que equivale a la lìnea 103 de este paso menos las 28 lìneas que se eliminan en las lìneas del script anteriores.  
      rgy2.append(i)
   if j >= 200: #Este es el ùltimmo indice que equivale a la ùltima lìnea 
      break
    
promedio=sum(rgy)/len(rgy)
promedio2=sum(rgy2)/len(rgy2)
print(len(rgy))
print(promedio)
print(" ")
print(len(rgy2))
print(promedio2)





