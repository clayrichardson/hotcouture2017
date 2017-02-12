import Adafruit_BBIO.GPIO as GPIO
import time
import signal
import sys
import multiprocessing
import random

pins = [7, 8, 9, 10, 11, 12, 14, 16]
processes = []

for pin in pins:
    GPIO.setup("P8_%s" % pin, GPIO.OUT)
    GPIO.output("P8_%s" % pin, GPIO.HIGH)

def signal_handler(signal, frame):
    print '\nCaught interrupt, cleaning up...'
    for process in processes:
        process.terminate()
    for pin in pins:
        GPIO.output("P8_%s" % pin, GPIO.HIGH)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def pin_process(pin):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    while 1:
        rand_time = random.random()
        rand_time = rand_time * 2
        s_time = random.uniform(0.01, 0.1)
        print 's_time: %s' % s_time
        print '%s sleeping for %s' % (pin, rand_time)
        time.sleep(rand_time)
        print 'flashing pin: %s' % pin
        for i in range(3):
            GPIO.output("P8_%s" % pin, GPIO.HIGH)
            time.sleep(s_time)
            GPIO.output("P8_%s" % pin, GPIO.LOW)
            time.sleep(s_time)
            GPIO.output("P8_%s" % pin, GPIO.HIGH)


def flash_pin(pin):
    for i in range(3):
        GPIO.output("P8_%s" % pin, GPIO.HIGH)
        time.sleep(s_time)
        GPIO.output("P8_%s" % pin, GPIO.LOW)
        time.sleep(s_time)
        GPIO.output("P8_%s" % pin, GPIO.HIGH)

for pin in pins:
    print 'trying pin: %s' % pin
    process = multiprocessing.Process(target=pin_process, args=(pin,))
    process.start()
    processes.append(process)

while 1:
    print 'main process sleeping'
    time.sleep(5)
