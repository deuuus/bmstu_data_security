from turtle import left
from des_tables import *

def permutation(bits_block: str, table: list):
    result = ""
    for i in table:
        result += bits_block[i-1]
    return result

def shift_left(s: str, n: int):
    for _ in range(n):
        s = s[1:] + s[:1]
    return s

#Генерация раундовых ключей.
def generate_round_keys(key: str): #На вход подается 64-битный ключ.
    round_keys = []
    #Ключ подвергается перестановке B (key_replace_table).
    key = permutation(key, key_replace_table)
    #Делим ключ на левую и правую половину.
    left_half = key[:28]
    right_half = key[28:]
    #Генерируем 16 раундовых ключей.
    for i in range(16):
        #Каждая из половин подвергается сдвигу влево (halfs_table).
        n = halfs_table[i]
        left_half = shift_left(left_half, n)
        right_half = shift_left(right_half, n)
        #После сдвигов половины объединяются.
        round_key = left_half + right_half
        #Затем применяется сжимающая перестановка CP (56 бит -> 48 бит).
        #Получаем очередной раундовый ключ.
        round_key = permutation(round_key, key_compression_table)
        round_keys.append(round_key)
    return round_keys

#Шифрование.
def encrypt(message: str, round_keys: list): #На вход подается 64-битное сообщение и 16 48-битных раундовых ключей
    #Сообщение подвергается начальной перестановке IP.
    message = permutation(message, initial_permutation)
    #Делим сообщение на левую и правую половину.
    left_half = message[:32]
    right_half = message[32:]
    #Выполняем 16 раундов.
    for i in range(16):
        #Новая левая половина получается из старой правой.
        new_left_half = right_half
        #Новая правая получается из старой левой и XOR из функции Фейстеля
        new_right_half = str_xor(left_half, feistel_cipher(right_half, round_keys[i]))

        left_half = new_left_half
        right_half = new_right_half
    
    message = left_half + right_half
    message = permutation(message, initial_permutation_back)
    return message

#Расшифровка.
def decrypt(message: str, round_keys: list): #На вход подается 64-битное сообщение и 16 48-битных раундовых ключей
    #Сообщение подвергается начальной перестановке IP.
    message = permutation(message, initial_permutation)
    #Делим сообщение на левую и правую половину.
    left_half = message[:32]
    right_half = message[32:]
    #Выполняем 16 раундов.
    for i in range(16):
        #Новая левая половина получается из старой правой.
        new_right_half = left_half
        #Новая правая получается из старой левой и XOR из функции Фейстеля
        new_left_half = str_xor(right_half, feistel_cipher(left_half, round_keys[i]))

        left_half = new_left_half
        right_half = new_right_half
    
    message = left_half + right_half
    message = permutation(message, initial_permutation_back)
    return message

#Шифр Фейстеля.
def feistel_cipher(message: str, round_key: str): #Получает на вход половину данных (32 бита) и раундовый ключ (сжимался до 48 бит).
    #Делаем расширяющую перестановку для блока данных, чтобы он тоже стал 48-битным.
    message = permutation(message, extend_permutation)
    #XOR ключа и данных
    res = str_xor(message, round_key)
    #Разбиваем 48 бит на 8 частей
    parts = []
    for i in range(0, 48, 6):
        parts.append(res[i:i+6])
    #Замены с использованием s-блоков (48 бит->32 бита).
    res = ""
    for i in range(8):
        row = int(parts[i][0] + parts[i][5], 2)
        column = int(parts[i][1:5], 2)
        change = s_blocks[i][row][column]
        change = bin(change)[2:]
        while len(change) < 4:
            change = '0' + change
        res += change
    #Применяется завершающая перестановка.
    res = permutation(res, end_permutation)
    return res

def str_xor(s1: str, s2: str):
    result = ""
    for i in range(len(s1)):
        x, y = int(s1[i], 2), int(s2[i], 2)
        result += str(x ^ y)
    return result

