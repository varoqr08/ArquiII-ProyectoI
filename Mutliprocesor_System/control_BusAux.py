from threading import Thread, Lock
import threading
import time 
import logging

class Control_BusAux(threading.Thread):
    bus = ''

    def __init__(self):
        self

    #READ 
    def read(self, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, core, memory, owner):
        time.sleep(3)
        logging.info('Busca el dato en la cache  BusAux '+str(asociate))
        global aux_owner 
        global memory_owner

        ## Asignacion de las caches que se necesitan
        if(asociate == 0):
            cache_request =  cache_processBusAux0
            cache_recive = cache_processBusAux1
            check_cache0 = cache_process10
            check_cache1 = cache_process11

            if(core == 'P0'):
                cache_write = cache_process00
            else:
                cache_write = cache_process01
        else:
            cache_request =  cache_processBusAux1
            cache_recive = cache_processBusAux0
            check_cache0 = cache_process00
            check_cache1 = cache_process01

            if(core == 'P0'):
                cache_write = cache_process10
            else:
                cache_write = cache_process11

        search_lineBusAux = direc_mem%4
        search_lineL1 = direc_mem%2

        aux_owner = ''
        memory_owner = 'C'+str(asociate)
        

        #Caso de que este el dato en la cache BusAux ACIERTOS
        if(cache_request.lines[direc_mem%4].direction == direc_mem):
            
            #La linea esta Invalida de la Cache BusAux
            if(cache_request.lines[direc_mem%4].state == 'I'):
                bus = 'Read miss from cache BusAux '+str(cache_request.asociate)
                logging.info(bus)
                logging.info('Verifica si la cache BusAux '+str(cache_request.asociate)+' tiene el dato para cambiar el estado si es necesario')
                #Busca en la otra cache BusAux
                if(direc_mem == cache_recive.lines[search_lineBusAux].direction and cache_recive.lines[search_lineBusAux].state == 'M'):
                        
                    #Cambia el estado de la caché BusAux del otro asociate
                    cache_recive.lines[search_lineBusAux].state = 'S'
                    #Cambia el estado de la caché BusAux del otro asociate
                    for i in range(len(cache_recive.lines[search_lineBusAux].owner)-1):
                        if (cache_recive.lines[search_lineBusAux].owner[i] == ';'):
                            cache_recive.lines[search_lineBusAux].owner = cache_recive.lines[search_lineBusAux].owner[0:i]
                    cache_recive.lines[search_lineBusAux].owner += ';E'
                    aux_owner = ';E'
                    memory_owner += ', C'+str(cache_recive.asociate)

                    #Modifica el estado de las L1
                    if(check_cache0.lines[search_lineL1].direction == direc_mem):
                        check_cache0.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineBusAux].state = 'S'

                    elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                        check_cache1.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineBusAux].state = 'S'
   
                    else:
                        cache_recive.lines[search_lineBusAux].state = 'I'
                else:
                    cache_recive.lines[search_lineBusAux].state = 'E'
                    aux_owner = ''
                    
                time.sleep(5)
                #Busca en memoria Principal
                #Escribe en Cache BusAux
                logging.info('Buscando en memoria el dato en la posicion '+str(direc_mem))
                logging.info('Linea de memoria en la que esta el dato, agregando el estado y los dueños: ')
                cache_request.write(cache_request.lines[search_lineBusAux], core+','+str(asociate)+owner+aux_owner, direc_mem, memory.lines[direc_mem].data, 'S')
                memory.lines[direc_mem].setOwner(cache_request.lines[search_lineBusAux].state, memory_owner)
                #Logs
                logging.info('            '+str(memory.lines[direc_mem].positionBin)+'  '+str(memory.lines[direc_mem].state)+'  '+str(memory.lines[direc_mem].owner)+'  '+str(memory.lines[direc_mem].data))
                logging.info('Escribe en cache BusAux '+str(asociate))
                logging.info('            '+str(cache_request.lines[search_lineBusAux].number)+'  '+str(cache_request.lines[search_lineBusAux].state)+'  '+str(cache_request.lines[search_lineBusAux].owner)+'  '+str(cache_request.lines[search_lineBusAux].directionBin)+'  '+str(cache_request.lines[search_lineBusAux].data))
                
                #Escribe en Cache L1
                cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
                logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.asociate))
                logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
                time.sleep(6)

            else:
                if(direc_mem == cache_recive.lines[search_lineBusAux].direction and (cache_recive.lines[search_lineBusAux].state == 'M' or cache_recive.lines[search_lineBusAux].state == 'S' )):
                    bus = 'Read hit from cache BusAux '+str(cache_request.asociate)
                    logging.info(bus)
                    logging.info('Verifica si la cache BusAux '+str(cache_request.asociate)+' tiene el dato para cambiar el estado si es necesario')    
                    #Cambia el estado de la caché BusAux del otro asociate
                    cache_recive.lines[search_lineBusAux].state = 'S'
                    #Cambia el estado de la caché BusAux del otro asociate
                    for i in range(len(cache_recive.lines[search_lineBusAux].owner)-1):
                        if (cache_recive.lines[search_lineBusAux].owner[i] == ';'):
                            cache_recive.lines[search_lineBusAux].owner = cache_recive.lines[search_lineBusAux].owner[0:i]
                    cache_recive.lines[search_lineBusAux].owner += ';E'
                    aux_owner = ';E'
                    memory_owner += ', C'+str(cache_recive.asociate)

                    #Modifica el estado de las L1
                    if(check_cache0.lines[search_lineL1].direction == direc_mem):
                        check_cache0.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineBusAux].state = 'S'

                    elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                        check_cache1.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineBusAux].state = 'S'
   
                    else:
                        cache_recive.lines[search_lineBusAux].state = 'I'

                else:
                    aux_owner = ''
                    
                
                #Cambia el owner
                cache_request.lines[direc_mem%4].owner = core+','+str(asociate)+owner+aux_owner
                cache_request.lines[direc_mem%4].state = 'S'

                logging.info('Linea en cache BusAux '+str(asociate)+' leida, con el cambio de owner si fuera necesario')
                logging.info('            '+str(cache_request.lines[search_lineBusAux].number)+'  '+str(cache_request.lines[search_lineBusAux].state)+'  '+str(cache_request.lines[search_lineBusAux].owner)+'  '+str(cache_request.lines[search_lineBusAux].directionBin)+'  '+str(cache_request.lines[search_lineBusAux].data))

                #Escribe en Cache L1
                cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
                logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.asociate))
                logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
                time.sleep(6)
                   
        #NO se encuentra la direccion de memoria en La cache BusAux
        else:
            
            bus = 'Read miss from cache BusAux '+str(cache_request.asociate)
            logging.info(bus)
            logging.info('Verifica si la cache BusAux '+str(cache_request.asociate)+' tiene el dato para cambiar el estado si es necesario')

            #Busca en la otra cache BusAux
            if(direc_mem == cache_recive.lines[search_lineBusAux].direction and (cache_recive.lines[search_lineBusAux].state == 'M' or cache_recive.lines[search_lineBusAux].state == 'S' )):
                    
                cache_recive.lines[search_lineBusAux].state = 'S'
                #Cambia el estado de la caché BusAux del otro asociate
                for i in range(len(cache_recive.lines[search_lineBusAux].owner)-1):
                    if (cache_recive.lines[search_lineBusAux].owner[i] == ';'):
                        cache_recive.lines[search_lineBusAux].owner = cache_recive.lines[search_lineBusAux].owner[0:i]
                cache_recive.lines[search_lineBusAux].owner += ';E'
                aux_owner = ';E'
                memory_owner += ', C'+str(cache_recive.asociate)

                #Modifica el estado de las L1
                if(check_cache0.lines[search_lineL1].direction == direc_mem):
                    check_cache0.lines[search_lineL1].state = 'S'
                    cache_recive.lines[search_lineBusAux].state = 'S'

                elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                    check_cache1.lines[search_lineL1].state = 'S'
                    cache_recive.lines[search_lineBusAux].state = 'S'

                else:
                    cache_recive.lines[search_lineBusAux].state = 'I'

            else:
                aux_owner = ''
                
            time.sleep(5)
            #Busca en memoria Principal
            #Escribe en Cache BusAux
            logging.info('Buscando en memoria el dato en la posicion '+str(direc_mem))
            logging.info('Linea de memoria en la que esta el dato, agregando el estado y los dueños: ')
            cache_request.write(cache_request.lines[search_lineBusAux], core+','+str(asociate)+owner+aux_owner, direc_mem, memory.lines[direc_mem].data, 'S')
            memory.lines[direc_mem].setOwner(cache_request.lines[search_lineBusAux].state, memory_owner)
            #Logs
            logging.info('            '+str(memory.lines[direc_mem].positionBin)+'  '+str(memory.lines[direc_mem].state)+'  '+str(memory.lines[direc_mem].owner)+'  '+str(memory.lines[direc_mem].data))
            logging.info('Escribe en cache BusAux '+str(asociate))
            logging.info('            '+str(cache_request.lines[search_lineBusAux].number)+'  '+str(cache_request.lines[search_lineBusAux].state)+'  '+str(cache_request.lines[search_lineBusAux].owner)+'  '+str(cache_request.lines[search_lineBusAux].directionBin)+'  '+str(cache_request.lines[search_lineBusAux].data))
            
            #Escribe en Cache L1
            cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
            logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.asociate))
            logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
            time.sleep(6)

