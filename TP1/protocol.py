from enum import Enum

IP_ADDRESS = '127.0.0.1'
IP_PORT = 5398
BUFFER_SIZE = 1024
CLIENTS_NUMBER = 3
ENCODING_FORMAT = 'ascii'

class ClientType(Enum):
    SERVER = "server"
    CLIENT = "client"
    SENSOR = "sensor"

def info():
        print('''
        Protocol SENSv1, developed for the Systems and Networks Administration Lab N°1.
        It sends data in ASCII format, with linebreaks as terminators. 
        
        - The connection is initiated by sending a INIT-[<client_name>,<client_type>] command.
        - The server responds with an OK message when the socket is successfully created.
        ''')
    
def init_connection(client_name: str):
    return f'NAME:{client_name}'
    
def ack():
    return 'OK'

def exit():
    return 'EXIT'

def error():
    return 'ERROR'
    
def request_humidity():
    return 'HUM'    
    
def send_humidity(hum: float):
    return f'HUM:{hum}'
      
def request_temperature():
    return 'TEMP'
    
def send_temperature(temp: float):
    return f'TEMP:{temp}'

def request_both():
    return 'BOTH'

def send_both(hum: float, temp: float):
    return f'{send_humidity(hum)}, {send_temperature(temp)}'
    
