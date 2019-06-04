#! /usr/bin/env python3
import asyncio
import serial
import struct
import time
import json

_position = 0
_destination = 0
_limit_status = False
_stopped = False
_port = serial.Serial("/dev/ttyUSB0", timeout=0, baudrate=57600)


async def update_state():
    global _destination, _position, _limit_status, _stopped, _port
    overflow = b""
    while True:
        if _port.in_waiting:
            message = _port.read(_port.in_waiting)
            print(f"Update State: {message!r}")
            try:
                message = overflow + message
                word = message.split(b"E")[-2]
                word = word.split(b"S")[-1]
                new_position = int(word)
                overflow = b""
            except (ValueError, IndexError) as e:
                print("Exception occurred", e)
                overflow = message
                continue
            _stopped = True
            _position = new_position
            _destination = _position
            print(f"Update State: {_position}, {_stopped}, {overflow}")
        await asyncio.sleep(0.01)


def home():
    raise NotImplementedError

def move_abs(position):
    global _destination, _port, _stopped
    _destintation = position
    _port.write(str(position).encode() + b'\n')
    _stopped = False

def move_rel(diff):
    move_abs(_destination + diff)

def is_busy():
    return not _stopped

def get_position():
    return _position



class MotorServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        print('Data received: {!r}'.format(data))
        response = {}
        try:
            request = json.loads(data)
            command = request["command"]
            response = {"ok": True, "command": command}

            if command == "home":
                home()
            elif command == "move_abs":
                move_abs(request["value"])
            elif command == "move_rel":
                move_rel(request["value"])
            elif command == "position":
                response["result"] = get_position()
            elif command == "is_busy":
                response["result"] = is_busy()
            else:
                response["ok"] = False
                response["reason"] = "unrecognized command"
        except Exception as e:
            response["ok"] = False
            response["reason"] = repr(e)
        self.transport.write(json.dumps(response).encode())



async def main(port=19853):
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: MotorServerProtocol(),
        '127.0.0.1', port)

    async with server:
        await server.serve_forever()


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.create_task(update_state())
loop.run_forever()
