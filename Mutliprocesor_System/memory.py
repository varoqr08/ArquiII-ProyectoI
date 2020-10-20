import threading
import time 
import numpy as np
import random
from lines_Memory import Lines_Memory


class Memory:

    #Lineas de memoria principal
    line0 = Lines_Memory(0)
    line1 = Lines_Memory(1)
    line2 = Lines_Memory(2)
    line3 = Lines_Memory(3)
    line4 = Lines_Memory(4)
    line5 = Lines_Memory(5)
    line6 = Lines_Memory(6)
    line7 = Lines_Memory(7)
    line8 = Lines_Memory(8)
    line9 = Lines_Memory(9)
    line10 = Lines_Memory(10)
    line11 = Lines_Memory(11)
    line12 = Lines_Memory(12)
    line13 = Lines_Memory(13)
    line14 = Lines_Memory(14)
    line15 = Lines_Memory(15)

    lines = [line0,line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,line11,line12,line13,line14,line15]

    def __init__(self):
        self.line0 = Lines_Memory(0)
        self.line1 = Lines_Memory(1)
        self.line2 = Lines_Memory(2)
        self.line3 = Lines_Memory(3)
        self.line4 = Lines_Memory(4)
        self.line5 = Lines_Memory(5)
        self.line6 = Lines_Memory(6)
        self.line7 = Lines_Memory(7)
        self.line8 = Lines_Memory(8)
        self.line9 = Lines_Memory(9)
        self.line10 = Lines_Memory(10)
        self.line11 = Lines_Memory(11)
        self.line12 = Lines_Memory(12)
        self.line13 = Lines_Memory(13)
        self.line14 = Lines_Memory(14)
        self.line15 = Lines_Memory(15)

    def setLine(self, line, state, owner, data):
        self.lines[line].setLine(state, owner, data)

