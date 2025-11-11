# mcp2515.py
# MCP2515 CAN Controller Driver for Raspberry Pi Pico

from machine import Pin, SPI
import time

# Register addresses (trimmed for brevity — keep your full list)
CAN_RESET    = 0xC0
CAN_READ     = 0x03
CAN_WRITE    = 0x02
CAN_RTS_TXB0 = 0x81
CAN_RD_STATUS= 0xA0

# Example CAN rate dictionary (adjust for oscillator frequency!)
CAN_RATE = {
    "500KBPS": [0x00, 0x9E, 0x03],  # for 16 MHz crystal
    "125KBPS": [0x03, 0x9E, 0x03],
}

class MCP2515:
    def __init__(self, spi_bus=0, cs_pin=5, baud="500KBPS"):
        self.spi = SPI(spi_bus, baudrate=10_000_000,
                       polarity=0, phase=0,
                       sck=Pin(6), mosi=Pin(7), miso=Pin(4))
        self.cs = Pin(cs_pin, Pin.OUT)
        self.baud = baud
        self.reset()
        self.init_can()

    def _select(self):
        self.cs(0)

    def _deselect(self):
        self.cs(1)

    def reset(self):
        self._select()
        self.spi.write(bytearray([CAN_RESET]))
        self._deselect()
        time.sleep(0.1)

    def write_reg(self, addr, val):
        self._select()
        self.spi.write(bytearray([CAN_WRITE, addr, val]))
        self._deselect()

    def read_reg(self, addr):
        self._select()
        self.spi.write(bytearray([CAN_READ, addr]))
        res = self.spi.read(1)
        self._deselect()
        return int.from_bytes(res, 'big')

    def init_can(self):
        cnf = CAN_RATE[self.baud]
        self.write_reg(0x2A, cnf[0])  # CNF1
        self.write_reg(0x29, cnf[1])  # CNF2
        self.write_reg(0x28, cnf[2])  # CNF3
        # Put controller in normal mode
        self.write_reg(0x0F, 0x00)

    def send(self, can_id, data):
        # Load ID
        self.write_reg(0x31, (can_id >> 3) & 0xFF)  # TXB0SIDH
        self.write_reg(0x32, (can_id & 0x07) << 5)  # TXB0SIDL
        # Load data
        for i, b in enumerate(data):
            self.write_reg(0x36 + i, b)
        # Set DLC
        self.write_reg(0x35, len(data) & 0x0F)
        # Request to send
        self._select()
        self.spi.write(bytearray([CAN_RTS_TXB0]))
        self._deselect()
