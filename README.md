# Raspberry Pi Sense Hat Clocks

This project implements time of day clocks for a
Raspberry Pi equipped with its official Sense Hat.
The clocks utilize the Sense Hat's 8x8 RGB LED matrix
to show the time.

![rpi3a-shat](assets/images/rpi3a-shat.jpg)

Raspberry Pi Sense Hat emulator at [https://trinket.io/sense-hat](https://trinket.io/sense-hat)


## Second Hand Pi Clock (2ndHandPiClock3.py)

This is a 12 hour time of day clock with digital or analog hours,
analog minutes, and analog seconds.
The clock's design shows a unique image for every second around the clock.
Any exact hh:mm:ss time is visually discernable at any time.

Digital hours time display:\
![Screenshot of time display 2:45:15](assets/images/Clock3.time.02.45.15.png)
2:45:15

Analog hours time display:\
![Screenshot of time display 10:10:40](assets/images/Clock3.time.10.10.40.png)
10:10:40


## Digital Clock 3x4 (DigitalClock3x4.py)

This is a 24 hour, four digit, digital clock.
A 3x4 dot matrix forms the two hours digits and the two minutes digits.
Hours and minutes digits have different colors
(red and cyan respectively) to separate them for readablility
since there's no bottom/top pixel spacing between them.
Seconds show as a 6-bit binary pattern of yellow pixels
at the right edge of the display.

![Screenshot of time display 18:23:29](assets/images/Clock3x4.time.18.23.29.png)
18:23:29


## Digital Clock 3x5 (DigitalClock3x5.py)

This is a 24 hour digital clock with clock digits formed with a 3x5 dot matrix.
There's insufficient space on the display to fit all four digits.
Thus clock digits may overlap.
The clock changes digit positions minute by minute
to minimize overlapping digits.
And when overlap is unavoidable, the overlapping pixels
use an alternate color pattern to improve digit readablility.
There's no seconds display for this clock design.

![Screenshot of time display 12:34](assets/images/Clock3x5.time.12.34.png)
12:34

