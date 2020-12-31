import digitalio
import board
import time

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

class SPScreen(object):

    def __init__(self):

        self.cs_pin = digitalio.DigitalInOut(board.CE0)
        self.dc_pin = digitalio.DigitalInOut(board.D25)

        self.reset_pin = None

        # Config for display baudrate (default max is 24mhz):
        self.BAUDRATE = 64000000
        self.spi = board.SPI()
        self.defaultBg = (16, 23, 31)

        # Create the ST7789 display:
        self.disp = st7789.ST7789(
            self.spi,
            cs=self.cs_pin,
            dc=self.dc_pin,
            rst=self.reset_pin,
            baudrate=self.BAUDRATE,
            width=135,
            height=240,
            x_offset=53,
            y_offset=40,
        )

        # Make sure to create image with mode 'RGB' for full color.
        self.height = self.disp.width  # swap height/width to rotate it to landscape
        self.width = self.disp.height
        self.image = Image.new("RGB", (self.width, self.height))
        self.rotation = 270

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        self.clear(self.defaultBg)

        self.padding = 5
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.x = 5

        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)

        self.backlight = digitalio.DigitalInOut(board.D22)
        self.backlight.switch_to_output()
        self.backlight.value = True
        self.auto_brightness = False
        self.brightness = 0.1


    def backlightOff(self):
        self.backlight.value = False


    def clear(self, bg):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=bg)
        self.disp.image(self.image, self.rotation)


    def message(self, message, color, bg):
        self.clear(bg)
        # self.y = self.top

        parts = message.split('|')
        for x in parts:
            self.draw.text((self.x, self.y), x, font=self.font, fill=color)
            self.y += self.font.getsize(x)[1]
            self.y += 9

        self.disp.image(self.image, self.rotation)
        # time.sleep(0.1)
