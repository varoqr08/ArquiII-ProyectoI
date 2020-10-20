
import threading
import time 
import numpy as np
import random
from Lines_L2 import Lines_L2
import threading


class L2(threading.Thread):

    #Lineas de memoria caché
    chip = 0
    core = 'P0'
    line0 = Lines_L2(0,'I',0,'0')
    line1 = Lines_L2(1,'I',0,'0')
    line2 = Lines_L2(2,'I',0,'0')
    line3 = Lines_L2(3,'I',0,'0')
    
    lines = [line0, line1, line2, line3]

    def __init__(self, chip):
        self.chip = chip
        self.line0 = Lines_L2(0,'I',0,'0')
        self.line1 = Lines_L2(1,'I',0,'0')
        self.line2 = Lines_L2(2,'I',0,'0')
        self.line3 = Lines_L2(3,'I',0,'0')
        
        self.lines = [self.line0, self.line1, self.line2, self.line3]

    def write(self, line, owner, direc, data, state):
        line.setLine(state, direc, data, owner )

