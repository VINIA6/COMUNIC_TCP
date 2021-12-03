from threading import Thread
import time
import socket
from _thread import *

class Sensor: # classe usada de base para os sensores
    def __init__(self, id, valor):
        self.id = id
        self.valor = valor
        self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 1233

    def getValor(self):
        return self.valor

    def getId(self):
        return self.id

    def atuador(self, atuadorId):
        if atuadorId == 1:
            self.valor = self.valor - 1.0
        else:
            self.valor = self.valor + 1.0


    def downValor(self):
        self.valor = self.valor - 0.10


    def getClientSocket(self):
        return self.ClientSocket
    
    def connect(self):
        print("Conectando sensor " + str(self.id))
        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e)+'\n\n')
#final da classe sensor

        


class Atuador: #class usada de base para os atuadores
    def __init__(self, id, sensor):
        self.id = id
        self.estado = False
        self.sensor = sensor
        self.ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'
        self.port = 1233

    def getId(self):
        return self.id

    def getEstado(self):
        return self.estado
        
    def getClientSocket(self):
        return self.ClientSocket
    
    def getSensor(self):
        return self.sensor

    def connect(self):
        print("Conectando Atuador " + str(self.id))
        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e)+'\n\n')
#final da classe atuador



class threadSensor(Thread): #thread usada para ler os sensores
    def __init__(self, sensor):
        Thread.__init__(self)
        self.sensor = sensor
        self.ClientSocket = sensor.getClientSocket()
        self.intervalo = 1
        self.estado = True
        self.start()

    def run(self):
        self.sensor.connect()
        while self.estado:
            Response = self.ClientSocket.recv(1024)
            if self.sensor.getId() == 2:
                self.sensor.downValor()    
            if self.sensor.getId() == 3:
                self.sensor.downValor()   
            self.ClientSocket.send(str.encode(str(self.sensor.getId()) + ' '+ str(self.sensor.getValor())))
            time.sleep(self.intervalo)

    def stop(self):
        self.estado = False
#final da classe threadSensor



class threadAtuador(Thread): #thread usada para ler os atuadores
    def __init__(self, atuador):
        Thread.__init__(self)
        self.atuador = atuador
        self.sensor = atuador.getSensor()
        self.ClientSocket = atuador.getClientSocket()
        self.intervalo = 1
        self.estado = True
        self.estadoAtuador = False
        self.start()

    def atuadorAtivado(self, atuadorId):
        if self.estadoAtuador:
            time.sleep(self.intervalo)
            self.sensor.atuador(atuadorId)
            self.atuadorAtivado(atuadorId)
        return
        

    def run(self):
        self.atuador.connect()
        while self.estado:
            response = self.ClientSocket.recv(1024)
            if response.decode() == str(self.atuador.getId()):
                if self.estadoAtuador:
                    self.estadoAtuador = False
                else:
                    self.estadoAtuador = True
            if self.estadoAtuador:
                start_new_thread(self.atuadorAtivado, (self.atuador.getId(),))
            time.sleep(self.intervalo)

    def stop(self):
        self.estado = False
#final da classe threadAtuador



if __name__ == "__main__": #criando os sensores
    sensorTemp = Sensor(1, 38.1)
    sensorUmidadeSolo = Sensor(2, 50.0)
    sensorCo2 = Sensor(3, 30.1)
    #------------------------------------------------------

    #criando os atuadores
    resfriador = Atuador(1, sensorTemp)
    aquecedor = Atuador(2, sensorTemp)
    irrigador = Atuador(3, sensorUmidadeSolo)
    injetorCo2 = Atuador(4, sensorCo2)
    #------------------------------------------------------

    #criando as threads dos sensores
    threadSensorTemp = threadSensor(sensorTemp)
    threadSensorUmidadeSolo = threadSensor(sensorUmidadeSolo)
    threadSensorCo2 = threadSensor(sensorCo2)
    #------------------------------------------------------

    #criando as threads dos atuadores
    threadAtuadorResfriador = threadAtuador(resfriador)
    threadAtuadorAquecedor = threadAtuador(aquecedor)
    threadAtuadorIrrigador = threadAtuador(irrigador)
    threadAtuadorInjetorCo2 = threadAtuador(injetorCo2)
    #------------------------------------------------------







        


