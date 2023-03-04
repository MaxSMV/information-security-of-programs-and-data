from Crypto.Cipher import DES

# Ключ для шифрування DES
key = b'secretKe'

# Створення об'єкта DES
des = DES.new(key, DES.MODE_ECB)

# Відкриває вхідні та вихідні файли
with open('input.txt', 'rb') as infile, open('output_des.txt', 'wb') as outfile:
    # Читання вхідного файла 8-байтними фрагментами
    while True:
        chunk = infile.read(8)
        if len(chunk) == 0:
            # Кінець файлу
            break
        elif len(chunk) % 8 != 0:
            # Якщо довжина фрагмента не перевищує 8 байт, він повинен бути доповнений пробілами
            chunk += b' ' * (8 - len(chunk))
        # Шифрування фрагмента і запис його у вихідний файл
        outfile.write(des.encrypt(chunk))

# Відкрити зашифрований файл і розшифрувати його
with open('output_des.txt', 'rb') as infile:
    # Читання зашифрованого файлу 8-байтними фрагментами
    while True:
        chunk = infile.read(8)
        if len(chunk) == 0:
            # Кінець файлу
            break
        # Розшифрування фрагмента і вивід
        print(des.decrypt(chunk).decode().rstrip())
