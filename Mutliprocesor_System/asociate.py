from multiprocesador import Group
import threading
import random
from L1 import L1
import time 
import numpy as np
from BusAux import BusAux


class asociate(threading.Thread):
    number_asociate = 0
    group0 = Group('',0,0,L1,L1,L1,L1,BusAux,BusAux)
    group1 = Group('',0,0,L1,L1,L1,L1,BusAux,BusAux)

    def __init__(self, number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1):
        self.number_asociate = number_asociate
        threading.Thread.__init__(self, name=number_asociate, target=asociate.initGroups, args=(self,number_asociate,main_memory,cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1,))
        
    
    def initGroups(self, number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1):
        self.group0 = Group('P0',number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1)
        self.group1 = Group('P1',number_asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1)
        self.group0.start()
        self.group1.start()
