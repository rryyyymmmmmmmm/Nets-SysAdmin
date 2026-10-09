import socket

class SENSV1_server:

    def __init__(self, ip_address: str, ip_port: int):
        self.ip_address = ip_address  # store the parameter as an attribute
        self.ip_port = ip_port        # store the parameter as an attribute
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip_address, self.ip_port))

    def start(self):
        self.server.listen()
        client, client_address = self.server.accept()

    def stop(self):
        self.server.close()


    
