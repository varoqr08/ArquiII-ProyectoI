from multiprocesador import Core
import threading
import time 
import numpy as np
import random
from L1 import L1
from BusAux import BusAux
import logging

class asociate(threading.Thread):
    number_asociate = 0
    core0 = Core('',0,0,L1,L1,L1,L1,BusAux,BusAux)
    core1 = Core('',0,0,L1,L1,L1,L1,BusAux,BusAux)

    def __init__(self, number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1):
        self.number_asociate = number_asociate
        threading.Thread.__init__(self, name=number_asociate, target=asociate.initCores, args=(self,number_asociate,main_memory,cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1,))
        
    
    def initCores(self, number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1):
        #Invocacion de los Cores
        self.core0 = Core('P0',number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1)
        self.core1 = Core('P1',number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1)

        self.core0.start()
        self.core1.start()