######################################################################################################################################################################################           
    
    
    #Control de lectura entre la caches L1, BusAux y memoria principal
    def write(self, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, core, memory, owner, data):
        logging.info('Peticion de escritura que llega a la cache BusAux '+str(asociate))
        global aux_owner 
        global memory_owner
        time.sleep(3)

        aux_owner = ''

        ## Asignacion de las caches que se necesitan
        if(asociate == 0):
            cache_request =  cache_processBusAux0
            cache_recive = cache_processBusAux1
            check_cache0 = cache_process10
            check_cache1 = cache_process11

            if(core == 'P0'):
                cache_write = cache_process00
            else:
                cache_write = cache_process01
        else:
            cache_request =  cache_processBusAux1
            cache_recive = cache_processBusAux0
            check_cache0 = cache_process00
            check_cache1 = cache_process01

            if(core == 'P0'):
                cache_write = cache_process10
            else:
                cache_write = cache_process11

        search_lineBusAux = direc_mem%4
        search_lineL1 = direc_mem%2

        memory_owner = 'C'+str(asociate)

        
        bus = 'Write miss from cache BusAux'+str(cache_request.asociate)
        logging.info(bus)
        logging.info('Verifica si la cache BusAux '+str(cache_request.asociate)+' tiene el dato para cambiar el estado si es necesario')
        #Busca en la otra cache BusAux
        if(direc_mem == cache_recive.lines[search_lineBusAux].direction and (cache_recive.lines[search_lineBusAux].state == 'M' or cache_recive.lines[search_lineBusAux].state == 'DS')):
                
            #Cambia el estado de la caché BusAux del otro asociate
            cache_recive.lines[search_lineBusAux].state = 'I'
            for i in range(len(cache_recive.lines[search_lineBusAux].owner)-1):
                if (cache_recive.lines[search_lineBusAux].owner[i] == ';'):
                    cache_recive.lines[search_lineBusAux].owner = cache_recive.lines[search_lineBusAux].owner[0:i]
            cache_recive.lines[search_lineBusAux].owner += ';E'
            aux_owner = ';E'
            memory_owner += ', C'+str(cache_recive.asociate)

            #Modifica el estado de las L1
            if(check_cache0.lines[search_lineL1].direction == direc_mem):
                check_cache0.lines[search_lineL1].state = 'I'

            elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                check_cache1.lines[search_lineL1].state = 'I'

            else:
                None
        else:
            aux_owner = ''
            
        time.sleep(5)
        #Escribe en Cache L1
        cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, data, 'M')
        
        #Escribe en Cache BusAux
        cache_request.write(cache_request.lines[search_lineBusAux], core+','+str(asociate)+owner+aux_owner, direc_mem, data, 'M')
        
        #Escribe en memoria
        memory.setLine(direc_mem, cache_request.lines[search_lineBusAux].state, memory_owner, data)

        logging.info('Linea en memoria en la cual se escribe el nuevo valor')   
        logging.info('            '+str(memory.lines[direc_mem].positionBin)+'  '+str(memory.lines[direc_mem].state)+'  '+str(memory.lines[direc_mem].owner)+'  '+str(memory.lines[direc_mem].data))

        logging.info('Linea en cache BusAux '+str(asociate)+' que se escribe, con su respectivo owner')
        logging.info('            '+str(cache_request.lines[search_lineBusAux].number)+'  '+str(cache_request.lines[search_lineBusAux].state)+'  '+str(cache_request.lines[search_lineBusAux].owner)+'  '+str(cache_request.lines[search_lineBusAux].directionBin)+'  '+str(cache_request.lines[search_lineBusAux].data))

        logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.asociate))
        logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
    

