from __future__ import division
import Adafruit_BBIO.GPIO as GPIO
import multiprocessing
import random

import time
import signal
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685
from random import randint

# Uncomment to enable debug output.
import logging
#logging.basicConfig(level=logging.DEBUG)

def signal_handler(signal, frame):

    print '\nCaught interrupt, cleaning up...'
    for process in processes:
        process.terminate()
    for channel in range(10):
        print 'setting channel %s to min' % channel
        pwm.set_pwm(channel, 0, servo_max)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685(busnum=2)


# Configure min and max servo pulse lengths
servo_min = 200  # Min pulse length out of 4096
servo_max = 440  # Max pulse length out of 4096

channels = range(10)
processes = []

pwm.set_pwm_freq(50)

def servo_process(channel):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    while 1:
        sleep_time = random.uniform(0.5, 1)
        value = randint(servo_min, servo_max)
        print '%s sleeping for %s' % (channel, sleep_time)
        time.sleep(sleep_time)
        print 'setting channel %s to %s' % (channel, value)
        pwm.set_pwm(channel, 0, value)

for channel in channels:
    print 'trying channel: %s' % channel
    process = multiprocessing.Process(target=servo_process, args=(channel,))
    process.start()
    processes.append(process)

while 1:
    print 'main process sleeping'
    time.sleep(5)
