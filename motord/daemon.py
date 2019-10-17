#! /usr/bin/env python3
import asyncio

import yaq_serial
from yaqd_core import hardware, set_action

class WlMotorDaemon(hardware.ContinuousHardwareDaemon):
    _kind = "wl-motor"
    defaults = {"baudrate": 57600}

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)

        self.limit_status = False
        self._port = yaq_serial.YaqSerial(config["com_port"], baudrate=config["baudrate"])
        self._limits = config.get("limits", [(-100_000, 100_000)])

    def _set_position(self, position):
        self._port.write(str(position).encode() + b"\n")

    async def update_state(self):
        overflow = b""
        async for line in self._port.areadlines():
            line = line.replace(b"S", b"").replace(b"E",b"")
            try:
                self._position = float(line)
                self._busy = False
                self._destintation = self._position
            except:
                pass

    @set_action
    def home(self):
        self._port.write(b"H")

if __name__ == "__main__":
    WlMotorDaemon.main()
