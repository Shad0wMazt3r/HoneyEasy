import socket
import paramiko
import threading
import os
from paramiko import RSAKey, ServerInterface, AUTH_SUCCESSFUL, AUTH_FAILED, OPEN_SUCCEEDED
import env_loader

ssh_directory = env_loader.load("SSH_DIRECTORY")


rsa_key_filename = env_loader.load("SSH_KEY")
if os.path.exists(rsa_key_filename):
    host_key = RSAKey(filename=rsa_key_filename)
else:
    host_key = RSAKey.generate(2048)
    host_key.write_private_key_file(rsa_key_filename)

motd = """
UNAUTHORIZED ACCESS TO THIS SYSTEM IS PROHIBITED.
\r\n
IF YOU ARE LOOKING FOR RANSOM, I CAN TELL YOU I DON'T HAVE MONEY. BUT WHAT I DO HAVE IS A VERY PARTICULAR SET OF SKILLS, SKILLS I HAVE ACQUIRED OVER A VERY LONG CAREER, SKILLS THAT MAKE ME A NIGHTMARE FOR PEOPLE LIKE YOU. IF YOU LET MY COMPUTER SYSTEM GO NOW, THAT'LL BE THE END OF IT. I WILL NOT LOOK FOR YOU, I WILL NOT PURSUE YOU. BUT IF YOU DON'T, I WILL LOOK FOR YOU, I WILL FIND YOU, AND I WILL KILL YOU.
\r\n"""

class FakeSSHServer(ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        log_entry = f"Username: {username}, Password: {password}\n"
        with open("ssh_honeypot.log", "a") as log_file:
            log_file.write(f"Login attempt - {log_entry}")
        
        if username == "root" and password == "toor":
            with open("ssh_honeypot.log", "a") as log_file:
                log_file.write("Successful login attempt\n")
            return AUTH_SUCCESSFUL
        else:
            with open("ssh_honeypot.log", "a") as log_file:
                log_file.write("Failed login attempt\n")
            return AUTH_FAILED

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
    channel.send("root> ")
    command_buffer = ""
    while True:
        try:
            data = channel.recv(1024)
            # print(data)
            if data == b'\x03':
                return
            data = data.decode("utf-8")
            # print(data)
            if not data:
                break
            
            for char in data:
                if char in ['\r', '\n']:
                    if command_buffer:
                        print(command_buffer.encode())
                        if command_buffer.lower() in ["exit", "quit", "q"]:
                            channel.send("\n\rExiting...\n\r")
                            return
                        elif command_buffer == "whoami":
                            channel.send("\n\rroot\n\r")
                            return
                        elif command_buffer == "id":
                            channel.send("\n\rruid=0(root) gid=0(root)\n\r")
                            return
                        elif command_buffer == "uname -a":
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
                    else:  # Empty command buffer
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
