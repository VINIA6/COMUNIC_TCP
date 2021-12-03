import socket
import json
# Criação do socket
ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

# Conecta ao servidor
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)

print('\n')
print('-'*45)
print('Digite os limites de atuação dos sensores.\n')
limit_temp_max =  float(input('Limite Max Temperatura: '))
limit_temp_min =  float(input('Limite Min Temperatura: '))

limit_humidade_max =  float(input('Limite Max Humidade: '))
limit_humidade_min =  float(input('Limite Min Humidade: '))

limit_co2_max =  float(input('Limite Max Co2: '))
limit_co2_min =  float(input('Limite Min Co2: '))


# cliente = {
#     "id":4,
#     "temMax": limit_temp_max,
#     "temMin": limit_temp_min,
#     "humidadeMax": limit_humidade_max,
#     "humidadeMin": limit_humidade_min,
#     "co2Max": limit_co2_max,
#     "co2Min": limit_co2_min}


# cliente = json.dumps(cliente)
# cliente = str(cliente)
ClientSocket.send(str.encode('4' + ' ' + str(limit_temp_max)+ ' ' +
                                        str(limit_temp_min)+ ' ' + 
                                        str(limit_humidade_max)+ ' ' + 
                                        str(limit_humidade_min )+' ' + 
                                        str(limit_co2_max)+ ' ' + 
                                        str(limit_co2_min)))

while True: # Loop infinito para enviar mensagens do servidor
    print()
    print('Configurações da estufa:')
    print('0 - relatorio')
    print('1 - ligar/desligar Resfriador')
    print('2 - ligar/desligar Aquecedor')
    print('3 - ligar/desligar Irrigador')
    print('4 - ligar/desligar Injetor de Co2')
    Input = input('qual opçao: ')
    ClientSocket.send(str.encode('0' + ' ' + str(Input)))
    if str(Input) == '0': #Relatorio das estufa com as ultimas medidas
        response = ClientSocket.recv(2048)
        response = response.decode('utf-8').split(' ')
        print('Ultima temperatura: {:.2f} C'.format(float(response[0])))
        print('Ultima umidade do solo: {:.2f} %'.format(float(response[1])))
        print('Ultima taxa de Co2: {:.2f} ppm'.format(float(response[2])))
        print()
        print()
        print()
        
ClientSocket.close()