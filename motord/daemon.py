#! /usr/bin/env python3
import asyncio

import serial
from yaq_daemon_core import hardware

class WlMotorDaemon(hardware.BaseHardwareDaemon):
    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)

        self.limit_status = False
        self._port = serial.Serial(config["com_port"], timeout=0, baudrate=config["baud_rate"])

    def _set_position(self, position):
        self._port.write(str(position).encode() + b"\n")

    async def update_state(self):
        overflow = b""
        while True:
            if self._port.in_waiting:
                message = self._port.read(self._port.in_waiting)
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
                self._not_busy.set()
                self._position = new_position
                self._destination = self._position
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    WlMotorDaemon.main()
