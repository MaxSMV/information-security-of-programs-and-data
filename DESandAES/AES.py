from Crypto.Cipher import AES

# Встановити ключ для шифрування AES
key = b'secretKey1234567'

# Створити об'єкт AES
aes = AES.new(key, AES.MODE_ECB)

# Відкриваємо вхідний та вихідний файли
with open('input.txt', 'rb') as infile, open('output_aes.txt', 'wb') as outfile:
    # Читання вхідного файлу 16-байтними фрагментами
    while True:
        chunk = infile.read(16)
        if len(chunk) == 0:
            # Кінець файлу
            break
        elif len(chunk) % 16 != 0:
            # Доповнити chunk пробілами, якщо його довжина менша за 16 байт
            chunk += b' ' * (16 - len(chunk))
        # Зашифрувати чанк і записати його у вихідний файл
        outfile.write(aes.encrypt(chunk))

# Відкрити зашифрований файл і розшифрувати його
with open('output_aes.txt', 'rb') as infile:
    # Читання зашифрованого файлу 16-байтними фрагментами
    while True:
        chunk = infile.read(16)
        if len(chunk) == 0:
            # Кінець файлу
            break
        # Розшифрувати і вивести його
        print(aes.decrypt(chunk).decode().rstrip())
