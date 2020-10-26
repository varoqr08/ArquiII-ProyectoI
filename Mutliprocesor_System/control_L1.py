import threading
import time 
import numpy as np
import random
from memory import Memory
from L1 import L1
from threading import Thread, Lock
from DataBus import DataBus
#import logging

class Control_L1(threading.Thread):
    def __init__(self):
        self

    def read(self, controlBusAux, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, memory, group, asociate):

        #Asignacion de caches a utilizar
        if (asociate == 0):
            if (group == 'P0'):
                cache_request =  cache_process00
                cache_recive = cache_process01
            else:
                cache_request =  cache_process01
                cache_recive = cache_process00
        else:
            if (group == 'P0'):
                cache_request =  cache_process10
                cache_recive = cache_process11
            else:
                cache_request =  cache_process11
                cache_recive = cache_process10
                
        owner = ''
        line_change = direc_mem%2


        ##############################################################

        #Encuentra la posicion de memoria en cache
        if (cache_request.lines[line_change].direction == direc_mem):
            time.sleep(2)
            print('Estaba en cache')

            #Caso en el que la linea esta en invalido
            if (cache_request.lines[line_change].state == 'I'):
                #Mensaje en el bus
                if (cache_recive.lines[line_change].state == 'M' and cache_recive.lines[line_change].direction == direc_mem):
                    cache_recive.lines[line_change].state = 'S'
                    owner = ','+cache_recive.group+','+str(cache_recive.asociate)
                
                else:
                    cache_recive.lines[line_change].state = 'E'
                    owner = ','+cache_recive.group+','+str(cache_recive.asociate)
                        
                #Llamada al control de BusAux en caso invalido
                controlBusAux.read(direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, group, memory, owner)

            #Caso en el que la linea esta en Compartido o Modificado
            else:
                return None
            
        #No Acierta la posicion de memoria en cache
        else:
            #Verifica los estados de la otra cache
            if (cache_recive.lines[line_change].state == 'M' and cache_recive.lines[line_change].direction == direc_mem):
                cache_recive.lines[line_change].state = 'S'
                owner = ','+cache_recive.group+','+str(cache_recive.asociate)
            controlBusAux.read(direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, group, memory, owner)
        


##############################################

    def write(self, controlBusAux, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, memory, group, asociate, data):
        time.sleep(2)
        #Asignacion de caches a utilizar
        if (asociate == 0):
            print("HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(group)
            if (group == 'P0'):
                cache_request =  cache_process00
                cache_recive = cache_process01
                print("MECAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            else:
                cache_request =  cache_process01
                cache_recive = cache_process00
                print("MECAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2")
        else:
            print("HOLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(group)
            if (group == 'P0'):
                cache_request =  cache_process10
                cache_recive = cache_process11
                print("MECAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA3")
            else:
                cache_request =  cache_process11
                cache_recive = cache_process10
                print("MECAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4")
                
        owner = ''
        line_change = direc_mem%2

        #Escritura en caches y en memoria
        if ((cache_recive.lines[line_change].state == 'M' or cache_recive.lines[line_change].state == 'S') and cache_recive.lines[line_change].direction == direc_mem):
            cache_recive.lines[line_change].state = 'I'
            owner = ','+cache_recive+','+str(cache_recive.asociate)
      
        controlBusAux.write(direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, group, memory, owner, data)
