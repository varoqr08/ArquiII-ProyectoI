from threading import Thread, Lock
import threading
import time 
import logging

class Control_L2(threading.Thread):
    bus = ''

    def __init__(self):
        self

    #READ 
    def read(self, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processL20, cache_processL21, chip, core, memory, owner):
        time.sleep(3)
        logging.info('Busca el dato en la cache  L2 '+str(chip))
        global aux_owner 
        global memory_owner

        ## Asignacion de las caches que se necesitan
        if(chip == 0):
            cache_request =  cache_processL20
            cache_recive = cache_processL21
            check_cache0 = cache_process10
            check_cache1 = cache_process11

            if(core == 'P0'):
                cache_write = cache_process00
            else:
                cache_write = cache_process01
        else:
            cache_request =  cache_processL21
            cache_recive = cache_processL20
            check_cache0 = cache_process00
            check_cache1 = cache_process01

            if(core == 'P0'):
                cache_write = cache_process10
            else:
                cache_write = cache_process11

        search_lineL2 = direc_mem%4
        search_lineL1 = direc_mem%2

        aux_owner = ''
        memory_owner = 'C'+str(chip)
        

        #Caso de que este el dato en la cache L2 ACIERTOS
        if(cache_request.lines[direc_mem%4].direction == direc_mem):
            
            #La linea esta Invalida de la Cache L2
            if(cache_request.lines[direc_mem%4].state == 'I'):
                bus = 'Read miss from cache L2 '+str(cache_request.chip)
                logging.info(bus)
                logging.info('Verifica si la cache L2 '+str(cache_request.chip)+' tiene el dato para cambiar el estado si es necesario')
                #Busca en la otra cache L2
                if(direc_mem == cache_recive.lines[search_lineL2].direction and cache_recive.lines[search_lineL2].state == 'M'):
                        
                    #Cambia el estado de la caché L2 del otro chip
                    cache_recive.lines[search_lineL2].state = 'S'
                    #Cambia el estado de la caché L2 del otro chip
                    for i in range(len(cache_recive.lines[search_lineL2].owner)-1):
                        if (cache_recive.lines[search_lineL2].owner[i] == ';'):
                            cache_recive.lines[search_lineL2].owner = cache_recive.lines[search_lineL2].owner[0:i]
                    cache_recive.lines[search_lineL2].owner += ';E'
                    aux_owner = ';E'
                    memory_owner += ', C'+str(cache_recive.chip)

                    #Modifica el estado de las L1
                    if(check_cache0.lines[search_lineL1].direction == direc_mem):
                        check_cache0.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineL2].state = 'S'

                    elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                        check_cache1.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineL2].state = 'S'
   
                    else:
                        cache_recive.lines[search_lineL2].state = 'I'
                else:
                    aux_owner = ''
                    
                time.sleep(5)
                #Busca en memoria Principal
                #Escribe en Cache L2
                logging.info('Buscando en memoria el dato en la posicion '+str(direc_mem))
                logging.info('Linea de memoria en la que esta el dato, agregando el estado y los dueños: ')
                cache_request.write(cache_request.lines[search_lineL2], core+','+str(chip)+owner+aux_owner, direc_mem, memory.lines[direc_mem].data, 'S')
                memory.lines[direc_mem].setOwner(cache_request.lines[search_lineL2].state, memory_owner)
                #Logs
                logging.info('            '+str(memory.lines[direc_mem].positionBin)+'  '+str(memory.lines[direc_mem].state)+'  '+str(memory.lines[direc_mem].owner)+'  '+str(memory.lines[direc_mem].data))
                logging.info('Escribe en cache L2 '+str(chip))
                logging.info('            '+str(cache_request.lines[search_lineL2].number)+'  '+str(cache_request.lines[search_lineL2].state)+'  '+str(cache_request.lines[search_lineL2].owner)+'  '+str(cache_request.lines[search_lineL2].directionBin)+'  '+str(cache_request.lines[search_lineL2].data))
                
                #Escribe en Cache L1
                cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
                logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.chip))
                logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
                time.sleep(6)

            else:
                if(direc_mem == cache_recive.lines[search_lineL2].direction and (cache_recive.lines[search_lineL2].state == 'M' or cache_recive.lines[search_lineL2].state == 'S' )):
                    bus = 'Read hit from cache L2 '+str(cache_request.chip)
                    logging.info(bus)
                    logging.info('Verifica si la cache L2 '+str(cache_request.chip)+' tiene el dato para cambiar el estado si es necesario')    
                    #Cambia el estado de la caché L2 del otro chip
                    cache_recive.lines[search_lineL2].state = 'S'
                    #Cambia el estado de la caché L2 del otro chip
                    for i in range(len(cache_recive.lines[search_lineL2].owner)-1):
                        if (cache_recive.lines[search_lineL2].owner[i] == ';'):
                            cache_recive.lines[search_lineL2].owner = cache_recive.lines[search_lineL2].owner[0:i]
                    cache_recive.lines[search_lineL2].owner += ';E'
                    aux_owner = ';E'
                    memory_owner += ', C'+str(cache_recive.chip)

                    #Modifica el estado de las L1
                    if(check_cache0.lines[search_lineL1].direction == direc_mem):
                        check_cache0.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineL2].state = 'S'

                    elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                        check_cache1.lines[search_lineL1].state = 'S'
                        cache_recive.lines[search_lineL2].state = 'S'
   
                    else:
                        cache_recive.lines[search_lineL2].state = 'I'

                else:
                    aux_owner = ''
                    
                
                #Cambia el owner
                cache_request.lines[direc_mem%4].owner = core+','+str(chip)+owner+aux_owner
                cache_request.lines[direc_mem%4].state = 'S'

                logging.info('Linea en cache L2 '+str(chip)+' leida, con el cambio de owner si fuera necesario')
                logging.info('            '+str(cache_request.lines[search_lineL2].number)+'  '+str(cache_request.lines[search_lineL2].state)+'  '+str(cache_request.lines[search_lineL2].owner)+'  '+str(cache_request.lines[search_lineL2].directionBin)+'  '+str(cache_request.lines[search_lineL2].data))

                #Escribe en Cache L1
                cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
                logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.chip))
                logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
                time.sleep(6)
                   
        #NO se encuentra la direccion de memoria en La cache L2
        else:
            
            bus = 'Read miss from cache L2 '+str(cache_request.chip)
            logging.info(bus)
            logging.info('Verifica si la cache L2 '+str(cache_request.chip)+' tiene el dato para cambiar el estado si es necesario')

            #Busca en la otra cache L2
            if(direc_mem == cache_recive.lines[search_lineL2].direction and (cache_recive.lines[search_lineL2].state == 'M' or cache_recive.lines[search_lineL2].state == 'S' )):
                    
                cache_recive.lines[search_lineL2].state = 'S'
                #Cambia el estado de la caché L2 del otro chip
                for i in range(len(cache_recive.lines[search_lineL2].owner)-1):
                    if (cache_recive.lines[search_lineL2].owner[i] == ';'):
                        cache_recive.lines[search_lineL2].owner = cache_recive.lines[search_lineL2].owner[0:i]
                cache_recive.lines[search_lineL2].owner += ';E'
                aux_owner = ';E'
                memory_owner += ', C'+str(cache_recive.chip)

                #Modifica el estado de las L1
                if(check_cache0.lines[search_lineL1].direction == direc_mem):
                    check_cache0.lines[search_lineL1].state = 'S'
                    cache_recive.lines[search_lineL2].state = 'S'

                elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                    check_cache1.lines[search_lineL1].state = 'S'
                    cache_recive.lines[search_lineL2].state = 'S'

                else:
                    cache_recive.lines[search_lineL2].state = 'I'

            else:
                aux_owner = ''
                
            time.sleep(5)
            #Busca en memoria Principal
            #Escribe en Cache L2
            logging.info('Buscando en memoria el dato en la posicion '+str(direc_mem))
            logging.info('Linea de memoria en la que esta el dato, agregando el estado y los dueños: ')
            cache_request.write(cache_request.lines[search_lineL2], core+','+str(chip)+owner+aux_owner, direc_mem, memory.lines[direc_mem].data, 'S')
            memory.lines[direc_mem].setOwner(cache_request.lines[search_lineL2].state, memory_owner)
            #Logs
            logging.info('            '+str(memory.lines[direc_mem].positionBin)+'  '+str(memory.lines[direc_mem].state)+'  '+str(memory.lines[direc_mem].owner)+'  '+str(memory.lines[direc_mem].data))
            logging.info('Escribe en cache L2 '+str(chip))
            logging.info('            '+str(cache_request.lines[search_lineL2].number)+'  '+str(cache_request.lines[search_lineL2].state)+'  '+str(cache_request.lines[search_lineL2].owner)+'  '+str(cache_request.lines[search_lineL2].directionBin)+'  '+str(cache_request.lines[search_lineL2].data))
            
            #Escribe en Cache L1
            cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
            logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.chip))
            logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
            time.sleep(6)

