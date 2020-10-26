import threading
import time 
import numpy as np
import random
from Lines_L1 import Lines_L1
import threading


class L1(threading.Thread):
    asociate = 0
    group = 'P0'
    line0 = Lines_L1(0,'I',0,'0')
    line1 = Lines_L1(1,'I',0,'0')
    line2 = Lines_L1(2,'I',0,'0')
    line3 = Lines_L1(3,'I',0,'0')
    lines = [line0, line1, line2, line3]

    def __init__(self, asociate, group):
        self.asociate = asociate
        self.group = group
        self.line0 = Lines_L1(0,'I',0,'0')
        self.line1 = Lines_L1(1,'I',0,'0')
        self.line2 = Lines_L1(2,'I',0,'0')
        self.line3 = Lines_L1(3,'I',0,'0')
        self.lines = [self.line0, self.line1, self.line2, self.line3]


    def writeOnLine(self, line, direc, data, state):
        line.setLine(state, direc, data)

        


    
