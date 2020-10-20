import threading

class Lines_L1(threading.Thread):
    
    #Atributos
    state =  ' '
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
    def setLine(self, state, direction, data):
        self.state = state
        self.direction = direction
        self.directionBin = bin(direction)
        self.data = data

    #Obtener el estado de la linea
    def getState(self):
        return self.state

