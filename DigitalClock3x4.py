#!/usr/bin/env python
from sense_hat import SenseHat
import time

"""
  Digital Clock 3x4 (DigitalClock3x4.py)
  asun.net 3/11/2025

  Raspberry Pi time of day digital clock with 3x4 number fonts
  formatted for the Sense HAT's 8x8 RGB LED matrix display.

  Repository: https://github.com/asunxx/rpi-sense-hat-clock
  Original concept: clock.py
    https://github.com/SteveAmor/Raspberry-Pi-Sense-Hat-Clock

"""

sense = SenseHat()

number3x4 = [
  1,1,1, #zero
  1,0,1,
  1,0,1,
  1,1,1,
  0,1,0, #one
  1,1,0,
  0,1,0,
  1,1,1,
  1,1,0, #two
  0,0,1,
  1,1,0,
  1,1,1,
  1,1,0, #three
  0,1,1,
  0,0,1,
  1,1,0,
  1,0,0, #four
  1,0,1,
  1,1,1,
  0,0,1,
  1,1,1, #five
  1,0,0,
  0,1,1,
  1,1,1,
  1,0,0, #six
  1,1,1,
  1,0,1,
  1,1,1,
  1,1,1, #seven
  0,0,1,
  0,1,0,
  1,0,0,
  1,1,1, #eight
  0,1,0,
  1,0,1,
  1,1,1,
  1,1,1, #nine
  1,0,1,
  1,1,1,
  0,0,1 ]

red   = [255,  0,  0]
green = [  0,255,  0]
blue  = [  0,  0,255]
black = [  0,  0,  0]
white = [255,255,255]
magenta = [255,  0,255]
cyan    = [  0,255,255]
yellow  = [255,255,  0]
yellowlite = [128,128,  0]
greenlite  = [  0,128,  0]

image = [
    0, 0, 0, 0, 0, 0, 0, 0,   #  0 ..  7
    0, 0, 0, 0, 0, 0, 0, 0,   #  8 .. 15
    0, 0, 0, 0, 0, 0, 0, 0,   # 16 .. 23
    0, 0, 0, 0, 0, 0, 0, 0,   # 24 .. 31
    0, 0, 0, 0, 0, 0, 0, 0,   # 32 .. 39
    0, 0, 0, 0, 0, 0, 0, 0,   # 40 .. 47
    0, 0, 0, 0, 0, 0, 0, 0,   # 48 .. 55
    0, 0, 0, 0, 0, 0, 0, 0 ]  # 56 .. 63

def draw_digit(digit, position, color):
    for r in range(4):
      for c in range(3):
        pix = number3x4[digit*12+r*3+c]
        if pix == 1:
          image[r*8+c+position] = color

####
# Main Loop
####
while True:
    now = time.time()
    hour24 = time.localtime(now).tm_hour
    hour12 = hour24%12
    if hour12 == 0:
      hour12 = 12
    hour = hour24 if True else hour12
    minute = time.localtime(now).tm_min
    second = time.localtime(now).tm_sec
    msecond = int(now*1000)%1000
#   hour = (minute+0)%24+0      # debug
#   minute = second             # debug
    if False:
      print("%02d:%02d:%02d.%03d" % (hour, minute, second, msecond))

# background and border
    for i in range(64):
      image[i] = black

# hours
    if True:
      d1 = int(hour/10)
      d2 = hour%10

      if d1 != 0:
        draw_digit(d1, 0, red)
      draw_digit(d2, 4, red)

# minutes
    if True:
      d1 = int(minute/10)
      d2 = minute%10

      draw_digit(d1, 33, cyan)
      draw_digit(d2, 37, cyan)

# seconds
    pass

# 1/2 second
    if True:
      if msecond >= 500:
        image[7] = cyan
      else:
        image[7] = black

# Display the time
#   sense.set_rotation(90)      # Optional
#   sense.low_light = True      # Optional
    sense.set_pixels(image)

    time.sleep((500.0-msecond%500)/1000.0)
