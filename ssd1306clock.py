# Original source/inspiration:
#       https://techatronic.com/ssd1306-raspberry-pi-pico/

# Frame buffer stuff:
#       https://docs.micropython.org/en/latest/library/framebuf.html

from machine import Pin, SPI, RTC
from ssd1306 import SSD1306_SPI
from ssd1306font import Display_font

import framebuf
from utime import sleep_ms

def ssd_text(string, font, char_height, offset=1):
    oled.fill(0)
    for c in string:
        try:
            fontchar = font[c]   # get char layout
        except KeyError:
            fontchar = font[":"] # default to ":" if not found. 
            
        char_width = len(fontchar)
        for i, line in enumerate(fontchar):
            ssd_x = i + offset
            for j, char_pixel in enumerate(line):
                ssd_y = (char_height - j) * 2 + 1 
                if char_pixel != " ":
                    oled.pixel(ssd_x, ssd_y, 1)
        offset += char_width + 2
    oled.show()

#-------------------------------------------------------------------------------------------
spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
#                 (width, height, spi, dc,      res,     cs, external_vcc=False):  
oled = SSD1306_SPI(128, 64,       spi, Pin(17), Pin(20), Pin(16))
font = Display_font("font28.txt")
fontsize = font.font_height
ssd_font = font.font

rtc_obj = RTC()
last_seconds = -1
wait = 100
try:
    while True:
#       rtc = (year, month, day, weekday, hours, minutes, seconds, subseconds)
        rtc = rtc_obj.datetime()
        seconds = rtc[6]
        if last_seconds != seconds:
            mytime = f"{rtc[4]:02d}" + ":" + f"{rtc[5]:02d}" + ":" + f"{seconds:02d}"
            ssd_text(mytime, ssd_font, fontsize, 30)
        last_seconds = seconds
        
        sleep_ms(wait)
except KeyboardInterrupt:
    pass
