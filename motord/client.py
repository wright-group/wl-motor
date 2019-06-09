import socket
import json

BUFFSIZE = 4096


class YaqDaemonException(Exception):
    pass


class Client:
    def __init__(self, port, host="127.0.0.1"):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))

        commands = self.send("list_commands")
        for c, d in zip(commands, self.send("help", commands)):
            if hasattr(self, c):
                continue

            def fun(comm):
                return lambda *args, **kwargs: self.send(comm, *args, **kwargs)

            setattr(self, c, fun(c))
            getattr(self, c).__doc__ = d

    def help(self, command=None):
        print(self.send("help", command))

    def send(self, command, *args, **kwargs):
        message = {"command": command, "args": args, "kwargs": kwargs}
        if len(args) == 0:
            message.pop("args")
        if len(kwargs) == 0:
            message.pop("kwargs")
        self._socket.sendall(json.dumps(message).encode())
        message = self._socket.recv(BUFFSIZE)
        message = json.loads(message)
        if not message["ok"]:
            raise YaqDaemonException(message["reason"])
        if "result" in message:
            return message["result"]
