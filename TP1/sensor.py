import socket
import protocol
import sys
import random
import time

from protocol import IP_ADDRESS, IP_PORT, ENCODING_FORMAT, BUFFER_SIZE, CLIENTS_NUMBER

def sense_humidity():
    return random.randrange(0, 100)

def sense_temperature():
    return random.randrange(-40, 80)

def start_client(sensor_type: str, client_name: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((IP_ADDRESS, IP_PORT))
        print(f"Connected to server at {IP_ADDRESS}:{IP_PORT}")

        message = protocol.init_connection(client_name)
        client_socket.sendall(message.encode(ENCODING_FORMAT))
        print(f"Sent: {message}")

        response = client_socket.recv(BUFFER_SIZE).decode(ENCODING_FORMAT)
        print(f"Received: {response}")

        while True:
            time.sleep(2)
            if sensor_type == 'hum':
                reading = sense_humidity()
                message = protocol.send_humidity(reading)
            else:
                reading = sense_temperature()
                message = protocol.send_temperature(reading)

            client_socket.sendall(message.encode(ENCODING_FORMAT))
            print(f"Sent: {message}")

            response = client_socket.recv(BUFFER_SIZE).decode(ENCODING_FORMAT)
            if not response:
                print("Server closed connection.")
                break
            print(f"Received: {response}")

    except KeyboardInterrupt:
        print("\nStopping sensor...")
        try:
            client_socket.sendall(protocol.exit().encode(ENCODING_FORMAT))
        except Exception:
            pass
    except ConnectionRefusedError:
        print(f"Connection refused: Is the server running on {IP_ADDRESS}:{IP_PORT}?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()               
        print("Socket closed.")

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ('hum', 'temp'):
        print("Usage: python sensor.py <hum|temp>")
        sys.exit(1)

    sensor_type = sys.argv[1].lower()
    print(f"Starting {sensor_type.upper()} sensor...")
    start_client(sensor_type=sensor_type, client_name=f"{sensor_type.upper()}_sensor")