from base64 import b32encode, b32decode
import random
import sys

BEGIN = 50
END = 100

#Вычисление публичного и приватного ключа, а также длины алфавита
def generate_keys():
    #Получение массива простых чисел в диапазоне [BEGIN; END]
    primes = eratosthenes(BEGIN, END)

    #Получение двух случайных различных чисел из массива    
    i, j = random_two_nums(len(primes))
    p, q = primes[i], primes[j]

    #Длина алфавита
    N = p * q

    #Функция Эйлера
    Fi = (p - 1) * (q - 1)

    #Открытый ключ вычисляется как взаимно простое число с Fi
    E = find_coprime(Fi, len(primes))

    #Вычисление закрытого ключа
    _, D, _ = xgcd(E, Fi)

    #Корректировка значения (по кольцу)
    if D < 0:
        D += Fi

    return E, D, N

#Решето Эратосфена для получения списка простых чисел в диапазоне [a; b]
def eratosthenes(a, b):
    start_arr = list(range(b + 1))
    start_arr[1] = 0

    for i in start_arr:
        if i > 1:
            for j in range(2 * i, len(start_arr), i):
                start_arr[j] = 0
    
    sieve = []
    for i in range(a, b):
        x = start_arr[i]
        if x != 0:
            sieve.append(x)
    
    return sieve

#Получение двух случайных различных чисел в диапазоне от 0 до n - 1
def random_two_nums(n):
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)

    while y == x:
        y = random.randint(0, n - 1)

    return x, y

#Вычисление взаимно простого числа к p
def find_coprime(p, n):
    x = random.randint(0, n - 1)
    while (gcd(p, x) != 1):
        x = random.randint(0, n - 1)
    return x

#Алгоритм Евклида
def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b

#Расширенный алгоритм Евклида
def xgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = xgcd(b % a, a)
    return (gcd, y - (b // a) * x, x)

#Быстрое возведение в степень
def fast_pow(a, b):
    if b == 0:
        return 1
    if b == -1:
        return 1. / a
    
    p = fast_pow(a, b // 2)
    p *= p

    if b % 2:
        p *= a
        
    return p

#Шифрование (единичное) 
def encrypt(char_code, key, N):
    return fast_pow(char_code, key) % N

#Шифрование всего сообщения
def encrypt_string(string, Key, N):
    result = ""
    for char in string:
        current_char = encrypt(ord(char), Key, N)
        result += chr(current_char)
    return result

def main():
    filename = sys.argv[1]

    f = open(filename, 'rb')

    data = f.read()
    data = b32encode(data)

    f.close()

    E, D, N = generate_keys()

    enc_res = encrypt_string(data.decode("ascii"), E, N)
    dec_res = b32decode(encrypt_string(enc_res, D, N))

    e = open("enc_" + filename, 'w')
    d = open("dec_" + filename, 'wb')

    e.write(enc_res)
    d.write(dec_res)

    e.close()
    d.close()

if __name__ == "__main__":
    main()