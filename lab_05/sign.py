from hmac import digest
from Crypto.Hash import SHA256
import sys
import rsa

#Хэширование строки байтов
def hash(data):
    h = SHA256.new()
    h.update(data)
    return h.digest()

#Генерация ключей алгоритма RSA и сохранение в файл открытого (public) ключа дешифровки D
def generate_keys():
    private_key, public_key = rsa.newkeys(2048)

    f = open("public_key.pem", "wb")
    f.write(public_key.save_pkcs1("PEM"))
    f.close()

    return private_key, public_key

#Подпись файла (шифрование с использованием секретного ключа E)
def make_signature(filename, private_key):
    f = open(filename, 'rb')
    data = f.read()
    f.close()

    hashed_data = hash(data)

    signed_data = rsa.encrypt(hashed_data, private_key)

    s = open("signed_" + filename, "wb")
    s.write(signed_data)
    s.close()

def main():
    filename = sys.argv[1]

    private_key, public_key = generate_keys()

    print("\nSource file: " + filename + "\n")

    print("Signing file...\nSign completed.\n")

    make_signature(filename, private_key)

    print("Signed file: signed_" + filename + "\n")

    print("File with public key: public_key.pem")

if __name__ == "__main__":
    main()