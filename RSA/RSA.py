from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_RSA_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_message(public_key, message):
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    ciphertext = cipher.encrypt(message.encode('utf-8'))
    return ciphertext

def decrypt_message(private_key, ciphertext):
    decrypt_cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    plaintext = decrypt_cipher.decrypt(ciphertext)
    return plaintext.decode('utf-8')

# Example usage
private_key, public_key = generate_RSA_keys()
print("Private key: ", private_key)
print("Public key: ", public_key)

message = "Hello, RSA!"
print("Original message: ", message)

ciphertext = encrypt_message(public_key, message)
print("Encrypted message: ", ciphertext)

plaintext = decrypt_message(private_key, ciphertext)
print("Decrypted message: ", plaintext)