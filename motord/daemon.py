#! /usr/bin/env python3
import asyncio
import serial
import struct

_position = 0
_destination = 0
_limit_status = False
_stopped = False
_port = serial.Serial("/dev/ttyUSB0", timeout=0, baudrate=57600)


async def update_state():
    global _position, _limit_status, _stopped, _port
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
            print(f"Update State: {_position}, {_stopped}, {overflow}")
        else:
            _stopped = _position == _destination
        await asyncio.sleep(0.01)


def home():
    raise NotImplementedError

def move_abs(position):
    _destintation = position
    _port.write(str(position).encode())
    _stopped = False

def move_rel(diff):
    move_abs(_position + diff)

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
        message = data.decode()
        print('Data received: {!r}'.format(message))

        if message.startswith("home"):
            home()
            self.transport.write(f"SUCCESS: {message}".encode())
        elif message.startswith("move_abs"):
            move_abs(int(message[8:]))
            self.transport.write(f"SUCCESS: {message}".encode())
        elif message.startswith("move_rel"):
            move_rel(int(message[8:]))
            self.transport.write(f" SUCCESS: {message}".encode())
        elif message.startswith("position"):
            self.transport.write(str(get_position()).encode())
            self.transport.write(f"SUCCESS: {message}".encode())
        else:
            self.transport.write("ERROR: unrecognized command".encode())



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
