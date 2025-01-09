#!/usr/bin/env python

"""
  Second Hand Pi Clock (2ndHandPiClock3.py)
  asun.net 1/9/2025

  Raspberry Pi sense hat 12 hour time of day clock with
  digital or analog hours, analog minutes, and analog seconds.

  The time of day display on the sense hat's 8x8 RGB LED matrix is
  unique for every second around the clock. Any exact hh:mm:ss time
  is visually discernable at any time.

  v3 - Displays accumulating seconds ring

"""

#
# Clock display settings
#
showSecond = 2  #  0 disable
  #  1 walking dot
  #  2 accumulating seconds ring resetting at 0
  #  3 accumulating resetting at 1 second
showHour   = 1  #  0 disable
  #  1 digital
  #  2 analog


from sense_hat import SenseHat
import time

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
 1,1,1, #zero
 1,0,1,
 1,0,1,
 1,0,1,
 1,1,1,
 0,1,0, #one
 0,1,0,
 0,1,0,
 0,1,0,
 0,1,0,
 1,1,1, #two
 0,0,1,
 1,1,1,
 1,0,0,
 1,1,1,
 1,1,1, #three
 0,0,1,
 0,1,1,
 0,0,1,
 1,1,1,
 1,0,0, #four
 1,0,1,
 1,1,1,
 0,0,1,
 0,0,1,
 1,1,1, #five
 1,0,0,
 1,1,1,
 0,0,1,
 1,1,1,
 1,1,0, #six
 1,0,0,
 1,1,1,
 1,0,1,
 1,1,1,
 1,1,1, #seven
 0,0,1,
 0,1,0,
 0,1,0,
 0,1,0,
 1,1,1, #eight
 1,0,1,
 1,1,1,
 1,0,1,
 1,1,1,
 1,1,1, #nine
 1,0,1,
 1,1,1,
 0,0,1,
 1,1,1
]

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
elif showSecond == 2 or showSecond == 3:
    rotLeftArr(ring0, 2) # shift 0 to image[3]

ring1 = [ # minutes, 0 at image[9]
     9, 10, 11, 12, 13,
    14, 22, 30, 38, 46,
    54, 53, 52, 51, 50,
    49, 41, 33, 25, 17 ]
rotLeftArr(ring1, 3) # shift 0 to image[12]

ring2 = [ # hours, 0 at image[18]
    18, 19, 20, 21,
    29, 37, 45, 44,
    43, 42, 34, 26 ]
rotLeftArr(ring2, 2) # shift 0 to image[20]
ring3 = [
    27, 28, 36, 35 ]
rotLeftArr(ring3, 1)

ring2d15 = [18, 17,  9, 10 ] # hours digit position every 15 minutes
rotLeftArr(ring2d15, 1)
ring2d30 = [17, 10 ]         # hours digit position every 30 minutes


while True:
    now = time.time()
    hour = time.localtime(now).tm_hour
    hour12 = hour%12
    if hour12 == 0:
      hour12 = 12
    minute = time.localtime(now).tm_min
    second = time.localtime(now).tm_sec
    msecond = int(now*1000)%1000

# background and border
    if second == 0:
      for r in range(1, 7):
        for c in range(1, 7):
          image[r*8+c] = black
    if ((second == 0 and showSecond == 2) or
        (second == 1 and showSecond == 3)):
      for c in range(24):
        image[ring0[c]] = yellowlite

# hours (digital)
    if showHour == 1:
      pixpos1 = ring2d15[int(minute/15)]
      if hour12 > 9:
        for r in range(5):
          image[pixpos1+r*8] = red
        pixpos1 = pixpos1 + 2
      else:
        pixpos1 = pixpos1 + 1
      for r in range(5):
        for c in range(3):
          if number3x5[(hour12%10)*15+r*3+c] == 1:
            image[r*8+c+pixpos1] = red

# hours
    elif showHour == 2:
      image[ring2[hour%12]] = red
      image[ring2[(hour-1+12)%12]] = red
      image[ring3[int((hour+1)/3)%4]] = red
      image[ring3[(int((hour+1)/3)-1+4)%4]] = red
      image[ring1[int((hour%12)*20/12)]] = red
      if hour%3 == 0:
        image[ring1[(int((hour%12)*20/12)-1+20)%20]] = red
      image[ring3[int((hour+5)/3)%4]] = red
      image[ring3[int((hour+6)/3)%4]] = red

# minutes
    if minute%3 == 2:
      image[ring1[(int(minute/3)+1)%20]] = white
      image[ring1[int(minute/3)]] = green
    else:
      image[ring1[int(minute/3)]] = white
      if minute%3 == 1:
        image[ring1[(int(minute/3)+1)%20]] = green
      else:
        image[ring1[(int(minute/3)-1+20)%20]] = white

# seconds
    if showSecond > 0:
      if (showSecond == 2 or showSecond == 3):
        ringPos   = (int((second+6)/15)+int(second/3))%24
      else:
        ringPos   = (int(second/15)+int(second/3))%24
      ringPosNext = (ringPos+1)%24
      ringPosPrev = (ringPos-1+24)%24
      if second%3 == 2:
        image[ring0[ringPosNext]] = white
        image[ring0[ringPos]] = green
      else:
        if showSecond == 1 or second > 2:
          image[ring0[ringPos]] = white
        if second%3 == 1:
          image[ring0[ringPosNext]] = green
        else:
          if ((showSecond == 1 and second%15 != 0) or
              (showSecond == 2 and (second == 0 or second == 3)) or
              (showSecond == 3 and second == 3)):
            image[ring0[ringPosPrev]] = yellowlite
          else:
            image[ring0[ringPosPrev]] = white
      ringPosPrev2 = (ringPos-2+24)%24
      if showSecond == 1 and second%15 == 0:
        image[ring0[ringPosPrev2]] = yellowlite
      elif showSecond == 1 and (second-1+15)%15 == 0:
        image[ring0[ringPosPrev]] = yellowlite
      elif ((showSecond == 2 or showSecond == 3) and (second+6)%15 == 0):
        image[ring0[ringPosPrev2]] = white

# 1/2 second
    if msecond >= 500:
      image[0] = red
    else:
      image[0] = black

# Display the time
#   sense.set_rotation(90) # Optional
#   sense.low_light = True # Optional
    sense.set_pixels(image)

    time.sleep((500.0-msecond%500)/1000.0)
