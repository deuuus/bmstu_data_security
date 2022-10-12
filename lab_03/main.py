import sys
import des
from struct import pack

def bytes_to_bits(bytes_arr: bytes):
    bits_arr = ""
    for byte in bytes_arr:
        bits = bin(byte)[2:]
        if len(bits) < 8:
            n = 8 - len(bits)
            for _ in range(n):
                bits = "0" + bits
        bits_arr += bits
    return bits_arr

def bits_to_bytes(bits: str):
    bytes_arr = b''
    for i in range (0, len(bits), 8):
        b = bits[i:i+8]
        bytes_arr += pack("B", int(b, 2))
    return bytes_arr

if __name__ == '__main__':

    filename = sys.argv[1]
    key_filename = sys.argv[2]

    input_file = open(filename, 'rb')
    data = input_file.read()
    bits_arr = bytes_to_bits(data)

    key_file = open(key_filename, 'rb')
    key = key_file.read()
    key_bits = bytes_to_bits(key)

    bytes_arr = bits_to_bytes(bits_arr)

    round_keys = des.generate_round_keys(key_bits)

    temp = ""
    enc_res = ""
    for bit in bits_arr:
        temp += str(bit)
        if len(temp) == 64:
            enc = des.encrypt(temp, round_keys)
            enc_res += enc
            temp = ""

    n = len(temp)
    if 0 < n < 64:
        zeros = 64 - n
        for i in range (zeros):
            temp += "0"
        enc = des.encrypt(temp, round_keys)
        enc_res += enc
    
    temp = ""
    dec_res = ""
    for bit in enc_res:
        temp += str(bit)
        if len(temp) == 64:
            dec = des.decrypt(temp, round_keys)
            dec_res += dec
            temp = ""
        
    zeros = 64 - n
    dec_res = dec_res[:(len(dec_res) - zeros)]

    enc_file = open('enc_' + filename, 'wb')
    enc_file.write(bits_to_bytes(enc_res))

    output_file = open('dec_' + filename, 'wb')
    output_file.write(bits_to_bytes(dec_res))