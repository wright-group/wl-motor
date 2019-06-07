import socket
import json

BUFFSIZE = 4096


class Client:
    def __init__(self, port=19853):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(("127.0.0.1", port))

    def close(self):
        self._socket.sendall(json.dumps({"command": "close"}).encode())
        message = self._socket.recv(BUFFSIZE)
        print(message)
        self._socket.close()

    def home(self):
        self._socket.sendall(json.dumps({"command": "home"}).encode())
        message = self._socket.recv(BUFFSIZE)
        print(message)

    def set_position(self, position):
        self._socket.sendall(
            json.dumps({"command": "set_position", "args": [position]}).encode()
        )
        message = self._socket.recv(BUFFSIZE)

    def get_position(self):
        self._socket.sendall(json.dumps({"command": "get_position"}).encode())
        message = self._socket.recv(BUFFSIZE)
        return json.loads(message)["result"]

    def get_destination(self):
        self._socket.sendall(json.dumps({"command": "get_destination"}).encode())
        message = self._socket.recv(BUFFSIZE)
        return json.loads(message)["result"]

    def busy(self):
        self._socket.sendall(json.dumps({"command": "busy"}).encode())
        message = self._socket.recv(BUFFSIZE)
        return json.loads(message)["result"]

    def help(self, command=None):
        self._socket.sendall(
            json.dumps({"command": "help", "args": [command]}).encode()
        )
        message = self._socket.recv(BUFFSIZE)
        print(json.loads(message)["result"])

    def list_commands(self):
        self._socket.sendall(json.dumps({"command": "list_commands"}).encode())
        message = self._socket.recv(BUFFSIZE)
        return json.loads(message)["result"]
