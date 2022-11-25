import os, sys

DICT_INIT_SIZE = 256

#Функция сжатия, принимает на вход два указателя на файл: 
#файл с содержимым, которое необходимо сжать, и файл, куда нужно записать сжатые данные.
def compress(src_f, dst_f):
    dictionary = dict([(bytes([i]), i) for i in range(DICT_INIT_SIZE)]) 

    dict_size = DICT_INIT_SIZE
    code_len = 9   #Количество бит, необходимое для шифрации очередного символа
    word = bytes() #Текущая фраза
    result = ""

    data = src_f.read()
    for symbol in data:
        c = bytes([symbol])

        if word + c in dictionary: #Если новая фраза уже есть в словаре, то обновляем текущую фразу и идем дальше
            word += c
        else: #Если новой фразы нет в словаре, то:

            #Полученный код символа - это значение в словаре, где ключ - текущее слово, получаем биты
            code = bin(dictionary[word])[2:]

            #Дополняем битовое представление незначащими нулями и сохраняем последовательность в результирующую переменную
            result += '0' * (code_len - len(code)) + code

            #Добавляем новую фразу в словарь
            dictionary[word + c] = dict_size

            #Обновляем количество бит, необходимых для шифрации
            if len(bin(dict_size)[2:]) > code_len:
                code_len += 1
            dict_size += 1

            #Обновляем текущую фразу
            word = c

    #Аналогичные действия по завершении цикла (последняя итерация)
    code = bin(dictionary[word])[2:]
    result += '0' * (code_len - len(code)) + code

    #Дополняем до байта
    if len(result) % 8 != 0:
        result += '0' * (8 - len(result) % 8)

    #Записываем результат в файл
    output = bytearray()
    for symbol in range(0, len(result), 8):
        output.append(int(result[symbol : symbol + 8], 2))
    dst_f.write(output)

#Функция, обратная сжатию, принимает на вход два указателя на файл:
#файл с содержимым, которое необходимо разжать, и файл, куда нужно записать разжатые данные.
def decompress(src_f, dst_f):
    dictionary = dict([(i, bytes([i])) for i in range(DICT_INIT_SIZE)])
    dict_size = DICT_INIT_SIZE
    code_len = 9 #Количество бит, необходимое для дешифрации очередного символа
    i = 0 #смещение от начала файла (в битах)
    result = bytearray()

    #Преобразуем байты в биты
    data = src_f.read()
    data_bin_str = ""
    for k in data:
        bin_k = bin(k)[2:]
        data_bin_str += '0' * (8 - len(bin_k)) + bin_k

    #Во входную фразу заносится первый код разжимаемого сообщения
    key = int(data_bin_str[i:i + code_len], 2)
    word = dictionary[key]

    #Заносим фразу в результат
    result += word
    i += code_len

    while i + code_len <= len(data_bin_str):
        #Вычисляем новый код (ключ)
        key = int(data_bin_str[i:i + code_len], 2)

        #Если ключ в словаре, то получаем по нему значение (строку)
        if key in dictionary:
            c = dictionary[key]
        elif key == dict_size: #Обработка исключительной ситуации: когда алгоритм сжатия выведет код прежде, чем распаковщик получит возможность определить его
            c = word + bytes([word[0]])
        
        #Заносим значение в результат
        result += c
        dictionary[dict_size] = word + bytes([c[0]])
        dict_size += 1
        i += code_len

        #Обновляем количество бит, необходимых для шифрации
        if len(bin(dict_size)[2:]) > code_len:
            code_len += 1

        #Обновляем текущую фразу
        word = c

    dst_f.write(result)

def main():
    filename = sys.argv[1]
    cfilename = 'compressed_' + filename
    dfilename = 'decompressed_' + filename

    f = open(filename, 'rb')
    cf = open(cfilename, 'wb')
    compress(f, cf)
    cf.close()
    f.close()

    cf = open(cfilename, 'rb')
    df = open(dfilename, 'wb')
    decompress(cf, df)
    cf.close()
    df.close()

    print("Uncompressed file: {} bytes".format(os.path.getsize(filename)))
    print("Compressed file:   {} bytes".format(os.path.getsize(cfilename)))
    print("Decompressed file: {} bytes".format(os.path.getsize(dfilename)))

if __name__ == '__main__':
    main()