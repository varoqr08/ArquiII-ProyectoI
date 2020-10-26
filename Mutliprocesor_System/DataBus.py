from threading import Thread, Lock
import threading
import time 

class DataBus(threading.Thread):
    bus = ''

    def __init__(self):
        self

    #READ 
    def read(self, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, group, memory, owner):
        time.sleep(4)
        global aux_owner 
        global memory_owner

        ## Asignacion de las caches que se necesitan
        if(asociate == 0):
            cache_request =  cache_processBusAux0
            cache_recive = cache_processBusAux1
            check_cache0 = cache_process10
            check_cache1 = cache_process11

            if(group == 'P0'):
                cache_write = cache_process00
                memory_owner = 'P1'
            else:
                cache_write = cache_process01
                memory_owner = 'P2'
        else:
            cache_request =  cache_processBusAux1
            cache_recive = cache_processBusAux0
            check_cache0 = cache_process00
            check_cache1 = cache_process01

            if(group == 'P0'):
                cache_write = cache_process10
                memory_owner = 'P3'
            else:
                cache_write = cache_process11
                memory_owner = 'P4'

        search_lineBusAux = direc_mem%4
        search_lineL1 = direc_mem%2

        aux_owner = ''
        #memory_owner = 'C'+str(asociate)
        

        #Caso de que este el dato en la cache BusAux ACIERTOS
        if(cache_request.lines[direc_mem%4].direction == direc_mem):
            
            #La linea esta Invalida de la Cache BusAux
            if(cache_request.lines[direc_mem%4].state == 'I'):
                if(direc_mem == cache_recive.lines[search_lineBusAux].direction and cache_recive.lines[search_lineBusAux].state == 'M'):
                        
                    #Cambia el estado de la caché BusAux del otro asociate
                    cache_recive.lines[search_lineBusAux].state = 'S'
                    memory_owner += ', (B'+str( cache_recive.asociate)+')'

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
                
                cache_request.write(cache_request.lines[search_lineBusAux], group + ',' + str(asociate)+owner+aux_owner, direc_mem, memory.lines[direc_mem].data, 'S')
                memory.lines[direc_mem].setOwner(cache_request.lines[search_lineBusAux].state, memory_owner)
               
                #Escribe en Cache L1
                cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
                time.sleep(4)

            else:
                if(direc_mem == cache_recive.lines[search_lineBusAux].direction and (cache_recive.lines[search_lineBusAux].state == 'M' or cache_recive.lines[search_lineBusAux].state == 'S' )):
                    cache_recive.lines[search_lineBusAux].state = 'S'

                    memory_owner += ', (B'+str( cache_recive.asociate)+')'

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
                cache_request.lines[direc_mem%4].owner = group+','+str(asociate)+owner+aux_owner
                cache_request.lines[direc_mem%4].state = 'S'

                #Escribe en Cache L1
                cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
                
                time.sleep(5)
                   
        #NO se encuentra la direccion de memoria BusAux
        else:
          
           #Busca en la otra cache BusAux
            if(direc_mem == cache_recive.lines[search_lineBusAux].direction and (cache_recive.lines[search_lineBusAux].state == 'M' or cache_recive.lines[search_lineBusAux].state == 'S' )):
                    
                cache_recive.lines[search_lineBusAux].state = 'S'

                memory_owner += ', (B'+str(cache_recive.asociate)+')'

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


################################################################################################################



            #Busca en memoria Principal

            cache_request.write(cache_request.lines[search_lineBusAux], group+','+str(asociate)+owner+aux_owner, direc_mem, memory.lines[direc_mem].data, 'S')
            memory.lines[direc_mem].setOwner(cache_request.lines[search_lineBusAux].state, memory_owner)
            
            #Escribe en Cache L1
            cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, cache_request.lines[direc_mem%4].data, 'S')
            time.sleep(4)

######################################################################################################################################################################################           
    
    
    #Control de lectura entre la caches L1, BusAux y memoria principal
    def write(self, direc_mem, cache_process00, cache_process01, cache_process10, cache_process11, cache_processBusAux0, cache_processBusAux1, asociate, group, memory, owner, data):
        global aux_owner 
        global memory_owner
        time.sleep(4)

        aux_owner = ''

        ## Asignacion de cache
        if(asociate == 0):
            cache_request =  cache_processBusAux0
            cache_recive = cache_processBusAux1
            check_cache0 = cache_process10
            check_cache1 = cache_process11

            if(group== 'P0'):
                cache_write = cache_process00
                memory_owner = 'P1'
            else:
                cache_write = cache_process01
                memory_owner = 'P2'
        else:
            cache_request =  cache_processBusAux1
            cache_recive = cache_processBusAux0
            check_cache0 = cache_process00
            check_cache1 = cache_process01

            if(group== 'P0'):
                cache_write = cache_process10
                memory_owner = 'P3'
            else:
                cache_write = cache_process11
                memory_owner = 'P4'

        search_lineBusAux = direc_mem%4
        search_lineL1 = direc_mem%2

        #memory_owner = 'C'+str(asociate)

        
        if(direc_mem == cache_recive.lines[search_lineBusAux].direction and (cache_recive.lines[search_lineBusAux].state == 'M' or cache_recive.lines[search_lineBusAux].state == 'S')):
                
            #Cambia el estado de la caché BusAux del otro asociate
            cache_recive.lines[search_lineBusAux].state = 'I'
            memory_owner += ', (B'+str( cache_recive.asociate)+')'

            #Modifica el estado de las L1
            if(check_cache0.lines[search_lineL1].direction == direc_mem):
                check_cache0.lines[search_lineL1].state = 'I'

            elif(check_cache1.lines[search_lineL1].direction == direc_mem):
                check_cache1.lines[search_lineL1].state = 'I'

            else:
                None
        else:
            aux_owner = ''
            
        time.sleep(4)
        
        #Escribe en Cache L1
        cache_write.writeOnLine(cache_write.lines[direc_mem%2],  direc_mem, data, 'M')
        
        #Escribe en Cache BusAux
        cache_request.write(cache_request.lines[search_lineBusAux], group+','+str(asociate)+owner+aux_owner, direc_mem, data, 'M')
        
        #Escribe en memoria
        memory.setLine(direc_mem, cache_request.lines[search_lineBusAux].state, memory_owner, data)
