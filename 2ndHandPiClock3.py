#!/usr/bin/env python
from sense_hat import SenseHat
import time

"""
  Second Hand Pi Clock (2ndHandPiClock3.py)
  asun.net 1/25/2025

  Raspberry Pi Sense HAT 12 hour time of day clock with
  digital or analog hours, analog minutes, and analog seconds.

  The time of day display on the Sense HAT's 8x8 RGB LED matrix is
  unique for every second around the clock. Any exact hh:mm:ss time
  is visually discernable at any time.

  v3 - Displays accumulating minutes and/or seconds ring

"""

####
# Clock display settings
####
showSecond = 1  #  0 disable
  #  1 walking dot
  #  2 accumulating seconds ring resetting at 0
  #  3 walking dot starting at top left corner
showMinute = 2  #  0 disable
  #  1 walking double dot
  #  2 accumulating minutes ring
  #  3 walking single dot starting at top left corner
showHour   = 1  #  0 disable
  #  1 digital
  #  2 analog


# Reverse Array
def revArr(arr, start, end):
    while start < end:
      arr[start], arr[end] = arr[end], arr[start]
      start += 1
      end -= 1

# Rotate Left Array by d elements
def rotLeftArr(arr, d):
    n = len(arr)
    d %= n
    revArr(arr, 0, d - 1)
    revArr(arr, d, n - 1)
    revArr(arr, 0, n - 1)

# Rotate Right Array by k times
def rotRightArr(arr, k):
    n = len(arr)
    k %= n
    revArr(arr, 0, n - 1)
    revArr(arr, 0, k - 1)
    revArr(arr, k, n - 1)


sense = SenseHat()

number3x5 = [
 0,1,0, #zero
 1,0,1,
 1,0,1,
 1,0,1,
 0,1,0,
 0,1,0, #one
 1,1,0,
 0,1,0,
 0,1,0,
 0,1,0,
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
 0,1,0,
 0,1,0,
 1,1,1, #eight
 1,0,1,
 0,1,0,
 1,0,1,
 1,1,1,
 0,1,0, #nine
 1,0,1,
 1,1,1,
 0,0,1,
 1,1,0,
 0,1,0, #ten
 1,0,1,
 1,0,1,
 1,0,1,
 0,1,0,
 0,1,0, #eleven
 0,1,0,
 0,1,0,
 0,1,0,
 0,1,0,
 0,1,0, #twelve
 1,0,1,
 0,0,1,
 0,1,0,
 1,1,1 ]

red   = [255,  0,  0]
green = [  0,255,  0]
blue  = [  0,  0,255]
black = [  0,  0,  0]
white = [255,255,255]
yellow     = [255,255,  0]
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
for i in range(len(image)):
    image[i] = black

ring0 = [ # seconds, 0 at image[1]
     1,  2,  3,  4,  5,  6,   # overlap  6, 15
    15, 23, 31, 39, 47, 55,   # overlap 55, 62
    62, 61, 60, 59, 58, 57,   # overlap 57, 48
    48, 40, 32, 24, 16,  8 ]  # overlap  8,  1
for i in range(24):
    image[ring0[i]] = yellowlite
if showSecond == 1:
    rotLeftArr(ring0, 3) # shift 0 to image[4]
elif showSecond == 2:
    rotLeftArr(ring0, 2) # shift 0 to image[3]

ring1 = [ # minutes, 0 at image[9]
     9, 10, 11, 12, 13,
    14, 22, 30, 38, 46,
    54, 53, 52, 51, 50,
    49, 41, 33, 25, 17 ]
ring1hr = [0] * len(ring1)
for i in range(len(ring1)):
  ring1hr[i] = ring1[i]
if showMinute == 1:
  rotLeftArr(ring1, 3) # shift 0 to image[12]
elif showMinute == 2:
  rotLeftArr(ring1, 2) # shift 0 to image[11]

rotLeftArr(ring1hr, 3) # shift 0 to image[12]
ring2 = [ # hours, 0 at image[18]
    18, 19, 20, 21,
    29, 37, 45, 44,
    43, 42, 34, 26 ]
rotLeftArr(ring2, 2) # shift 0 to image[20]
ring3 = [
    27, 28, 36, 35 ]
rotLeftArr(ring3, 1)

ring2d15 = [18, 17,  9, 10 ] # hours digit position every 15 minutes
if showMinute == 1 or showMinute == 2:
  rotLeftArr(ring2d15, 1)
