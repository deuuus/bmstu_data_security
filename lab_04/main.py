from base64 import b32encode, b32decode
import random
import sys

BEGIN = 50
END = 100

#Вычисление публичного и приватного ключа, а также длины алфавита.
def generate_keys():
    #Получение массива простых чисел в диапазоне [BEGIN; END].
    primes = eratosthenes(BEGIN, END)

    #Получение двух случайных различных чисел из массива.  
    i, j = random_two_nums(len(primes))
    p, q = primes[i], primes[j]

    #Длина алфавита.
    N = p * q

    #Функция Эйлера.
    Fi = (p - 1) * (q - 1)

    #Открытый ключ вычисляется как взаимно простое число с Fi.
    E = find_coprime(Fi, len(primes))

    #Закрытый ключ D для шифрования вычисляется как решение уравнения (E * D) mod (Fi(N)) = 1.
    #Это обратное число к открытому ключу, но в кольце Fi(N).
    _, D, _ = xgcd(E, Fi)

    #Корректировка значения (по кольцу).
    if D < 0:
        D += Fi

    return E, D, N

#Решето Эратосфена для получения списка простых чисел в диапазоне [a; b].
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

#Получение двух случайных различных чисел в диапазоне от 0 до n - 1.
def random_two_nums(n):
    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)

    while y == x:
        y = random.randint(0, n - 1)

    return x, y

#Вычисление взаимно простого числа к p.
#Два числа называются взаимного простыми по отношению друг к другу, если их наибольший общий делитель равен 1.
def find_coprime(p, n):
    x = random.randint(0, n - 1)
    while (gcd(p, x) != 1):
        x = random.randint(0, n - 1)
    return x

#Алгоритм Евклида: вычисление наибольшего общего делителя.
def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b

#Расширенный алгоритм Евклида. Решение соотношения Безу: НОД(a, b) = a * x + b * y.
#Пусть мы нашли решение (x1, y1) для пары (b % a, a): b % a * x1 + a * y1 = g,
#и хотим получить решение (x, y) для пары (a, b): a * x + b * y = НОД(a, b).
#Для этого преобразуем величину b % a = b - [b / a] * a.
#Подставим: (b % a * x1 + a * y1 = g) => ((b - [b / a] * a) * x1 + a * y1 = g)
#Выполнив перегруппировку, получаем: g = b * x1 + a * (y1 - [b / a] * x1)
#Сравнив с исходным выражением, получаем: x = (y1 - [b / a] * x1), y = x1.
def xgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = xgcd(b % a, a)
    return (gcd, y - (b // a) * x, x)

#Шифрование (единичное).
def encrypt(char_code, key, N):
    return char_code ** key % N

#Шифрование всего сообщения.
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