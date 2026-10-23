import socket

try:
    import protocol
except ImportError:
    from TP1 import protocol

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5398
BUFFER_SIZE = 1024


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

    except ConnectionRefusedError:
        print(f"Connection refused: Is the server running on {SERVER_IP}:{SERVER_PORT}?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Socket closed.")

start_client()