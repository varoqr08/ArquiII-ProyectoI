import threading
from threading import Thread, Lock
import time 
import random
from L1 import L1
import numpy as np
import queue
from control_L1 import Control_L1
from DataBus import DataBus


class Group(threading.Thread):

    #Atributos iniciales no definidos
    asociate = 0
    instruction = ''
    operation = ''
    data = ''
    group = ''
    memory = ''


    #Constructor
    def __init__(self, group, asociate, main_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1):
        threading.Thread.__init__(self, name=group, target=Group.instruction_generator, args=(self, main_memory,cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1, group, asociate))
        self.asociate = asociate
        self.group = group

        
    def instruction_generator(self, main_memory,cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1,group, asociate):
        
        
        #Contador
        counter = 0

        
        control = Control_L1()
        dataBus = DataBus()
        data_write = ''

        #Generador de instrucciones
        while True:
###########################################################################################
            if(counter == 25):        #CANTIDAD DE ITERACIONES PARA DETENERSE (por procesador)
                break
###########################################################################################

            #Instrucciones
            distribution = np.random.binomial(10,0.5)%3

            #Direcciones de memoria
            memory = np.random.binomial(20,0.5)%16
            aux_memory = memory

            #Instruccion de READ
            if(distribution==0):
                self.operation = 'READ'
                self.memory = bin(memory)
                self.instruction = self.operation+' '+str(self.memory)
                print('Se da la instruccion '+self.operation+' '+str(self.memory))
                control.read(dataBus, aux_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1,  main_memory, self.group, self.asociate) 
                counter += 1    

            #Instruccion de WRITE
            elif(distribution==2):
                i = 0
                while(i<8):
                    data_write += random.choice('ABCDEF123456789')
                    i+=1
                self.operation = 'WRITE'
                self.memory = bin(memory)
                self.data = data_write
                self.instruction = self.operation+' '+str(self.memory)+'; '+self.data
                print('Se da la instruccion '+self.operation+' '+str(self.memory)+'; '+self.data)
                control.write(dataBus, aux_memory, cache_L100, cache_L101, cache_L110, cache_L111, cache_BusAux0, cache_BusAux1, main_memory,  self.group, self.asociate, self.data)
                data_write = ''
                counter += 1 
                
            #Instruccion de CALC
            else:
                self.operation = 'CALC'
                self.instruction = self.operation
                print('Se da la instruccion '+self.operation)
                time.sleep(4)
                counter += 1 

            print("Counter: "+str(counter))
                
                
