import socket

IP_ADDRESS = '127.0.0.1'
IP_PORT = 5398

def init(ip_address: str = IP_ADDRESS, ip_port: int = IP_PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, ip_port))

def start(self):
    init()
    self.server.listen()
    client, client_address = self.server.accept()

def stop(self):
    self.server.close()

def register_client():


################
    
def send_humidity():
    pass

def request_humidity():
    pass

def parse(message: str):
    parts = message.split(':')

    # checking if the message contains only one command

    if(len(parts)==1):
        for p in parts:
            match p:
                case 'OK':
                    pass
                case 'HUM':
                    pass
                case 'TEMP':
                    pass
                case 'BOTH':
                    pass
    else:

    
    

