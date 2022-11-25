from hmac import digest
from Crypto.Hash import SHA256
import sys
import rsa

#Хэширование строки байтов
def hash(data):
    h = SHA256.new()
    h.update(data)
    return h.digest()

#Чтение открытого ключа дешифровки D из файла
def get_public_key():
    f = open("public_key.pem")
    data = f.read()

    public_key = rsa.PrivateKey.load_pkcs1(data, format='PEM')

    return public_key

#Проверка подписи (дешифровка с использованием открытого ключа D)
def check_signature(source_filename, signed_filename, public_key):

    f = open(source_filename, "rb")
    data = f.read()
    f.close()

    hashed_data = hash(data)

    s = open(signed_filename, "rb")
    signed_data = s.read()
    s.close()

    decrypted_data = rsa.decrypt(signed_data, public_key)

    return (decrypted_data == hashed_data)

def main():
    source_filename = sys.argv[1] #Файл с сообщением M, которое к нам пришло
    signed_filename = sys.argv[2] #Файл с подписью (предположительно)

    public_key = get_public_key() #Открытый ключ расшифровки D
    res = check_signature(source_filename, signed_filename, public_key)

    if res:
        print("Signature is valid.")
    else:
        print("Signature is not valid.")

if __name__ == "__main__":
    main()