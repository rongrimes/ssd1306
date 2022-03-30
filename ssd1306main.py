# Original source/inspiration:
#       https://techatronic.com/ssd1306-raspberry-pi-pico/

# Frame buffer stuff:
#       https://docs.micropython.org/en/latest/library/framebuf.html

from machine import Pin, SPI, RTC
from ssd1306 import SSD1306_SPI
from ssd1306font import Display_font

import framebuf
from utime import sleep_ms

def show_image(filename):
    oled.fill(0)
    oled.show()
    oled.text(filename, 0, 0)
    oled.show()
    sleep_ms(1000)

def hlines(c):
    for row in range(1,63,2): # shows odd numbered lines
        oled.hline(0, row, 128, c)
        oled.show()
        sleep_ms(50)
    sleep_ms(1000)

def vlines(c):
    for col in range(128):
        oled.vline(col, 0, 64, c)
        oled.show()
        sleep_ms(20)
    sleep_ms(1000)

def grow_square(c):
    oled.hline(16, 33, 96, c)
    oled.show()
    sleep_ms(50)
    
    for i in range(1,16):
        oled.rect(16-i, 33-i*2, 96+i*2, i*4+1, c)
        oled.show()
        sleep_ms(50)
    sleep_ms(1000)

def ssd_text(string, font, char_height, offset=1):
    oled.fill(0)
#   oled.show()
            
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
#       oled.show()
        offset += char_width + 2
    oled.show()

#-------------------------------------------------------------------------------------------
spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
#                 (width, height, spi, dc,      res,     cs, external_vcc=False):  
oled = SSD1306_SPI(128, 64,       spi, Pin(17), Pin(20), Pin(16))
font = Display_font("font28.txt")
fontsize = font.font_height
ssd_font = font.font

while True:
    try:
        rtc_obj = RTC()
#       rtc = (year, month, day, weekday, hours, minutes, seconds, subseconds)
        for _ in range(5): 
#       while True`: 
            rtc = rtc_obj.datetime()
            mytime = f"{rtc[4]:02d}" + ":" + f"{rtc[5]:02d}" + ":" + f"{rtc[6]:02d}"
            ssd_text(mytime, ssd_font, fontsize, 30)
            sleep_ms(1000)

        for i in range(11):
            ssd_text(str(i), ssd_font, fontsize, 60)
            sleep_ms(500)
            
        for offset in range(1,51,10):
            oled.fill(0)
#           oled.show()
            oled.text("HELLO WORLD",offset,offset)
            oled.show()
            sleep_ms(250)

        oled.fill(0)
        oled.rect(0,1,128,63,1)
        oled.show()
        sleep_ms(1000)

        oled.hline(0,33,128,1)
        oled.vline(63,0,63,1)
        oled.show()
        sleep_ms(1000)

        oled.fill(0)
        oled.show()
        hlines(1)
        hlines(0)

        oled.fill(0)
        oled.show()
        vlines(1)
        vlines(0)

        oled.fill(0)
        oled.show()
        grow_square(1)
        grow_square(0)
#
#       Read/show image
#       show_image("frog.bmp")

    except KeyboardInterrupt:
        break
  