#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
import keyboard

GPIO.setmode(GPIO.BCM)

# +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+
# | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
# |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
# |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
# |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 0 | IN   | TxD     | 15  | 14  |
# |     |     |      0v |      |   |  9 || 10 | 1 | IN   | RxD     | 16  | 15  |
# |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
# |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
# |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
# |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
# |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
# |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
# |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 1 | IN   | CE0     | 10  | 8   |
# |     |     |      0v |      |   | 25 || 26 | 1 | IN   | CE1     | 11  | 7   |
# |     |     |         |      |   |    ||    |   |      |         |     |     |
# |     |     |         |      |   |  BELOW   |   |      |         |     |     |
# |     |     | USED BY JARVIS PROGRAM TO CONTROL RELAYS |         |     |     |
# |     |     |         |      |   |    ||    |   |      |         |     |     |
# |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
# |   5 |  21 | GPIO.21 |   IN | 0 | 29 || 30 |   |      | 0v      |     |     |
# |   6 |  22 | GPIO.22 |   IN | 0 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
# |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
# |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
# |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
# |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
# +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+

#  5 rows
rows = [2,3,4,17,27]

# 9 columns
columns = [22,10,14,15,18,23,24,25,8]

current_row = 0

def trigger_input(column):
    global current_row
    print "Input triggered from row: %s and column: %s" % (current_row, column)
    keyboard.write("azerty")

# INIT
# 5 rows x 9 columns = 45 keys matrix

# Columns are output
for row in rows:
    GPIO.setup(row, GPIO.OUT)

# Rows are input with pull-up
for column in columns:
    GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(column, GPIO.RISING, callback=trigger_input, bouncetime=100)

try:
    while True:
        for row in rows:
            # Write 1
            GPIO.output(row, 1)
            current_row = row
            print current_row
            # Sleep 100 ms
            sleep(0.1)

            # Write 0 to release column
            GPIO.output(row, 0)
finally:
    GPIO.cleanup()