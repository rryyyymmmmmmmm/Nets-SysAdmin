import socket
import threading
import protocol
from protocol import IP_ADDRESS, IP_PORT, ENCODING_FORMAT, BUFFER_SIZE, CLIENTS_NUMBER, ClientType

# configuration variables for the server

# init function to quickly creata a server 
def init(ip_address: str = IP_ADDRESS, ip_port: int = IP_PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip_address, ip_port))
    return server

# simple function to stop the server
def stop(server):
    server.close()

# storing the humidity and temperature readings globally 
latest_readings = {
    'temp': 0.0,
    'hum': 0.0
}

# tracks which sensor types are currently connected and running
running_sensors = set()  # e.g. {'temp'}, {'hum'}, {'temp', 'hum'}

# functions to send the latest humidity readings to the client
def get_reading(reading_type: str):
    if reading_type not in latest_readings:
        raise ValueError(f"Unknown reading type: {reading_type}")
    return latest_readings[reading_type]

def get_temperature():
    return latest_readings['temp']

# function to parse the incoming messages from both the clients and the sensors
def parse(message: str):
    # make sure the message isnt empty to not break the server
    if not message:
        return None
    # split the message with ':'
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
                return {
                    'message_type': 'init',
                    'client_name': parts[1],
                    'client_type': parts[2].lower() if len(parts) >= 3 else ClientType.CLIENT.value,
                }
            case 'TEMP':
                return {'message_type': 'sensor_temp', 'value': float(parts[1])}
            case 'HUM':
                return {'message_type': 'sensor_hum', 'value': float(parts[1])}
    return {'message_type': 'unknown'}

# sensor_type_map maps the message_type a sensor sends to the reading key it owns
SENSOR_MESSAGE_TO_KEY = {
    'sensor_temp': 'temp',
    'sensor_hum':  'hum',
}

# defining a function for handling both the client and the sensors (it will be used to define a thread further down in the coe)
def handle_client(client_socket, client_address, client_type : ClientType):
    client_name = str(client_address)
    # the reading key owned by this connection if it turns out to be a sensor
    sensor_key = None
    try:
        while True:
            # receive raw data from any client
            raw_data = client_socket.recv(BUFFER_SIZE)
            # if the data received is empty break from the loop to not break the function
            if not raw_data:
                break
            # decode the message
            message = raw_data.decode(ENCODING_FORMAT).strip()
            parsed = parse(message)
            if not parsed:
                continue

            message_type = parsed.get('message_type')

            match message_type:
                case 'init':
                    client_name = parsed['client_name']
                    registered_type = parsed['client_type']
                    if registered_type == ClientType.SENSOR.value:
                        client_type = ClientType.SENSOR
                    elif registered_type == ClientType.CLIENT.value:
                        client_type = ClientType.CLIENT
                    else:
                        client_socket.sendall(protocol.error().encode(ENCODING_FORMAT))
                        break
                    print(f"[+] Added {client_name} from {client_address}")
                    client_socket.sendall(protocol.ack().encode(ENCODING_FORMAT))

                case 'sensor_temp' if client_type == ClientType.SENSOR:
                    # mark temperature sensor as running on first reading
                    if sensor_key is None:
                        sensor_key = 'temp'
                        running_sensors.add(sensor_key)
                        print(f"[+] Sensor '{sensor_key}' is now running.")
                    latest_readings['temp'] = parsed['value']
                    print(f"[{client_name}] Updated TEMP: {latest_readings['temp']}")
                    client_socket.sendall(protocol.ack().encode(ENCODING_FORMAT))

                case 'sensor_hum' if client_type == ClientType.SENSOR:
                    # mark humidity sensor as running on first reading
                    if sensor_key is None:
                        sensor_key = 'hum'
                        running_sensors.add(sensor_key)
                        print(f"[+] Sensor '{sensor_key}' is now running.")
                    latest_readings['hum'] = parsed['value']
                    print(f"[{client_name}] Updated HUM: {latest_readings['hum']}")
                    client_socket.sendall(protocol.ack().encode(ENCODING_FORMAT))

                case 'temp' if client_type == ClientType.CLIENT:
                    if 'temp' not in running_sensors:
                        print(f"[!] {client_name} requested TEMP but temperature sensor is not running.")
                        client_socket.sendall(protocol.error().encode(ENCODING_FORMAT))
                    else:
                        msg = protocol.send_temperature(get_reading('temp'))
                        client_socket.sendall(msg.encode(ENCODING_FORMAT))

                case 'hum' if client_type == ClientType.CLIENT:
                    if 'hum' not in running_sensors:
                        print(f"[!] {client_name} requested HUM but humidity sensor is not running.")
                        client_socket.sendall(protocol.error().encode(ENCODING_FORMAT))
                    else:
                        msg = protocol.send_humidity(get_reading('hum'))
                        client_socket.sendall(msg.encode(ENCODING_FORMAT))

                case 'both' if client_type == ClientType.CLIENT:
                    missing = [k for k in ('temp', 'hum') if k not in running_sensors]
                    if missing:
                        print(f"[!] {client_name} requested BOTH but sensors not running: {missing}")
                        client_socket.sendall(protocol.error().encode(ENCODING_FORMAT))
                    else:
                        msg = protocol.send_both(latest_readings['hum'], latest_readings['temp'])
                        client_socket.sendall(msg.encode(ENCODING_FORMAT))

                case 'exit' if client_type == ClientType.CLIENT:
                    print(f"[-] {client_name} requested disconnect.")
                    break

                case _:
                    print(f"[!] Unauthorized command '{message_type}' from {client_type.name} {client_name}")
    except Exception as e:
        print(f"Error handling {client_name}: {e}")
    finally:
        # if this connection was a sensor, unregister it so clients get errors again
        if sensor_key is not None:
            running_sensors.discard(sensor_key)
            print(f"[-] Sensor '{sensor_key}' is no longer running.")
        client_socket.close()
        print(f"Connection with {client_name} ({client_address}) closed.")
          
def start():
    server = init(IP_ADDRESS, IP_PORT)
    server.listen(CLIENTS_NUMBER)
    print(f'Started server at {IP_ADDRESS}:{IP_PORT}. Waiting for a connexion...')

    try:
        while True:
            client_socket, client_address = server.accept()
            client_type = ClientType.CLIENT
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_type), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        stop(server)
        
start()

    
