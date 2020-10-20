import threading
from threading import Thread, Lock
import time 
import numpy as np
import random
from L1 import L1
import queue
from control_L1 import Control_L1
from control_L2 import Control_L2
import logging

mutex = Lock()

#Clase core
class Core(threading.Thread):

    #Atributos no definidos
    operation = ''
    memory = ''
    data = ''
    core = ''
    chip = 0
    instruction = ''


    #Constructor
    def __init__(self, core, chip, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21):
        threading.Thread.__init__(self, name=core, target=Core.instruction_generator, args=(self, main_memory,cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21, core, chip,))
        self.core = core
        self.chip = chip
         #Definicion de los LOG
        logging.basicConfig(filename='LOG.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


        
    def instruction_generator(self, main_memory,cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21,core, chip):
        
        
        #Contador
        counter = 0
        #print(memory)
        data_write = ''

        control = Control_L1()
        control_L2 = Control_L2()

       

        #Generador de instrucciones
        while True:
        
            #Distribucion binomial para las instrucciones
            distribution = np.random.binomial(10,0.5)%3

            #Distribucion binomial para la direcciones de memoria
            memory = np.random.binomial(20,0.5)%16
            aux_memory = memory

            #mutex.acquire()

            #Instruccion de lectura
            if(distribution==0):
                self.operation = 'READ'
                self.memory = bin(memory)
                self.instruction = str(self.core) + ','+str(self.chip)+': '+self.operation+' '+str(self.memory)
                print('Se lanza la instruccion '+str(self.core) + ','+str(self.chip)+': '+self.operation+' '+str(self.memory))
                logging.info('Se lanza la instruccion '+str(self.core) + ','+str(self.chip)+': '+self.operation+' '+str(self.memory))
                control.read(control_L2, aux_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21,  main_memory, self.core, self.chip) 
                counter += 1    

            #Instruccion de escritura
            elif(distribution==2):
                for x in range(8):
                    data_write += random.choice('ABCDEF123456789')
                self.operation = 'WRITE'
                self.memory = bin(memory)
                self.data = data_write
                self.instruction = str(self.core) + ','+str(self.chip)+': '+self.operation+' '+str(self.memory)+'; '+self.data
                print('Se lanza la instruccion '+str(self.core) + ','+str(self.chip)+': '+self.operation+' '+str(self.memory)+'; '+self.data)
                logging.info('Se lanza la instruccion '+str(self.core) + ','+str(self.chip)+': '+self.operation+' '+str(self.memory)+'; '+self.data)
                control.write(control_L2, aux_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_L20, cache_L21, main_memory,  self.core, self.chip, self.data)
                data_write = ''
                #counter += 1 
                
                
 
            #Instruccion de CALC
            else:
                self.operation = 'CALC'
                self.instruction = str(self.core) + ','+str(self.chip)+': '+self.operation
                print('Se lanza la instruccion '+str(self.core) + ','+str(self.chip)+': '+self.operation)
                logging.info('Se lanza la instruccion '+str(self.core) + ','+str(self.chip)+': '+self.operation)
                time.sleep(3)
                
                
        #print(self.core + ','+str(self.chip))
            time.sleep(1)
            #mutex.release()
