import socket
import json

BUFFSIZE = 4096

class Client:
    
    def __init__(self, port=19853):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(("127.0.0.1", port))

    def close(self):
        self._socket.close()

    def home(self):
        self._socket.sendall(json.dumps({"command":"home"}).encode())
        message = self._socket.recv(BUFFSIZE)
        print(message)

    def move_abs(self, position):
        self._socket.sendall(json.dumps({"command":"move_abs", "value":position}).encode())
        message = self._socket.recv(BUFFSIZE)
        print(message)

    def move_rel(self, diff):
        self._socket.sendall(json.dumps({"command":"move_rel", "value":diff}).encode())
        message = self._socket.recv(BUFFSIZE)
        print(message)

    def position(self):
        self._socket.sendall(json.dumps({"command":"position"}).encode())
        message = self._socket.recv(BUFFSIZE)
        print(message)
        return json.loads(message)["result"]

    def is_busy(self):
        self._socket.sendall(json.dumps({"command":"is_busy"}).encode())
        message = self._socket.recv(BUFFSIZE)
        print(message)
        return json.loads(message)["result"]
