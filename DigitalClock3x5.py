#!/usr/bin/env python
from sense_hat import SenseHat
import time

"""
  Digital Clock 3x5 (DigitalClock3x5.py)
  asun.net 3/8/2025

  Raspberry Pi time of day digital clock with 3x5 number fonts
  formatted for the Sense HAT's 8x8 RGB LED matrix display.

  Four 3x5 clock digits will overlap on the 8x8 display matrix
  since there's insufficient space to fit them all at once.
  The code dynamically places clock digits to minimize
  overlapping pixels. To maintain readability of overlapping
  digits, overlapping pixels alternate their color pattern.

  Repository: https://github.com/asunxx/rpi-sense-hat-clock
  Original concept: MixiClock.pde
    http://timewitharduino.blogspot.com/2012/01/mixiclock-4-digits-displayed-on-8x8-led.html

"""

sense = SenseHat()

number3x5 = [
 0,1,0, #zero
 1,0,1,
 1,0,1,
 1,0,1,
 0,1,0,
 0,0,1, #one
 0,0,1,
 0,0,1,
 0,0,1,
 0,0,1,
 0,1,0, #two
 1,0,1,
 0,0,1,
 0,1,0,
 1,1,1,
 1,1,1, #three
 0,0,1,
 0,1,0,
 0,0,1,
 1,1,0,
 1,0,0, #four
 1,0,1,
 1,1,1,
 0,0,1,
 0,0,1,
 1,1,1, #five
 1,0,0,
 1,1,1,
 0,0,1,
 1,1,0,
 0,1,1, #six
 1,0,0,
 1,1,1,
 1,0,1,
 0,1,0,
 1,1,1, #seven
 0,0,1,
 0,1,0,
 1,0,0,
 1,0,0,
 1,1,1, #eight
 1,0,1,
 0,1,0,
 1,0,1,
 1,1,1,
 0,1,0, #nine
 1,0,1,
 1,1,1,
 0,0,1,
 1,1,0 ]

red   = [255,  0,  0]
green = [  0,255,  0]
blue  = [  0,  0,255]
black = [  0,  0,  0]
white = [255,255,255]
magenta = [255,  0,255]
cyan    = [  0,255,255]
yellow  = [255,255,  0]

image = [
    0, 0, 0, 0, 0, 0, 0, 0,   #  0 ..  7
    0, 0, 0, 0, 0, 0, 0, 0,   #  8 .. 15
    0, 0, 0, 0, 0, 0, 0, 0,   # 16 .. 23
    0, 0, 0, 0, 0, 0, 0, 0,   # 24 .. 31
    0, 0, 0, 0, 0, 0, 0, 0,   # 32 .. 39
    0, 0, 0, 0, 0, 0, 0, 0,   # 40 .. 47
    0, 0, 0, 0, 0, 0, 0, 0,   # 48 .. 55
    0, 0, 0, 0, 0, 0, 0, 0 ]  # 56 .. 63

def draw_digit(digit, position, color, color2 = black):
    for r in range(5):
      for c in range(3):
        if number3x5[digit*15+r*3+c] == 1:
          pixpos = r*8+c+position
          if image[pixpos] == black:
            image[pixpos] = color
          else:
            if color2 != black:
              image[pixpos] = color2

def ovl_digit(digit, position): # count overlap pixels for digit
    n = 0
    for r in range(3, 5):       # assume rows 0, 1, 2 never overlap
      for c in range(3):
        if (number3x5[digit*15+r*3+c] == 1 and
            image[r*8+c+position] != black):
          n = n + 1
    return n

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
    for i in range(len(image)):
      image[i] = black

# minutes
    if True:
      d1 = int(minute/10)
      d2 = minute%10
      d1off = 0
      # shift to left the first digit in minute if hours are single-digit
#     if (hour < 10):
      if (hour < 10 and hour != 1 and hour != 7):
        d1off = 1
      # shift to left if first digit in minute is 1
      if (d1 == 1):
        if (10 <= hour < 20):
          d1off = 2
        else:
          d1off = 0

      d1pos = 25
      d2pos = 29
      draw_digit(d1, d1pos - d1off, green, yellow)
      draw_digit(d2, d2pos, green, yellow)

# hours
    if True:
      d1 = int(hour/10)
      d2 = hour%10
      minUnit = minute%10
      minDecs = int(minute/10)
      d1off = 5
      d2off = 1

      d1pos = 5
      d2pos = 5

      if d1 == 0:
        # show just one digit, in the middle
        d1off = 8       # out of display
        d2off = 3
#       if (d2 == 0 or d2 == 2 or d2 == 3 or d2 == 7):
#         d2off = 2
        if (minUnit == 1):
          d2off = 2

        if (minDecs == 1 or d2 == 7):
          d2off = 5
        if (d2 == 1):
          d2off = 7
        if (d2off == 3 and d2 != 1 and d2 != 4):
          # find offset with fewest pixel overlaps
          ovlapMin = 3*5+1
          for t2off in (3, 2):
            ovlap = ovl_digit(d2, d2pos-t2off)
            if ovlap < ovlapMin:
              ovlapMin = ovlap
              d2off = t2off

      elif d1 == 1:
        # show one in the first column
        d1off = 7
        if (d2 == 1 or d2 == 4):
          d2off = 3
        if (minDecs == 1):
          d2off = 3

        if (d2off == 1 and d2 != 7):
          # find offset with fewest pixel overlaps
          ovlapMin = 3*5+1
          for t2off in (2, 3, 1):
            ovlap = ovl_digit(d2, d2pos-t2off)
            if ovlap < ovlapMin:
              ovlapMin = ovlap
              d2off = t2off

      elif d2 == 1:
        # show one in the middle column
        d2off = 3

      if True:
        if second%2 == 0:
          if d1 != 0:
            draw_digit(d1, d1pos - d1off, red, red)
          draw_digit(d2, d2pos - d2off, red, red)
        else:
          if d1 != 0:
            draw_digit(d1, d1pos - d1off, red)
          draw_digit(d2, d2pos - d2off, red)
      else:
        if d1 != 0:
          draw_digit(d1, d1pos - d1off, red, yellow)
        draw_digit(d2, d2pos - d2off, red, yellow)

# seconds
    pass

# 1/2 second
    if True:
      if msecond >= 500:
        image[7] = green
      else:
        image[7] = black

# Display the time
#   sense.set_rotation(90)      # Optional
#   sense.low_light = True      # Optional
    sense.set_pixels(image)

    time.sleep((500.0-msecond%500)/1000.0)
