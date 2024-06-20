import socket
import paramiko
import threading
import os
from paramiko import RSAKey, ServerInterface, AUTH_SUCCESSFUL, AUTH_FAILED, OPEN_SUCCEEDED
import datetime
import env_loader
import logger


ssh_directory = env_loader.load("SSH_DIRECTORY")
motd = env_loader.banner_load("SSH")
motd = motd.replace("\n", "\r\n")

log_file = env_loader.load("SSH_LOG")

rsa_key_filename = env_loader.load("SSH_KEY")

if os.path.exists(rsa_key_filename):
    host_key = RSAKey(filename=rsa_key_filename)
else:
    host_key = RSAKey.generate(2048)
    host_key.write_private_key_file(rsa_key_filename)

# logged_in_username = ""

def read_creds():
    file_name = env_loader.load("SSH_CREDS")
    with open(file_name, "r") as f:
        for line in f:
            username, password = line.strip().split(":")
            yield username, password

class FakeSSHServer(ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        log_entry = f"Username: {username}, Password: {password}\n"
        logger.log(f"Login attempt - {log_entry}{datetime.datetime.now()}\n", log_file)
        
        creds = read_creds()

        for uname, passwd in creds:
            if username == uname and password == passwd:
                logger.log(f"Login successful - {log_entry}{datetime.datetime.now()}\n", log_file)
                logged_in_username = username
                return AUTH_SUCCESSFUL
        logger.log(f"Login failed - {log_entry}{datetime.datetime.now()}\n", log_file)


    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return OPEN_SUCCEEDED
        return AUTH_FAILED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

def handle_connection(client_socket):
    transport = paramiko.Transport(client_socket)
    transport.add_server_key(host_key)
    
    server = FakeSSHServer()
    try:
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel is not None:
            server.event.wait(10)
            if not server.event.is_set():
                channel.close()
                return
            channel.send(motd)
            fake_shell(channel)
            channel.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        transport.close()

def fake_shell(channel):
    prompt = logged_in_username + ">"
    channel.send(prompt)
    command_buffer = ""
    while True:
        try:
            data = channel.recv(1024)
            if data == b'\x03':
                return
            data = data.decode("utf-8")
            if not data:
                break
            for char in data:
                if char in ['\r', '\n']:
                    if command_buffer:
                        print(command_buffer.encode())
                        if command_buffer in ["exit", "quit", "q"]:
                            channel.send("\n\rExiting...\n\r")
                            return
                        elif command_buffer == "whoami":
                            channel.send("\n\rroot\n\r")
                            return
                        elif command_buffer == "id":
                            channel.send("\n\rruid=0(root) gid=0(root)\n\r")
                            return
                        elif command_buffer == "uname -a":
                            # server_uname_a = "Linux lite-server 5.4.0-109-generic #123-Ubuntu SMP" + ADD DATE TIME HERE +"x86_64 x86_64 x86_64 GNU/Linux\n\r"
                            channel.send("\n\rLinux lite-server 5.4.0-109-generic #123-Ubuntu SMP Thu Oct 22 22:39:06 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux\n\r")
                            return
                        elif command_buffer == "id -u":
                            channel.send("\n\r0\n\r")
                            return
                        elif command_buffer == "id -g":
                            channel.send("\n\r0\n\r")
                            return
                        elif command_buffer == "pwd":
                            channel.send("\n\r/\n\r")
                            return
                        channel.send(f"\n\r{command_buffer}: command not found\n\r")
                        with open("ssh_honeypot.log", "a") as log_file:
                            log_file.write(f"Command executed: {command_buffer}\n")

                        command_buffer = ""
                        channel.send("root> ")
                    else:
                        channel.send("\n\rroot> ")
                else:
                    command_buffer += char
                    channel.send(char)
        except Exception as e:
            break

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
