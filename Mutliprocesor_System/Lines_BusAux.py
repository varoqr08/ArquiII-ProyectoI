import threading

class Lines_BusAux(threading.Thread):
    #Atributos
    state =  ' '
    owner = ' '
    data = ' '
    direction = 0
    directionBin = 0
    number = 0
    def __init__(self, number, state, direction, data):
        self.number = number
        self.state = state
        self.direction = direction
        self.directionBin = bin(direction)
        self.data = data
    def setLine(self, state, direction, data, owner):
        self.state = state
        self.direction = direction
        self.directionBin = bin(direction)
        self.owner = owner
        self.data = data
    def getState(self):
        return self.state