######################################################################################################################################################################################           
    
    
    #Control de lectura entre la caches L1, L2 y memoria principal
    def write(self, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processL20, cache_processL21, chip, core, memory, owner, data):
        logging.info('Peticion de escritura que llega a la cache L2 '+str(chip))
        global aux_owner 
        global memory_owner
        time.sleep(3)

        aux_owner = ''

        ## Asignacion de las caches que se necesitan
        if(chip == 0):
            cache_request =  cache_processL20
            cache_recive = cache_processL21
            check_cache0 = cache_process10
            check_cache1 = cache_process11

            if(core == 'P0'):
                cache_write = cache_process00
            else:
                cache_write = cache_process01
        else:
            cache_request =  cache_processL21
            cache_recive = cache_processL20
            check_cache0 = cache_process00
            check_cache1 = cache_process01

            if(core == 'P0'):
                cache_write = cache_process10
            else:
                cache_write = cache_process11

        search_lineL2 = direc_mem%4
        search_lineL1 = direc_mem%2

        memory_owner = 'C'+str(chip)

        
        bus = 'Write miss from cache L2'+str(cache_request.chip)
        logging.info(bus)
        logging.info('Verifica si la cache L2 '+str(cache_request.chip)+' tiene el dato para cambiar el estado si es necesario')
        #Busca en la otra cache L2
        if(direc_mem == cache_recive.lines[search_lineL2].direction and (cache_recive.lines[search_lineL2].state == 'M' or cache_recive.lines[search_lineL2].state == 'DS')):
                
            #Cambia el estado de la caché L2 del otro chip
            cache_recive.lines[search_lineL2].state = 'I'
            for i in range(len(cache_recive.lines[search_lineL2].owner)-1):
                if (cache_recive.lines[search_lineL2].owner[i] == ';'):
                    cache_recive.lines[search_lineL2].owner = cache_recive.lines[search_lineL2].owner[0:i]
            cache_recive.lines[search_lineL2].owner += ';E'
            aux_owner = ';E'
            memory_owner += ', C'+str(cache_recive.chip)

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
        
        #Escribe en Cache L2
        cache_request.write(cache_request.lines[search_lineL2], core+','+str(chip)+owner+aux_owner, direc_mem, data, 'M')
        
        #Escribe en memoria
        memory.setLine(direc_mem, cache_request.lines[search_lineL2].state, memory_owner, data)

        logging.info('Linea en memoria en la cual se escribe el nuevo valor')   
        logging.info('            '+str(memory.lines[direc_mem].positionBin)+'  '+str(memory.lines[direc_mem].state)+'  '+str(memory.lines[direc_mem].owner)+'  '+str(memory.lines[direc_mem].data))

        logging.info('Linea en cache L2 '+str(chip)+' que se escribe, con su respectivo owner')
        logging.info('            '+str(cache_request.lines[search_lineL2].number)+'  '+str(cache_request.lines[search_lineL2].state)+'  '+str(cache_request.lines[search_lineL2].owner)+'  '+str(cache_request.lines[search_lineL2].directionBin)+'  '+str(cache_request.lines[search_lineL2].data))

        logging.info('Escribe en cache L1 '+str(cache_write.core)+','+str(cache_write.chip))
        logging.info('            '+str(cache_write.lines[direc_mem%2].number)+'  '+str(cache_write.lines[direc_mem%2].state)+'  '+str(cache_write.lines[direc_mem%2].data))
    

