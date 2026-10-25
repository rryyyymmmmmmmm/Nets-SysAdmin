import socket
import threading
import protocol

IP_ADDRESS = '127.0.0.1'
IP_PORT = 5398
BUFFER_SIZE = 1024
CLIENTS_NUMBER = 3

def init(ip_address: str = IP_ADDRESS, ip_port: int = IP_PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip_address, ip_port))
    return server

def stop(server):
    server.close()

latest_readings = {
    'temp': 0.0,
    'hum': 0.0
}
    
def send_humidity():
    return latest_readings['hum']

def send_temperature():
    return latest_readings['temp']

def request_humidity():
    pass

def request_temperature():
    pass

def parse(message: str):
    if not message:
        return None
    parts = message.strip().split(':')
    if len(parts) == 1:
        match parts[0]:
            case 'OK':
                return {'message_type': 'ok'}
            case 'HUM':
                return {'message_type': 'hum'}
            case 'TEMP':
                return {'message_type': 'temp'}
            case 'BOTH':
                return {'message_type': 'both'}
            case 'EXIT':
                return {'message_type': 'exit'}
            case 'ERROR':
                return {'message_type': 'error'}
    elif len(parts) >= 2:
        match parts[0]:
            case 'NAME':
                return {'message_type': 'init', 'client_name': parts[1]}
            case 'TEMP':
                return {'message_type': 'sensor_temp', 'value': float(parts[1])}
            case 'HUM':
                return {'message_type': 'sensor_hum', 'value': float(parts[1])}
    return {'message_type': 'unknown'}

def handle_client(client_socket, client_address):
    client_name = "Unknown"
    try:
        while True:
            raw_data = client_socket.recv(BUFFER_SIZE)
            if not raw_data:
                break
            message = raw_data.decode('utf-8').strip()
            parsed = parse(message)
            if not parsed:
                continue

            message_type = parsed.get('message_type')
            match message_type:
                case 'init':
                    client_name = parsed['client_name']
                    print(f"[+] Added {client_name} from {client_address}")
                    client_socket.sendall(protocol.ack().encode('utf-8'))

                case 'sensor_temp':
                    latest_readings['temp'] = parsed['value']
                    print(f"[{client_name}] Updated TEMP: {latest_readings['temp']}")
                    client_socket.sendall(protocol.ack().encode('utf-8'))

                case 'sensor_hum':
                    latest_readings['hum'] = parsed['value']
                    print(f"[{client_name}] Updated HUM: {latest_readings['hum']}")
                    client_socket.sendall(protocol.ack().encode('utf-8'))

                case 'temp':
                    msg = protocol.send_temperature(latest_readings['temp'])
                    client_socket.sendall(msg.encode('utf-8'))

                case 'hum':
                    msg = protocol.send_humidity(latest_readings['hum'])
                    client_socket.sendall(msg.encode('utf-8'))

                case 'both':
                    msg = protocol.send_both(latest_readings['hum'], latest_readings['temp'])
                    client_socket.sendall(msg.encode('utf-8'))

                case 'exit':
                    print(f"[-] {client_name} requested disconnect.")
                    break
    except Exception as e:
        print(f"Error handling {client_name}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_name} ({client_address}) closed.")
          
def start():
    server = init(IP_ADDRESS, IP_PORT)
    server.listen(CLIENTS_NUMBER)
    print(f'Started server at {IP_ADDRESS}:{IP_PORT}. Waiting for a connexion...')

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        stop(server)
        
start()

    

