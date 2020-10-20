from multiprocesador import Core
import threading
import time 
import numpy as np
import random
from L1 import L1
from L2 import L2
import logging

class Chip(threading.Thread):
    number_chip = 0
    core0 = Core('',0,0,L1,L1,L1,L1,L2,L2)
    core1 = Core('',0,0,L1,L1,L1,L1,L2,L2)

    def __init__(self, number_chip, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21):
        self.number_chip = number_chip
        threading.Thread.__init__(self, name=number_chip, target=Chip.initCores, args=(self,number_chip,main_memory,cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21,))
        
    
    def initCores(self, number_chip, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21):
        #Invocacion de los Cores
        self.core0 = Core('P0',number_chip, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21)
        self.core1 = Core('P1',number_chip, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21)

        self.core0.start()
        self.core1.start()
