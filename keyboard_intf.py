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
# |   2 |   8 |   SDA.1 |  OUT | 0 |  3 || 4  |   |      | 5V      |     |     |
# |   3 |   9 |   SCL.1 |  OUT | 0 |  5 || 6  |   |      | 0v      |     |     |
# |   4 |   7 | GPIO. 7 |  OUT | 0 |  7 || 8  | 0 | PU   | TxD     | 15  | 14  |
# |     |     |      0v |      |   |  9 || 10 | 0 | PU   | RxD     | 16  | 15  |
# |  17 |   0 | GPIO. 0 |  OUT | 0 | 11 || 12 | 0 | PU   | GPIO. 1 | 1   | 18  |
# |  27 |   2 | GPIO. 2 |  OUT | 0 | 13 || 14 |   |      | 0v      |     |     |
# |  22 |   3 | GPIO. 3 |   PU | 0 | 15 || 16 | 0 | PU   | GPIO. 4 | 4   | 23  |
# |     |     |    3.3v |      |   | 17 || 18 | 0 | PU   | GPIO. 5 | 5   | 24  |
# |  10 |  12 |    MOSI |   PU | 0 | 19 || 20 |   |      | 0v      |     |     |
# |   9 |  13 |    MISO |   PU | 0 | 21 || 22 | 0 | PU   | GPIO. 6 | 6   | 25  |
# |  11 |  14 |    SCLK |   PU | 0 | 23 || 24 | 0 | PU   | CE0     | 10  | 8   |
# |     |     |      0v |      |   | 25 || 26 | 0 | PU   | CE1     | 11  | 7   |
# |     |     |         |      |   |    ||    |   |      |         |     |     |
# |     |     |         |      |   |  BELOW   |   |      |         |     |     |
# |     |     | USED BY JARVIS PROGRAM TO CONTROL RELAYS |         |     |     |
# |     |     |         |      |   |    ||    |   |      |         |     |     |
# |   0 |  30 |   SDA.0 | RELAY| 1 | 27 || 28 | 1 | RELAY| SCL.0   | 31  | 1   |
# |   5 |  21 | GPIO.21 | RELAY| 0 | 29 || 30 |   |      | 0v      |     |     |
# |   6 |  22 | GPIO.22 | RELAY| 0 | 31 || 32 | 0 | RELAY| GPIO.26 | 26  | 12  |
# |  13 |  23 | GPIO.23 | RELAY| 0 | 33 || 34 |   |      | 0v      |     |     |
# |  19 |  24 | GPIO.24 | RELAY| 0 | 35 || 36 | 0 | RELAY| GPIO.27 | 27  | 16  |
# |  26 |  25 | GPIO.25 | RELAY| 0 | 37 || 38 | 0 | RELAY| GPIO.28 | 28  | 20  |
# |     |     |      0v |      |   | 39 || 40 | 0 | RELAY| GPIO.29 | 29  | 21  |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
# +-----+-----+---------+------+---+---Pi 3---+---+------+---------+-----+-----+

#  5 rows
rows = [2,3,4,17,27]

# 12 columns
columns = [22,10,9,11,14,15,18,23,24,25,8,7]

# list keys
keymap = []
keymap.append("$|1 é|2 \"|3 '|4 (|5 -|6 è|7 _|8 ç|9 à|& =|+ )|°")
keymap.append("a z e r t y u i o p ACCENT")
keymap.append("q s d f g h j k l m ù|%")
keymap.append("w x c v b n ,|? ;|. :|/ !|§")
keymap.append("SHIFT SPACE CAPS BACK_SPACE")

if len(keymap) != len(rows):
  raise Exception('Keymap length differs from rows length')

keys = []
for index, row in enumerate(rows):
  current_keymap_row = keymap[index]
  
  # Split on space
  split_chars = current_keymap_row.split(' ')
  
  if len(split_chars) > len(columns):
    raise Exception('Keymap row is greater than column length')
  
  for indexColumn, column in enumerate(columns):
    current_chars = split_chars[indexColumn]
    
    lower_char = ''
    upper_char = ''
    
    if '|' in current_chars:
      # First char = "lower" case
      # Second char = "upper" case
      (lower_char, upper_char) = current_chars.split('|')
    elif len(current_chars) == 0:
      lower_char = current_chars
      upper_char = current_chars.upper()
    # Specials chars
    elif current_chars == "ACCENT":
      lower_char = '^'
      upper_char = '¨'
    elif current_chars == "SHIFT":
      lower_char = 'shift'
      upper_char = 'shift'
    elif current_chars == "CAPS":
      lower_char = 'caps lock'
      upper_char = 'caps lock'
    elif current_chars == "BACK_SPACE":
      lower_char = 'backspace'
      upper_char = 'backspace'
    
    keys[row][column]['lower'] = lower_char
    keys[row][column]['upper'] = upper_char

print keys

current_row = 0

def trigger_input(column):
    global keys
    global current_row
    print "Input triggered from row: %s and column: %s" % (current_row, column)
    keyboard.write(keys[current_row][column])

# INIT
# 5 rows x 12 columns = 60 keys matrix

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