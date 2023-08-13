from st7735 import TFT
from machine import SPI,Pin
import time
import math

spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)


tft.fill(TFT.RED)
