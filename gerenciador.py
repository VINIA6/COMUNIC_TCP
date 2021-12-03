import socket
from _thread import *

# Criação do socket TCP (SOCK_STREAM)
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1233
ThreadCount = 0 # Numero de Threads
listAddrs = [] # Lista de endereços de clientes

# valores das medições
lastTemp = 0
lastUmi = 0
lastCo2 = 0

# Bind do socket
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(10)


# Criação de theads principal para cada conexão
def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        
        if not data:
            connection.close()
            break
        reply = data.decode().split(' ')
        if reply[0] == '4':
            temMax=reply[1]
            temMin=reply[2]
            humidadeMax=reply[3]
            humidadeMin=reply[4]
            co2Max=reply[5]
            co2Min=reply[6]
            
        elif reply[0] == '1': # Temperatura
            maxMin(reply[1], reply[0])
            global lastTemp 
            lastTemp = reply[1]
            print('Temperatura: {:.2f} C'.format(float(reply[1])))
            connection.send(str.encode(reply[1]))
        elif reply[0] == '2': # Umidade
            maxMin(reply[1], reply[0])
            global lastUmi
            lastUmi = reply[1]
            print('Umidade do Solo: {:.2f}%'.format(float(reply[1])))
            connection.send(str.encode(reply[1]))
        elif reply[0] == '3': # CO2
            maxMin(reply[1], reply[0])
            global lastCo2
            lastCo2 = reply[1]
            print('Co2: {:.2f} ppm'.format(float(reply[1])))
            connection.send(str.encode(reply[1]))
        elif reply[0] == '0': # Comandos vindo do cliente
            if reply[1] == '0':
                resp = str(lastTemp) + ' ' + str(lastUmi) + ' ' + str(lastCo2)
                connection.send(str.encode(resp))
            send_command(str(reply[1]))


        
        
            

def command(connection, atuador): # Envia comandos para os clientes
    connection.sendall(str.encode(atuador))
    
def send_command(atuador): # Envia comandos para os clientes
    for i in listAddrs:
        start_new_thread(command, (i, atuador))


def maxMin(value, sensor, ): # Verifica se o valor está dentro do limite
    if sensor == '1':
        if int(value) > 80:
            send_command('1')
        elif int(value )< 20:
            send_command('2')
    elif sensor == '2':
        if int(value) > 80 or int(value )< 20:
            send_command('3')
    elif sensor == '3':
        if int(value) > 80 or int(value) < 20:
            send_command('4')

#recebendo valores maximos e mínimos.
while True: # Loop principal
    Client, address = ServerSocket.accept()
    listAddrs.append(Client)
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client,))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()