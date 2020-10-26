import threading
import numpy as np
import time 
import random
from Lines_BusAux import Lines_BusAux


class BusAux(threading.Thread):

    #Lineas de memoria caché
    asociate = 0
    group = 'P0'
    line0 = Lines_BusAux(0,'I',0,'0')
    line1 = Lines_BusAux(1,'I',0,'0')
    line2 = Lines_BusAux(2,'I',0,'0')
    line3 = Lines_BusAux(3,'I',0,'0')
    
    lines = [line0, line1, line2, line3]

    def __init__(self, asociate):
        self.asociate = asociate
        self.line0 = Lines_BusAux(0,'I',0,'0')
        self.line1 = Lines_BusAux(1,'I',0,'0')
        self.line2 = Lines_BusAux(2,'I',0,'0')
        self.line3 = Lines_BusAux(3,'I',0,'0')
        
        self.lines = [self.line0, self.line1, self.line2, self.line3]

    def write(self, line, owner, direc, data, state):
        line.setLine(state, direc, data, owner )

