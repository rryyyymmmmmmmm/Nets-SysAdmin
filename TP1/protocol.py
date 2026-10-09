from enum import Enum

class ClientType(Enum):
    SERVER = "server"
    CLIENT = "client"
    SENSOR = "sensor"

class SENSv1:
    def __init__(self):
        pass

    @staticmethod
    def info():
        print('''
        Protocol SENSv1, developed for the Systems and Networks Administration Lab N°1.
        It sends data in ASCII format, with linebreaks as terminators. 
        
        - The connection is initiated by sending a INIT-[<client_name>,<client_type>] command.
        - The server responds with an OK message when the socket is successfully created.
        ''')
    
    @staticmethod
    def init_connection(client_name: str, client_type: ClientType):
        pass
    
    @staticmethod
    def ack():
        pass

    @staticmethod
    def request_humidity():
        pass
    
    @staticmethod
    def send_humidity():
        pass
    
    @staticmethod
    def request_temperature():
        pass
    
    @staticmethod
    def send_temperature():
        pass
    
