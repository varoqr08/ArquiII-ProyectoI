class Lines_Memory:

    position = 0
    positionBin = 0
    state = ' '
    owner = ' '
    data = '0'

    def __init__(self, position):
        self.position = position
        self.positionBin = bin(position)

    def setOwner(self, state, owner):
        self.state = state
        self.owner = owner

    def setLine(self, state, owner, data):
        self.state = state
        self.owner = owner
        self.data = data

