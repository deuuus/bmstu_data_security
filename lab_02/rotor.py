from common import *

class Rotor:
    def __init__(self):
        self.offset = 0
        self.full = False
        self.map = list(range(SYMBOL_COUNT))
        self.start_map = self.map
        random.shuffle(self.map)
        
    def reset(self):
        self.offset = 0
        self.map = self.start_map
    
    def forward(self, index):
        return self.map.index(index)
		   
    def backwards(self, index):
        return self.map[index]
		
    def rotate(self):
        self.map = self.map[1:] + self.map[:1]
        self.offset += 1
        if self.offset == SYMBOL_COUNT:
            self.offset = 0
            self.full = True
        else:
            self.full = False