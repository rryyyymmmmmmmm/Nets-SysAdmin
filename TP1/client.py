import socket
import protocol

from protocol import IP_ADDRESS, IP_PORT, ENCODING_FORMAT, BUFFER_SIZE, CLIENTS_NUMBER
SERVER_IP = IP_ADDRESS
SERVER_PORT = IP_PORT

def print_commands():
    print('''
    Commands : 
        - <TEMP> to get current temperature reading
        - <HUM> to get current humidity reading
        - <BOTH> to get both of the current temperature and humidity reading
        - <EXIT> to close the connection
        - <HELP> to show this message
    ''')


def start_client(client_name: str = 'Client'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # connect the client socket to the server
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

        # construct init message (to register the client with the server) using the pre-defined protocol init_connection method 
        message = protocol.init_connection(client_name)

        # send the encoded message
        client_socket.sendall(message.encode(ENCODING_FORMAT))
        print(f"Sent: {message}")

        # receive server's acknowledgement ('OK')
        response = client_socket.recv(BUFFER_SIZE).decode(ENCODING_FORMAT)
        print(f"Received: {response}")

        print_commands()

        while True:
            # normalize the input command
            command = input("Enter command: ").strip().upper()

            match command:
                case 'TEMP':
                    message = protocol.request_temperature()
                    client_socket.sendall(message.encode(ENCODING_FORMAT))
                    print(f"Sent: {message}")
                case 'HUM':
                    message = protocol.request_humidity()
                    client_socket.sendall(message.encode(ENCODING_FORMAT))
                    print(f"Sent: {message}")
                case 'BOTH':
                    message = protocol.request_both()
                    client_socket.sendall(message.encode(ENCODING_FORMAT))
                    print(f"Sent: {message}")
                case 'EXIT':
                    client_socket.sendall(protocol.exit().encode(ENCODING_FORMAT))
                    break
                case 'HELP':
                    print_commands()
                    break
                case _:
                    print(f"Invalid command '{command}'. Please choose from TEMP, HUM, BOTH, or EXIT.")
                    continue

            response = client_socket.recv(BUFFER_SIZE).decode(ENCODING_FORMAT)
            if not response:
                print("Server closed connection.")
                break
            print(f"Received: {response}")

    except ConnectionRefusedError:
        print(f"Connection refused: the server might not be running on {SERVER_IP}:{SERVER_PORT}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()               
        print("Socket closed.")

start_client()