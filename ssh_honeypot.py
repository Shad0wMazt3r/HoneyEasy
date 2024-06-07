import socket
import paramiko
import threading
import sys
from paramiko import RSAKey, ServerInterface, AUTH_FAILED, OPEN_SUCCEEDED


host_key = RSAKey.generate(2048)

class FakeSSHServer(ServerInterface):
    def check_auth_password(self, username, password):
        with open("ssh_honeypot.log", "a") as log_file:
            log_file.write(f"Username: {username}, Password: {password}\n")
        return AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return OPEN_SUCCEEDED
        return AUTH_FAILED

def handle_connection(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)
    
    server = FakeSSHServer()
    try:
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel is not None:
            channel.send("Welcome to the fake SSH server!\n")
            channel.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        transport.close()

def start_server(host='0.0.0.0', port=22):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(100)
    
    print(f"[*] Listening on {host}:{port}")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr}")
        
        client_handler = threading.Thread(target=handle_connection, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
