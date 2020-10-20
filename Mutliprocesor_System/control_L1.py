import threading
import time 
import numpy as np
import random
from memory import Memory
from L1 import L1
from threading import Thread, Lock
from control_BusAux import Control_BusAux
import logging

class Control_L1(threading.Thread):

    bus = ' '


    def __init__(self):
        self


    def read(self, controlBusAux, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, memory, core, asociate):

        logging.info('Busca el dato en la cache  L1 '+str(core)+','+str(asociate))
        #Controlador de caches L1
        
        #Asignacion de caches a utilizar
        if (asociate == 0):
            if (core == 'P0'):
                cache_request =  cache_process00
                cache_recive = cache_process01
            else:
                cache_request =  cache_process01
                cache_recive = cache_process00
        else:
            if (core == 'P0'):
                cache_request =  cache_process10
                cache_recive = cache_process11
            else:
                cache_request =  cache_process11
                cache_recive = cache_process10
                
        owner = ''
        line_change = direc_mem%2
        ##################################  Logica de Reads entre L1's  ############################
    

        #Acierta la posicion de memoria en cache
        if (cache_request.lines[line_change].direction == direc_mem):
            time.sleep(1)
            print('Estaba en cache')

            #Caso en el que la linea esta en invalido
            if (cache_request.lines[line_change].state == 'I'):
                #Mensaje en el bus
                bus = 'Read miss from cahe L1 '+str(cache_request.asociate)+' '+str(cache_request.core)
                logging.info(bus)
                #Verifica los estados de la otra cache
                #Caso en que este M en la otra cache
                if (cache_recive.lines[line_change].state == 'M' and cache_recive.lines[line_change].direction == direc_mem):
                    cache_recive.lines[line_change].state = 'S'
                    owner = ','+cache_recive.core+','+str(cache_recive.asociate)
                
                else:
                    cache_recive.lines[line_change].state = 'E'
                    owner = ','+cache_recive.core+','+str(cache_recive.asociate)
                        
                #Llamada al control de BusAux en caso invalido
                controlBusAux.read(direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, core, memory, owner)

            #Caso en el que la linea esta en Compartido o Modificado
            else:
                bus = 'Read Hit '+str(cache_request.asociate)+' '+str(cache_request.core)
                logging.info(bus)
                return None
            
        #No Acierta la posicion de memoria en cache
        else:
            bus = 'Read miss from cahe L1 '+str(cache_request.asociate)+' '+str(cache_request.core)
            logging.info(bus)
            #Verifica los estados de la otra cache
            if (cache_recive.lines[line_change].state == 'M' and cache_recive.lines[line_change].direction == direc_mem):
                cache_recive.lines[line_change].state = 'S'
                owner = ','+cache_recive.core+','+str(cache_recive.asociate)
            controlBusAux.read(direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, core, memory, owner)
        


##########################Escribir en las L1

    def write(self, controlBusAux, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, memory, core, asociate, data):
        logging.info('Peticion de escritura generada en la cache L1 '+str(core)+','+str(asociate))
        time.sleep(1)
        #Asignacion de caches a utilizar
        if (asociate == 0):
            if (core == 'P0'):
                cache_request =  cache_process00
                cache_recive = cache_process01
            else:
                cache_request =  cache_process01
                cache_recive = cache_process00
        else:
            if (core == 'P0'):
                cache_request =  cache_process10
                cache_recive = cache_process11
            else:
                cache_request =  cache_process11
                cache_recive = cache_process10
                
        owner = ''
        line_change = direc_mem%2

        #Escritura en caches y en memoria

        bus = 'Write Miss from cahe L1 '+str(cache_request.asociate)+' '+str(cache_request.core)
        logging.info(bus)
        #Caso en que este M en la otra cache
        if ((cache_recive.lines[line_change].state == 'M' or cache_recive.lines[line_change].state == 'S') and cache_recive.lines[line_change].direction == direc_mem):
            cache_recive.lines[line_change].state = 'I'
            owner = ','+cache_recive.core+','+str(cache_recive.asociate)
      
        controlBusAux.write(direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, core, memory, owner, data)

       


            