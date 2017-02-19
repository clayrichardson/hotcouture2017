import bibliopixel
#causes frame timing information to be output
bibliopixel.log.setLogLevel(bibliopixel.log.INFO)

from random import randint
from bibliopixel.colors import color_scale

#Load driver for the AllPixel
from bibliopixel.drivers.serial_driver import *
from bibliopixel.drivers.visualizer import DriverVisualizer

#set number of pixels & LED type here
#driver = DriverSerial(num = 300, type = LEDTYPE.APA102)
#visualizer = DriverVisualizer(width=2, height=150)

#load the LEDStrip class
from bibliopixel.led import *

#strip = LEDStrip(visualizer, threadedUpdate = False, masterBrightness = 150)


#load channel test animation
from bibliopixel.animation import BaseStripAnim

def rand_color():
    #return (color_scale((randint(0,255),randint(0,255),randint(0,255)), randint(0,255)))
    return (color_scale((randint(0,255),randint(0,255),randint(0,255)), 255))

class RainbowCycle(BaseStripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=-1):
        super(RainbowCycle, self).__init__(led, start, end)

    def step(self, amt = 1):
        for i in range(self._size):
            #color = (i * (384 / self._size) + self._step) % 384
            #c = colors.wheel_helper(i, self._size, self._step)
            c = colors.hue_helper(i, self._size, self._step)
            self._led.set(self._start + i, c)

        self._step += amt
        if self._step == 20: self._step = 0

rows = []
number = 10

row_start_start = [[0,10], [55,56], [110, 120], [165, 175]]

#print map(lambda x: x, map(lambda y: y + 1, row_start_start))
print [map(lambda y: y + 220, x) for x in row_start_start]


print row_start_start

side0_start = [[0,10], [55,56], [110, 120], [165, 175]]
side1_start = [map(lambda y: y + 220, x) for x in side0_start]
side2_start = [map(lambda y: y + 220, x) for x in side1_start]

for i in range(number):
    left0 = range(side0_start[0][0], side0_start[0][1])
    middle0 = range(side0_start[1][0], side0_start[1][1])
    right0 = range(side0_start[2][0], side0_start[2][1])

    left1 = range(side1_start[0][0], side1_start[0][1])
    middle1 = range(side1_start[1][0], side1_start[1][1])
    right1 = range(side1_start[2][0], side1_start[2][1])

    left2 = range(side2_start[0][0], side2_start[0][1])
    middle2 = range(side2_start[1][0], side2_start[1][1])
    right2 = range(side2_start[2][0], side2_start[2][1])

    rows.append(left0 + middle0 + right0 + left1 + middle1 + right1 + left2 + middle2 + right2)

    print "append: %s, %s, %s" % (left0, middle0, right0)

    reduction = side0_start[0][1] - side0_start[0][0]
    increase = side0_start[1][1] - side0_start[1][0]

    side0_start[0][0] += reduction
    side0_start[0][1] += reduction - 1

    side0_start[1][0] += increase
    side0_start[1][1] += increase + 1

    side0_start[2][0] += reduction
    side0_start[2][1] += reduction - 1

    side1_start[0][0] += reduction
    side1_start[0][1] += reduction - 1

    side1_start[1][0] += increase
    side1_start[1][1] += increase + 1

    side1_start[2][0] += reduction
    side1_start[2][1] += reduction - 1

    side2_start[0][0] += reduction
    side2_start[0][1] += reduction - 1

    side2_start[1][0] += increase
    side2_start[1][1] += increase + 1

    side2_start[2][0] += reduction
    side2_start[2][1] += reduction - 1

for i in range(number):
    top0 = range(side0_start[3][0], side0_start[3][1])
    top1 = range(side1_start[3][0], side1_start[3][1])
    top2 = range(side2_start[3][0], side2_start[3][1])
    print "append top: %s" % top0
    rows.append(top0 + top1 + top2)

    reduction = side0_start[3][1] - side0_start[3][0]
    side0_start[3][0] += reduction
    side0_start[3][1] += reduction - 1

    side1_start[3][0] += reduction
    side1_start[3][1] += reduction - 1

    side2_start[3][0] += reduction
    side2_start[3][1] += reduction - 1

rows.reverse()


# rows.append(range(0,10) + range(55,55) + range(110, 120))
# rows.append(range(10, 19) + range(56,58) + range(120, 129))
# rows.append(range(19, 27) + range(58,61) + range(129, 137))

class BottomUp(BaseStripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=-1):
        super(BottomUp, self).__init__(led, start, end)

    def step(self, amt = 1):
        print self._step
        self._led.all_off()
        for pixel in rows[self._step]:
            self._led.set(pixel, rand_color())

        self._step += amt
        if self._step == 20: self._step = 0


class CrazyRainbowBottomUp(BaseStripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=-1):
        super(CrazyRainbowBottomUp, self).__init__(led, start, end)

    def step(self, amt = 1):

        for i in range(20):
            #color = (i * (384 / self._size) + self._step) % 384
            #c = colors.wheel_helper(i, self._size, self._step)
            for pixel in rows[i]:
                c = colors.hue_helper(i, 20, self._step)
                self._led.set(self._start + pixel, c)

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow

class RainbowBottomUp(BaseStripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=-1):
        super(RainbowBottomUp, self).__init__(led, start, end)

    def step(self, amt = 1):
        for i in range(20):
            #color = (i * (384 / self._size) + self._step) % 384
            #c = colors.wheel_helper(i, self._size, self._step)
            for pixel in rows[i]:
                c = colors.hue_helper(i, 20, self._step)
                if 1 == randint(1,15):
                    c = (randint(1,255),randint(1,255),randint(1,255))
                    #c = (c[0], c[1], c[2])
                elif 1 == randint(1,5):
                    c = (0,0,0)
                else:
                    c = colors.hue_helper(i, 20, self._step)
                
                self._led.set(self._start + pixel, c)

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow

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

# while True:

#     try:
#         anim.run()
#     except Exception as e:
#         print "problem: %s" % e

#     except KeyboardInterrupt:
#         #Ctrl+C will exit the animation and turn the LEDs offs
#         # strip.all_off()
#         break
