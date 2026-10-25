import socket
import protocol

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5398
BUFFER_SIZE = 1024

def print_commands():
    print('''
    Commands : 
        - <TEMP> to get current temperature reading
        - <HUM> to get current humidity reading
        - <BOTH> to get both of the current temperature and humidity reading
        - <EXIT> to close the connection
    ''')

def request_temp():
    pass
def request_hum():
    pass
def request_both():
    pass
def exit():
    pass

def start_client(client_name: str = 'Client'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

        # Construct init message using protocol
        message = protocol.init_connection(client_name)

        # Send encoded message
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent: {message}")

        # Receive server response (e.g., 'OK')
        response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Received: {response}")

        while True:
            print_commands()
            command = input("Enter command: ").strip().upper()

            match command:
                case 'TEMP':
                    message = protocol.request_temperature()
                    client_socket.sendall(message.encode('utf-8'))
                    print(f"Sent: {message}")
                case 'HUM':
                    message = protocol.request_humidity()
                    client_socket.sendall(message.encode('utf-8'))
                    print(f"Sent: {message}")
                case 'BOTH':
                    message = protocol.request_both()
                    client_socket.sendall(message.encode('utf-8'))
                    print(f"Sent: {message}")
                case 'EXIT':
                    client_socket.sendall(protocol.exit().encode('utf-8'))
                    break
                case _:
                    print(f"Invalid command '{command}'. Please choose from TEMP, HUM, BOTH, or EXIT.")
                    continue

            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not response:
                print("Server closed connection.")
                break
            print(f"Received: {response}")

    except ConnectionRefusedError:
        print(f"Connection refused: Is the server running on {SERVER_IP}:{SERVER_PORT}?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()               
        print("Socket closed.")

start_client()