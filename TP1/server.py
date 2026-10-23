import socket

IP_ADDRESS = '127.0.0.1'
IP_PORT = 5398
BUFFER_SIZE = 1024

def init(ip_address: str = IP_ADDRESS, ip_port: int = IP_PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_address, ip_port))
    return server

def stop(server):
    server.close()

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
                case 'ERROR':
                    pass
    else:
        for p in parts:
            match p:
                case 'NAME':
                    return {'message_type': 'init', 'client_name': parts[1]}
                

#

def start():
    clients = []
    server = init(IP_ADDRESS, IP_PORT)
    server.listen()
    print(f'Started server at {IP_ADDRESS}:{IP_PORT}. Waiting for a connexion...')
    client_socket, client_address = server.accept()
    message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    parsed = parse(message)
    if parsed and parsed.get('message_type') == 'init':
        client_name = parsed['client_name']
        clients.append({'name': client_name, 'address': client_address, 'socket': client_socket})
        print(f'Added {client_name} from address {client_address}')
        client_socket.sendall('OK'.encode('utf-8'))
    client_socket.close()
    stop(server)


start()

    

