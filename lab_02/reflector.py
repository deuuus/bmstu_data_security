from common import *

class Reflector:
    def __init__(self):
        self.map = [None for i in range(SYMBOL_COUNT)]
        temp_alph = list(range(SYMBOL_COUNT))[:]
        for i in range(len(self.map)):
            if self.map[i] == None:
                code = random.choice(temp_alph)
                while code == i:
                    code = random.choice(temp_alph)
                temp_alph.pop(temp_alph.index(code))
                temp_alph.pop(temp_alph.index(i))
                self.map[i] = code
                self.map[code] = i
		   
    def reflect(self, index):
        return self.map[index]