ring2d30 = [17, 10 ]         # hours digit position every 30 minutes


####
# Main Loop
####
while True:
    now = time.time()
    hour = time.localtime(now).tm_hour
    hour12 = hour%12
    if hour12 == 0:
      hour12 = 12
    minute = time.localtime(now).tm_min
    second = time.localtime(now).tm_sec
    msecond = int(now*1000)%1000
    if msecond < 500 and False:
      print("%02d:%02d:%02d.%03d" % (hour, minute, second, msecond))

# background and border
    for r in range(1, 7):
      for c in range(1, 7):
        image[r*8+c] = black
    if second == 0 and showSecond == 2:
      for c in range(24):
        image[ring0[c]] = yellowlite

# hours (digital)
    if showHour == 1:
      if True:
        pixpos1 = ring2d15[int(minute/15)]
      else:
        pixpos1 = ring2d30[int(minute/30)]      # :00 :30
        if showMinute == 1:
          pixpos1 = ring2d30[int((minute+8)/30)%2]      # :22 :52
        elif showMinute == 2:
          pixpos1 = ring2d30[int((minute+6)/30)%2]      # :24 :54
      if hour12 > 9:
        for r in range(5):      # show the 1 for hours 10, 11, 12
          image[pixpos1+r*8] = red
        pixpos1 = pixpos1 + 2
      else:
        pixpos1 = pixpos1 + 1
      for r in range(5):        # show digit font for hours
        for c in range(3):
          if number3x5[(hour12)*15+r*3+c] == 1:
            image[r*8+c+pixpos1] = red

# hours
    elif showHour == 2:
      image[ring2[hour%12]] = red
      image[ring2[(hour-1+12)%12]] = red
      image[ring3[int((hour+1)/3)%4]] = red
      image[ring3[(int((hour+1)/3)-1+4)%4]] = red
      image[ring1hr[int((hour%12)*20/12)]] = red
      if hour%3 == 0:
        image[ring1hr[(int((hour%12)*20/12)-1+20)%20]] = red
      image[ring3[int((hour+5)/3)%4]] = red
      image[ring3[int((hour+6)/3)%4]] = red

# minutes
    if showMinute > 0:
      if showMinute == 2:
        if minute > 1:
          minute = minute + 1
        ringPos = int(minute/3)
        if ringPos > 1:         # fill in accumulated minutes
          for i in range(1, ringPos):
            if image[ring1[i]] == black:
              image[ring1[i]] = white
      ringPos = int(minute/3)%20
      ringPosNext = (ringPos+1)%20
      ringPosPrev = (ringPos-1+20)%20
      if minute%3 == 2:
        image[ring1[ringPosNext]] = white
        image[ring1[ringPos]] = green
      else:
        if showMinute != 2 or minute > 2:
          image[ring1[ringPos]] = white
        if minute%3 == 1:
          image[ring1[ringPosNext]] = green
        if (showMinute == 1 and minute%3 == 0):
          image[ring1[ringPosPrev]] = white

# seconds
    if showSecond > 0:
      if showSecond == 2:
        if second > 1:
          second = second + 1
        ringPos   = (int((second+6)/15)+int(second/3))%24
      else:
        ringPos   = (int(second/15)+int(second/3))%24
      ringPosNext = (ringPos+1)%24
      ringPosPrev = (ringPos-1+24)%24
      if second%3 == 2:
        image[ring0[ringPosNext]] = white
        image[ring0[ringPos]] = green
      else:
        if showSecond != 2 or second > 2:
          image[ring0[ringPos]] = white
        if second%3 == 1:
          image[ring0[ringPosNext]] = green
        if ((showSecond != 2 and second%15 != 0) or
            (showSecond == 2 and second <= 4)):
          image[ring0[ringPosPrev]] = yellowlite
        else:
          image[ring0[ringPosPrev]] = white
      ringPosPrev2 = (ringPos-2+24)%24
      if showSecond != 2 and second%15 == 0:
        image[ring0[ringPosPrev2]] = yellowlite
      elif showSecond == 2 and (second+6)%15 == 0:
        image[ring0[ringPosPrev2]] = white

# 1/2 second
    if msecond >= 500:
      image[63] = red
    else:
      image[63] = black

# Display the time
#   sense.set_rotation(90) # Optional
#   sense.low_light = True # Optional
    sense.set_pixels(image)

    time.sleep((500.0-msecond%500)/1000.0)
