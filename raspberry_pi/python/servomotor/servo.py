#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Dependencies (Raspbian):
#
#    aptitude install python3-rpi.gpio
#
# Pinout:
#
#     Model A, Model B rev.2:
#                  _ _
#        3.3V    -| V |-    5V
#   (i2c) SDA  2 -|   |-    5V
#   (i2c) SCL  3 -|   |-    GND
#              4 -|   |- 14 TXD (serial)
#         GND    -|   |- 15 RXD (serial)
#             17 -|   |- 18
#             27 -|   |-    GND
#             22 -|   |- 23
#        3.3V    -|   |- 24
#  (spi) MOSI 10 -|   |-    GND
#  (spi) MISO  9 -|   |- 25
#  (spi) SCKL 11 -|   |- 8
#         GND    -|   |- 7
#                  --- 
#
# The GPIO uses 3.3V for all inputs and outputs.
# Any pin with a number next to it can act as a GPIO pin.
#
# Special pins:
# - TXD, RXD = the serial interface
# - SDA, SCL = the I2C interface
# - MOSI, MISO, SCKL = the SPI interface
#
# Warning:
# - Do not put more than 3.3V on any GPIO pin.
# - Do not draw more than 3mA per output.
# - Do not draw more than a total of 50mA from the 3.3V supply pins.
# - Do not draw more than a total of 250mA from the 5V supply pins.

# Warning: you should execute this script as "root" to get the right to handle GPIO pins.

# Inspired by "Recipe 10.1" of the "Raspberry Pi Cookbook" by Simon Monk (ed. Oreilly)

# Move a servomotor on GPIO pin 18.

import RPi.GPIO as gpio
import time

led_pin = 18
sleep_time = 0.01

# "Tower Pro DG92R Micro Servo" (cf. www.adafruit.com/product/169):
# - position 0°: 1.5 ms pulse
# - position +90° (max angle): 2 ms pulse
# - position -90° (min angle): 1 ms pulse
frequency = 100              # Frequency = 100Hz (10ms)
min_duty_cycle = 10          # 1ms (-90°)
max_duty_cycle = 20          # 2ms (+90°)
initial_duty_cycle = 15      # 1.5ms (0°)

def main():
    """Main function"""

    # gpio.setmode: set up numbering mode to use for channels.
    # - gpio.BOARD = use Raspberry Pi board numbers.
    # - gpio.BCM = use  Broadcom GPIO 00..nn numbers.
    gpio.setmode(gpio.BCM)

    gpio.setup(led_pin, gpio.OUT)

    # Create a PWM (Pulse Width Modulation) instance.
    pwm = gpio.PWM(led_pin, frequency)

    # Start software PWM with the given duty cycle (0.0 to 100.0)
    duty_cycle = initial_duty_cycle               # Duty cycle (0.0 to 100.0)
    pwm.start(duty_cycle)

    direction = 1

    while True:
        if duty_cycle <= min_duty_cycle:
            direction = 1
        elif duty_cycle >= max_duty_cycle:
            direction = -1

        duty_cycle += direction
        print(duty_cycle)

        pwm.ChangeDutyCycle(duty_cycle)

        time.sleep(sleep_time)   # Wait 'sleep_time' seconds

    # REM: others useful functions:
    # - pwm.stop()
    # - pwm.ChangeFrequency(frequency)

if __name__ == '__main__':
    main()
