import bibliopixel
from bibliopixel.led import *
from random import randint
from bibliopixel.colors import color_scale
from bibliopixel.drivers.serial_driver import *
from bibliopixel.animation import BaseStripAnim, BaseMatrixAnim, AnimationQueue
from bibliopixel.drivers.visualizer import DriverVisualizer
import bibliopixel.gamma as gamma
from bibliopixel.util import genVector
from multiprocessing import Process, Value, Array
import time

# (1) Fade upwards to the top of the strand
# (2) Jazz time
# (3) Reverse of (1)


#causes frame timing information to be output
#bibliopixel.log.setLogLevel(bibliopixel.log.INFO)

#Driver, Strip, and Matrix
driver = DriverSerial(num=236, type=LEDTYPE.APA102)
#visualizer = DriverVisualizer(width=2, height=118)

strip = LEDStrip(driver, threadedUpdate=True, masterBrightness=150)
# matrix = LEDMatrix(driver, 
#                    width=2, 
#                    height=118,
#                    serpentine=False)
queue = AnimationQueue(strip)

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

    def wave_range(self, start, peak, step):
        main = [i for i in range(start, peak+1, step)]
        return main# + [i for i in reversed(main[0:len(main)-1])]

    def __init__(self, led):
        super(DNA, self).__init__(led)
   
        led.all_off()

        #Levels for brightness fade
        self._levels = self.wave_range(30, 255, 70)
     
        #Base pair colors
        self.colors = [cRed, cOrange, cBlue, cLime]
        self._level_count = len(self._levels)
        self._color_count = len(self.colors)

        self._l_step = 0;


    def step(self, amt=1):

        c_index = (self._step / self._level_count) % self._color_count
        l_index = (self._l_step % self._level_count)

        color = colors.color_scale(self.colors[(self._step) % self._color_count], self._levels[l_index])
        
        self._led.set(self._step, color)

        self._l_step += 1;
        #self._step += amt
        if(self._l_step >= self._level_count):
            self._l_step = 0
            self._step += amt



from stringanimation import RainbowBottomUp

anim = DNA(strip)
rainbow = [colors.Red, colors.Orange, colors.Yellow, colors.Green, colors.Blue, colors.Purple]
#anim = ColorFade(strip, rainbow, step=2)
#anim2 = ColorFade(strip, rainbow, step=40)
anim3 = RainbowBottomUp(strip)
#anim = DNAMatrix(matrix)

queue.addAnim(anim, max_steps=1180, fps=30)
queue.addAnim(anim3)

while True:

    try:
        queue.run()
    except Exception as e:
        print "problem: %s" % e
    except KeyboardInterrupt:
        #Ctrl+C will exit the animation and turn the LEDs offs
        strip.all_off()
        break
