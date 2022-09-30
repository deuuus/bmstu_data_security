from common import *
from struct import pack

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

class Enigma:
    def __init__(self, rotors, reflector):
        self.rotors = rotors
        self.reflector = reflector
        
    def reset(self):
        for rotor in self.rotors:
            rotor.reset()  
               
    def encrypt_symbol(self, symbol):
        encrypted_symbol = symbol
        n = len(self.rotors)
        
        for rotor in self.rotors:
            encrypted_symbol = rotor.forward(encrypted_symbol)
        
        encrypted_symbol = self.reflector.reflect(encrypted_symbol)   
        
        for rotor in self.rotors[::-1]:
            encrypted_symbol = rotor.backwards(encrypted_symbol)
            
        self.rotors[0].rotate()
        for i in range(1, n):
            if self.rotors[i - 1].full:
                self.rotors[i].rotate()
                
        return encrypted_symbol
        
    def encrypt_data(self, data):
        encrypted_data = b''
        for symbol in data:
            encrypted_symbol = self.encrypt_symbol(symbol)
            encrypted_data += pack("B", encrypted_symbol)
        return encrypted_data
        