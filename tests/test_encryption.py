import os
import pytest
from safecrypt.encryption import encrypt_file, decrypt_file, generate_key, load_key

def test_encryption_decryption():
    key = generate_key()
    test_file = "test.txt"
    with open(test_file, "w") as f:
        f.write("Hello World!")

    encrypt_file(test_file, key)
    assert os.path.exists(test_file + ".enc")

    decrypt_file(test_file + ".enc", key)
    assert os.path.exists(test_file + "_dec")

    os.remove(test_file)
    os.remove(test_file + ".enc")
    os.remove(test_file + "_dec")
    os.remove("key.key")
