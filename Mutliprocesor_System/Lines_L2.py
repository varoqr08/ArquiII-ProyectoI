

import threading

class Lines_L2(threading.Thread):
    
    #Atributos
    state =  ' '
    owner = ' '
    data = ' '
    direction = 0
    directionBin = 0
    number = 0

    #Constructor
    def __init__(self, number, state, direction, data):
        self.number = number
        self.state = state
        self.direction = direction
        self.directionBin = bin(direction)
        self.data = data

    #Editar la linea de la cache
    def setLine(self, state, direction, data, owner):
        self.state = state
        self.direction = direction
        self.directionBin = bin(direction)
        self.owner = owner
        self.data = data

    #Obtener el estado de la linea
    def getState(self):
        return self.state

