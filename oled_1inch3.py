# oled_1inch3.py
# Waveshare 1.3-inch OLED HAT driver for Raspberry Pi Pico (MicroPython)

from machine import Pin, SPI
import framebuf, time

# Pin definitions (adjust if needed)
DC   = 8
RST  = 12
MOSI = 11
SCK  = 10
CS   = 9

class OLED_1inch3(framebuf.FrameBuffer):
    def __init__(self, rotate=180):
        self.width = 128
        self.height = 64
        self.rotate = rotate  # only 0 or 180

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(1, baudrate=20_000_000, polarity=0, phase=0,
                       sck=Pin(SCK), mosi=Pin(MOSI), miso=None)
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)

        self.white = 0xFFFF
        self.black = 0x0000

        self.init_display()

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)

        self.write_cmd(0xAE)  # display off
        self.write_cmd(0x00)  # set lower column
        self.write_cmd(0x10)  # set higher column
        self.write_cmd(0xB0)  # set page address
        self.write_cmd(0xDC)  # set display start line
        self.write_cmd(0x00)
        self.write_cmd(0x81)  # contrast
        self.write_cmd(0x6F)
        self.write_cmd(0x21)  # memory addressing mode
        self.write_cmd(0xA0 if self.rotate == 0 else 0xA1)  # segment remap
        self.write_cmd(0xC0)  # COM scan direction
        self.write_cmd(0xA4)  # disable entire display on
        self.write_cmd(0xA6)  # normal display
        self.write_cmd(0xA8)  # multiplex ratio
        self.write_cmd(0x3F)  # duty = 1/64
        self.write_cmd(0xD3)  # display offset
        self.write_cmd(0x60)
        self.write_cmd(0xD5)  # osc division
        self.write_cmd(0x41)
        self.write_cmd(0xD9)  # pre-charge period
        self.write_cmd(0x22)
        self.write_cmd(0xDB)  # vcomh
        self.write_cmd(0x35)
        self.write_cmd(0xAD)  # charge pump enable
        self.write_cmd(0x8A)
        self.write_cmd(0xAF)  # display on

    def show(self):
        self.write_cmd(0xB0)
        for page in range(0, 64):
            column = 63 - page if self.rotate == 0 else page
            self.write_cmd(0x00 + (column & 0x0F))
            self.write_cmd(0x10 + (column >> 4))
            for num in range(0, 16):
                self.write_data(self.buffer[page * 16 + num])
