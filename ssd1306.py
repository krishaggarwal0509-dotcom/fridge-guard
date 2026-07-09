from machine import I2C
import framebuf

class SSD1306_I2C:
    def __init__(self, width, height, i2c, addr=0x3C):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray(self.height * self.width // 8)
        self.framebuf = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, buf):
        self.i2c.writeto(self.addr, b'\x40' + buf)

    def init_display(self):
        cmds = [
            0xAE, 0x20, 0x00, 0x40, 0xA1, 0xC8, 0x81, 0xFF,
            0xA6, 0xA8, self.height - 1, 0xD3, 0x00, 0xD5,
            0x80, 0xD9, 0xF1, 0xDA, 0x12, 0xDB, 0x40,
            0x8D, 0x14, 0xAF
        ]
        for cmd in cmds:
            self.write_cmd(cmd)

    def fill(self, color):
        self.framebuf.fill(color)

    def text(self, string, x, y):
        self.framebuf.text(string, x, y)

    def show(self):
        for page in range(self.height // 8):
            self.write_cmd(0xB0 | page)
            self.write_cmd(0x00)
            self.write_cmd(0x10)
            start = self.width * page
            end = start + self.width
            self.write_data(self.buffer[start:end])



