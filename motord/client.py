import socket

class Client:
    
    def __init__(self, port=19853):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(("127.0.0.1", port))

    def close(self):
        self._socket.close()

    def home(self):
        self._socket.sendall(b"home")
        message = self._socket.recv(1024)

    def move_abs(self, position):
        self._socket.sendall(f"move_abs {position}".encode())
        message = self._socket.recv(1024)

    def move_rel(self, diff):
        self._socket.sendall(f"move_rel {diff}".encode())
        message = self._socket.recv(1024)

    def position(self):
        self._socket.sendall(b"position")
        message = self._socket.recv(1024)
        return int(message.decode())
