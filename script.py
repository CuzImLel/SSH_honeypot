import socket, paramiko, threading

from paramiko.pkey import PKey

class SSH_server(paramiko.ServerInterface):
    def check_auth_password(self, username: str, password: str):
        print(f"{username}:{password}")
        return paramiko.AUTH_FAILED
    
    def check_auth_publickey(self, username: str, key: PKey):
        return paramiko.AUTH_FAILED
    
def handle_connection(clientsocket, serverkey):
    transport = paramiko.Transport(clientsocket)
    transport.add_server_key(serverkey)
    ssh = SSH_server()
    transport.start_server(server=ssh)



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 22))
    server_socket.listen(100)
    serverkey = paramiko.RSAKey.generate(2048)
    while True:
        clientsocket, clientaddress = server_socket.accept()
        print(f"Connection: {clientaddress[0]}:{clientaddress[1]}")
        t = threading.Thread(target= handle_connection, args=(clientsocket,serverkey))
        t.start()



if __name__ == "__main__":
    main()