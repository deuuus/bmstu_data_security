import random
import sys

from common import *
from rotor import *
from reflector import *
from enigma import *

def main():
    src_filename = sys.argv[1]
    src_file = open(src_filename, "rb")
        
    rotors = [0] * ROTORS_COUNT
    for i in range(ROTORS_COUNT):
        rotors[i] = Rotor()
        
    reflector = Reflector()

    enigma = Enigma(rotors, reflector)
  
    enc_file = open("encrypted_" + src_filename, "wb")
        
    lines = src_file.read()
    
    src_file.close()
    
    encrypted_data = enigma.encrypt_data(lines)

    enc_file.write(encrypted_data)
    enc_file.close()
    
    data_str = 'Input text:\n%s\n' % (lines.decode("latin-1") )
    input_file = open("input_" + src_filename, "wb")
    input_file.write(lines)

    #print(data_str)
    
    enc_str = 'Encrypted text:\n%s\n' % (encrypted_data.decode("latin-1"))
    #print(enc_str)
    
    enc_file = open("encrypted_" + src_filename, "rb")
    dec_file = open("decrypted_" + src_filename, "wb")
    
    enigma.reset()
    
    lines = enc_file.read()
    enc_file.close()

    decrypted_data = enigma.encrypt_data(lines)
    dec_file.write(decrypted_data)
    dec_file.close()
    
    dec_str = 'Decrypted text:\n%s\n' % (decrypted_data.decode("latin-1") )
    #print(dec_str)
    
if __name__ == "__main__":
    main()