# coding: utf-8
import socket
import sys
import binascii
import math
import re
import os
from Punto import Punto
import GUI
import time
import numpy as np
from sklearn.cluster import KMeans
from operator import itemgetter


    







class Operations:
    
    
    
    
    
   
    
    """Esta función se utiliza para tradurcir los datos recibidos del láser a números
        decimales según la forma de traducir descrita en la documentación del
        dispositivo"""
    def toDecimal(sensin):
        total=[]
        for elem in sensin:
            res=""
            for i in elem:
                t=int(i,16)
                if t > int('0x30',16) and t < int('0x39',16):
                    t = t - int('0x30',16)
                elif t > int('0x41',16) and t < int('0x46',16):
                    t = t - int('0x37',16)
                binario = bin(int(t))
                res = res + str(binario)
            total.append(str(int(res,2)))
        return total
    
    
    '''Función para traducir las coordenadas polares a cartesianas'''  
    def aCartesianos(p):
        coorX=p.getX()
        coorY=p.getY()
        
        coor1=math.fabs(coorX)*math.cos(math.radians(coorY))
        coor2=math.fabs(coorX)*math.sin(math.radians(coorY))
        
        puntoCart=Punto()
        puntoCart.setX(coor1)
        puntoCart.setY(coor2)
        return puntoCart
    
    """Se necesita crear esta función debido a errores presentes en la creación 
    de una lista de ángulos"""
    def creaangulos(x, y, jump):
        while x < y:
            yield x
            x += jump
            
    '''
    Funcion que calcula el tamaño de cada cluster en funcion del numero de puntos que comprende
    Se itera a traves de c sumando ocurrencias de un mismo cluster
    (Debe ser una lista en la que cada elemento representa un punto con valor igual al cluster al que pertenece)
    k representa el numero de clusters
    '''       
    def clusterSize(self,c,k):
        cluster_size = np.zeros(k)
        for point in c:
            cluster_size[point]+=1
        return cluster_size
                
    '''
    Funcion que devuelve la posicion de la variable punto dentro del contenedor container
    '''    
    def findIndex(self,punto,container):
        
        #Encuentra la primera ocurrencia del punto en el contenedor y devuelve su posicion
        j = 0

        ret = None
        for element in container:
            if(punto.getX() == element.getX() and punto.getY() == element.getY()):
                ret = j
                break
            else:
                j+=1
            ret = False
                
            
        return ret
    
    '''
    Funcion que calcula la distancia entre dos clusters en funcion de su distancia 
    y su angulo respecto del emisor laser
    Recibe una lista con angulos y otra lista con distancias, en las que cada 
    elemento i corresponde al mismo elemento i en la otra lista
    Solo para clusters de tamaño 3
    Devuelve una tupla compuesta por la distancia que separa el cluster 0 del 1 y el cluster 1 del 2
    '''
    def betweenClusterDistances(self,clusters):
        
        pi = 22/7
        angles = list()
        distances = list()
        for e in clusters:
            angles.append(e[0])
            distances.append(e[1]) 
            
        #Calcula las distancias entre los distintos centros geometricos de los clusters teoricos
        angle0to1 = (angles[1]-angles[0])*(pi/180)
        angle1to2 = (angles[2]-angles[1])*(pi/180)
        
        
        #Aplicando el teorema del coseno
        distance01 = math.sqrt(math.pow(distances[0],2)+math.pow(distances[1],2)-(2*distances[0]*distances[1]*math.cos(angle0to1)))
        distance02 = math.sqrt(math.pow(distances[1],2)+math.pow(distances[2],2)-(2*distances[1]*distances[2]*math.cos(angle1to2)))
        
        return list([distance01,distance02])
    
    '''
    Funcion que calcula la distancia media de todos los puntos de un cluster respecto del emisor (laser)
    Recibe una lista resultado del clustering kmeans y el vector de distancias de todos los puntos
    Devuelve un vector de tamaño k (3) con las distancias medias a cada cluster
    '''
    def realClusterDistances(self,model,distances):
        sum_distances = np.zeros((3,2))
        mean_distances = np.zeros(3)
        #en sum_distances se guarda una tupla por cada cluster que se compone de la suma de todas las 
        #distancias y el numero de elementos que componen el cluster
        
        
        for i in range(0,len(model.labels_)):
            
                
            sum_distances[model.labels_[i]][0]+=float(distances[i])
            sum_distances[model.labels_[i]][1]+=1
            
        for j in range(0,len(sum_distances)):
            mean_distances[j] = sum_distances[j][0]/sum_distances[j][1]
        return mean_distances
    
        '''
    Funcion que calcula el angulo medio de todos los puntos de un cluster respecto del emisor (laser)
    Recibe una lista resultado del clustering kmeans y el vector de angulos de todos los puntos
    Devuelve un vector de tamaño k (3) con los angulos medios a cada cluster
    '''
    #El primer bucle se usa para que las distancias de los clusters queden ordenadas según el cluster al que pertenecen 
    #numerando los clusters de izquierda a derecha
    def realClusterAngles(self,model,angulos):
        sum_angles = np.zeros((3,2))
        mean_angles = np.zeros(3)
        #Calcula la distancia media que separa a los puntos de cada cluster respecto del LIDAR
        #en sum_distances se guarda una tupla por cada cluster que se compone de la suma de todas las 
        #distancias y el numero de elementos que componen el cluster
        
        for i in range(0,len(model.labels_)):
               
            sum_angles[model.labels_[i]][0]+=float(angulos[i])
            sum_angles[model.labels_[i]][1]+=1
            
        for j in range(0,len(sum_angles)):
            mean_angles[j] = sum_angles[j][0]/sum_angles[j][1]
        
        return mean_angles
    
    '''
    Función que calcula si un punto está dentro del área de interes establecida
    '''
              
    def esValido(p):

        min_x = -1000
        max_x = 1000
        min_y = 950
        max_y = 2050
        
        return (max_x > p.getX() > min_x and max_y > p.getY() > min_y)
                            
    '''
    Funcion  encargada de procesar los datos recibidos desde el laser 
    (previo tratamiento en la funcion principal)
    En esta funcion se traducen los datos, se crean la nube de puntos (Cada punto se codifica como un objeto punto),
    y se realizan las comprobaciones para calcular si la trama corresponde a un palet
    Recibe una lista con los datos preprocesados de la lectura del laser(target) y
    un booleano representando si se trata de la primera ejecucion para en cuyo caso 
    lanzar la interfaz grafica (clase GUI)
    '''        
    def procesadoYMuestra(self,target,flag):
        
        
        #Se inicia un contador para calcular el framerate de procesao o tasa de FPS
        start=time.time()
        
        retorno = False
        
        """Separamos por el string de datos en partes de longitud 4 (longitud de cada dato).
        La longitud es calculada como 4324(número de caracteres de medición recibidos)/1081
        (número de mediciones realizadas por el láser) = 4(caracteres/medición) """
        datosSeparados=[ [target[i:i+4]] for i in range(0, int(len(target)), 4) ]
        """Eliminamos el último de los elementos ya que pertenece a información ajena a los 
        datos de medida"""
        datosSeparados.pop(-1)
        
        #Pasamos cada elemento del anteior array de hexadecimal a decimal
        distancias_puntos=Operations.toDecimal(datosSeparados)
        
        #Creamos la lista con ángulos
        angulos=list(Operations.creaangulos(-45,225,270/1081))
        
        #Creamos una lista de puntos con coordenadas polares
        listaPolares=list()
        for i in range(len(distancias_puntos)):
            #Si el valor de la distancia es mayor de 40000 representa un error de lectura del laser, por lo tanto lo descartamos
            if(int(distancias_puntos[i])<40000):
                p=Punto(int(distancias_puntos[i]),angulos[i])
                listaPolares.append(p)
        
        #Pasamos las coordenadas de cada punto de polares a cartesianas
        listaCartesianos=list()
        listaCX=list()
        listaCY=list()
        for pun in listaPolares:
            punto=Operations.aCartesianos(pun)
            listaCartesianos.append(punto)
        
        
        new_distances = list()
        new_angles = list()
        
        for p in listaCartesianos:
            
            if(Operations.esValido(p)):
                
                listaCX.append(p.getX())
                listaCY.append(p.getY())
                
                #Pasamos a guardar la distancia y el ángulo a ese punto
                i = self.findIndex(p,listaCartesianos)
                new_angles.append(angulos[i])
                new_distances.append(distancias_puntos[i])
                
                
                
        angulos = new_angles
        distancias_puntos = new_distances
                

            
        
        #Seleccionamos el área de interés
        
            
        coorXgrafico = np.array(listaCX)
        coorYgrafico = np.array(listaCY)
        

        #Creacion de archivo de logging para labores de depuracion 
        file = open("plotdata.txt","w")
        
        #Transformamos los puntos a un formato adecuado para el algoritmo K-Means
        points = list()
        for x,y in zip(coorXgrafico,coorYgrafico):
            points.append(list((x,y)))
            #Log de los datos de cada trama a fichero
            file.write(str(x)+","+str(y)+"\n")
            #separador para delimitar las tramas
            file.write("-----\n")
        file.close()
        
        GUI.MyGUI.printGraph(self,coorXgrafico,coorYgrafico)
        #if(flag):
            #gui_test = GUI(points)
            

            
        
        '''APARTADO DE CLUSTERING'''
        #Parametros del algoritmo
        clustering = KMeans(n_clusters = 3)
        #Aplicacion del algoritmo
        model = clustering.fit(points)
        
        
        '''
        Primera comprobacion en la que se mide que los tres cluster tengan un tamaño similar
        Si los tres clusters tienen aproximadamente el mismo tamaño continuamos con el proceso
        La tolerancia se expresa en el numero de puntos de diferencia entre un cluster y otro
        '''
        point_tolerance = 10
        cluster_size = self.clusterSize(model.labels_,3)
        dif1 = abs(cluster_size[0]-cluster_size[1])
        dif2 = abs(cluster_size[1]-cluster_size[2])
        dif3 = abs(cluster_size[0]-cluster_size[2])

        if((dif1 < point_tolerance) and (dif2 < point_tolerance) and (dif3 < point_tolerance)):
            
            #Juntamos los datos por pares de angulo y distancia, y los ordenamos por cluster de izquierda a derecha
            cluster_distances = self.realClusterDistances(model,distancias_puntos)
            cluster_angles = self.realClusterAngles(model,angulos)
            
            clusters = list()
            m_dist = 0
            m_ang = 0
            for ang,dist in zip(cluster_angles,cluster_distances):
                clusters.append([ang,dist])
                m_ang += float(ang)
                m_dist += float(dist)
            

            clusters.sort()
            
            
            

            '''
            Ahora con los datos de angulos y distancias de los centros calculamos
            la distancia real que separa los centros de los clusters puesto que la distancia que se aprecia 
            en los datos de medida podria distorsionarse en funcion de la distancia al palet
            '''
            
            leg_separation = self.betweenClusterDistances(clusters)

            #Separación de las patas de un palet. Ajustable a diferentes modelos de palet
            fixed_separation = 350
            #Tolerancia en la distancia de las patas del palet
            leg_tolerance = 20
            
            if(((abs(leg_separation[0] - fixed_separation)<leg_tolerance) and
                (abs(leg_separation[1] - fixed_separation)<leg_tolerance))):
                
                
                dist = m_dist/3
                ang = 90 - (m_ang/3)
                print("Palet detectado con exito a una distancia de ",dist, " y un ángulo de ", ang)
                retorno = True
            
        end = time.time()
        #Calculamos la tasa de FPS en funcion del tiempo transcurrido desde la llamada a la funcion            
        print("FPS:",(1/(end-start)))
        #Se añade un pequeño retardo para poder visualizar mejor los resultados
        time.sleep(1)
        return retorno
        
    
    
    
    def mainFunction(self):
        

        # Se crea el socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Se conecta y se comprueba que la conexión se realizó con exito
        conectado = os.system('ping -w 10 -n 2 192.168.0.10 >/dev/null 2>&1')
        if conectado == 0:
            server_address = ('192.168.0.10', 10940)
        else:
            server_address = ('127.0.0.1', 10500)
        
        print (sys.stderr, 'connecting to %s port %s' % server_address)
        try:
            sock.connect(server_address)
        except socket.timeout:
            print('Error de conexion')
        
        try:
            
            # Envio del mensaje (000EAR02 - Envio continuo de información de escaneo)
            message = [bytes([2]),chr(48),chr(48),chr(48),chr(69),chr(65),chr(82),chr(48),chr(50),binascii.unhexlify(b"00"),binascii.unhexlify(b"83"),bytes([3])]
            b = bytearray()
            b.extend(map(ord, message))
            print (sys.stderr, 'sending "%s"' % b)
            sock.send(b)
            

        
            # Se recoge la respuesta (En este caso la información de lectura del láser)
            sens=""
            amount_received = 0
            datosFinales=list()
            exit = False
            		
            
                
            num_sens=2
            amount_received = 0
            amount_expected = 4500*num_sens
            iteration = 0
            
            '''
            Bucle para procesar cada trama que envia el laser de forma continua
            Como implementacion futura usar una tecla del teclado para cambiar la 
            variable exit y salir del bucle cuando se pulse dicha tecla
            '''
            while not exit:
                iteration+=1
                
                sens=""
                
                #Bucle para procesar todos los datos de una trama puesto que 
                #no es posible recibirla de una sola vez
                
                while amount_received < amount_expected:
                    data = sock.recv(32)
                    sens+= data.decode('utf-8')
                    amount_received += len(data)
    
                amount_received = 0
    
            	# Se separa los datos del resto de información enviada por el laser
                datos_lectura=re.split('\x02|\x03',sens)
    
            	#Eliminamos las divisiones inecesarias (ya que se producen divisiones vacias)
                for e in datos_lectura:
                    if(len(e)<50):
                        datos_lectura.remove(e)
        
            	#Escogemos como dato el primero de los grupos de datos y 
                #retiramos los datos correspondientes a información innecesaria.
                target=datos_lectura[1][97:]
                
                #Diferenciamos entre la primera iteracion e iteraciones posteriores
                #por razones de actualización de los graficos de la GUI
                if(iteration == 1):
                    self.procesadoYMuestra(target,True)
                else:
                    self.procesadoYMuestra(target,False)
    
            return datosFinales
                        
                
        finally:
            #Cierre de recursos y envío de mensaje de parada al laser
            
            print (sys.stderr, 'closing socket')
            messagecierre = [bytes([2]),chr(48),chr(48),chr(48),chr(69),chr(65),chr(82),chr(48),chr(51),binascii.unhexlify(b"89"),binascii.unhexlify(b"92"),bytes([3])]
            bcierre = bytearray()
            bcierre.extend(map(ord, messagecierre))
            sock.send(bcierre)
            sock.close()





    

if __name__ == '__main__':

    obj = Operations()
    obj.mainFunction()