from cryptography.fernet import Fernet
import os

def generate_key():
    """
    Generates a new key for encryption and saves it as key.key
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key(key_file="key.key"):
    """
    Loads the key from a file
    """
    return open(key_file, "rb").read()

def encrypt_file(file_path, key):
    """
    Encrypts a file with the given key
    """
    fernet = Fernet(key)
    with open(file_path, "rb") as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_path, key):
    """
    Decrypts an encrypted file with the given key
    """
    fernet = Fernet(key)
    with open(file_path, "rb") as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    new_file_path = file_path.replace(".enc", "_dec")
    with open(new_file_path, "wb") as dec_file:
        dec_file.write(decrypted)
