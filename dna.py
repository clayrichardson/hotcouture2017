import bibliopixel
from bibliopixel.led import *
from random import randint
from bibliopixel.colors import color_scale
from bibliopixel.drivers.serial_driver import *
from bibliopixel.animation import BaseStripAnim
import bibliopixel.gamma as gamma
from multiprocessing import Process, Value, Array
import time

#causes frame timing information to be output
#bibliopixel.log.setLogLevel(bibliopixel.log.INFO)

#Driver and Strip
driver = DriverSerial(num=300, type=LEDTYPE.APA102, gamma=gamma.APA102)
strip = LEDStrip(driver, threadedUpdate=True, masterBrightness=150)
matrix = LEDMatrix(width=2, height=150, driver, threadedUpdate=True, masterBrightness=150)

#http://www.colourlovers.com/palette/1813691/Art_is_in_my_DNA
cRed = (255,0,96)
cOrange = (255,143,0)
cLime = (205,255,0)
cBlue = (35,216,216)
cGreen = (254,214,0)

def rand_color():
    #return (color_scale((randint(0,255),randint(0,255),randint(0,255)), randint(0,255)))
    return (color_scale((randint(0,255),randint(0,255),randint(0,255)), 255))

class ColorFade(BaseStripAnim):
    """Fill the dots progressively along the strip."""

    def wave_range(self, start, peak, step):
        main = [i for i in range(start, peak+1, step)]
        return main + [i for i in reversed(main[0:len(main)-1])]

    def __init__(self, led, colors, step = 5, start=0, end=-1):
        super(ColorFade, self).__init__(led, start, end)
        self._colors = colors
        self._levels = self.wave_range(30, 255, step)
        self._level_count = len(self._levels)
        self._color_count = len(colors)

    def step(self, amt = 1):
        if self._step > self._level_count * self._color_count:
            self._step = 0

        c_index = (self._step / self._level_count) % self._color_count
        l_index = (self._step % self._level_count)
        color = self._colors[c_index];
        self._led.fill(colors.color_scale(color, self._levels[l_index]), self._start, self._end)

        self._step += amt


class DNA(BaseStripAnim):
    def __init__(self, led, start=0, end=-1):
        super(DNA, self).__init__(led, start, end)

        self._r = Array('i', self._led.numLEDs)
        self._g = Array('i', self._led.numLEDs)
        self._b = Array('i', self._led.numLEDs)
        self._my_step = Value('i', 0) 

        for i in range(self._led.numLEDs):
            self._r[i] = 0
            self._r[i] = 0
            self._r[i] = 0

        p = Process(target=self.fillColor, args=(self._r, self._g, self._b, self._my_step))
        p.start()

    def step(self, amt = 1):

        for i in range(self._led.numLEDs):
            self._led.set(i, (self._r[i], self._g[i], self._b[i]))

        self._step += amt
        self._my_step.value = self._step

    def fillColor(self, r, g, b, step):

        #Creates an array of levels to use for brightness values
        def wave_range(self, start, peak, step):
            main = [i for i in range(start, peak+1, step)]
            return main + [i for i in reversed(main[0:len(main)-1])]

        self._levels = self.wave_range(30, 255, step)

        left_strand = [cRed, cBlue]
        right_strand = [cGreen, cOrange]

        while True:
            for i in range(0,150):
                r[i], g[i], b[i] = my_colors[(step.value + i) % len(my_colors)]
            time.sleep(.5)   

    def fillColor2(self, r, g, b, step):

        my_colors = [green, orange]

        while True:
            for i in range(200, 300):
                r[i], g[i], b[i] = my_colors[(step.value + i) % len(my_colors)]
            time.sleep(1)

    def fillColor3(self, r, g, b, step):

        while True:
            for i in range(100):
                r[i], g[i], b[i] = (0,0,0)
            time.sleep(1)
            for i in range(100):
                r[i], g[i], b[i] = (255,255,255)
            time.sleep(1)

    def fillColor4(self, r, g, b, step):
        i = 0
        while True:
            while i < 300:
                r[i], g[i], b[i] = colors.Red
                time.sleep(1)
                i += 1

#anim = RainbowCycle(strip)
#anim = BottomUp(strip)
#anim = RainbowBottomUp(strip)
#anim = CrazyRainbowBottomUp(strip)
#anim = LarsonScanner(led,color=(255,0,0), tail=25)
#anim = Poops(led)
#anim = MatrixPoops(led)
#anim = MatrixCalibrationTest(led)
#anim = RandMatrix(led)
#anim = FireMatrix(led)

#anim = DNA(strip)
rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]
anim = ColorFade(strip, rainbow)

while True:

    #try:
    anim.run()
    #except Exception as e:
   #    print "problem: %s" % e
    #except KeyboardInterrupt:
        #Ctrl+C will exit the animation and turn the LEDs offs
    #    strip.all_off()
    #    break
