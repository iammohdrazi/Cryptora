import os
import sys
import datetime
import argparse
from cryptography.fernet import Fernet, InvalidToken

# ---------------- Paths ----------------
if getattr(sys, 'frozen', False):  # running as exe
    BASE_DIR = os.path.dirname(sys.executable)
else:  # running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KEYS_DIR = os.path.join(BASE_DIR, "keys")
if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)

# ---------------- Encryption / Decryption Logic ----------------
def generate_key():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    key_name = f"cryptora_{timestamp}.key"
    key_path = os.path.join(KEYS_DIR, key_name)
    key = Fernet.generate_key()
    with open(key_path, "wb") as f:
        f.write(key)
    print(f"Key generated: {key_path}")
    return key_path

def load_key(path):
    if not os.path.exists(path):
        print(f"Key file not found: {path}")
        return None
    with open(path, "rb") as f:
        return f.read()

def list_keys():
    keys = [f for f in os.listdir(KEYS_DIR) if f.endswith(".key")]
    if not keys:
        print("No keys found.")
        return None
    keys_sorted = sorted(keys)
    print("All keys:")
    for k in keys_sorted:
        print(f" - {k}")
    latest_key = keys_sorted[-1]
    print(f"Latest key: {latest_key}")
    return os.path.join(KEYS_DIR, latest_key)

def get_latest_key():
    keys = [f for f in os.listdir(KEYS_DIR) if f.endswith(".key")]
    if not keys:
        return None
    latest_key = sorted(keys)[-1]
    return os.path.join(KEYS_DIR, latest_key)

def select_key_interactively():
    keys = [f for f in os.listdir(KEYS_DIR) if f.endswith(".key")]
    if not keys:
        print("No keys found. Generate one first.")
        return None
    keys_sorted = sorted(keys)
    print("Select a key from the list below:")
    for idx, k in enumerate(keys_sorted, 1):
        print(f"{idx}. {k}")
    while True:
        choice = input(f"Enter number (1-{len(keys_sorted)}) or press Enter for latest: ").strip()
        if choice == "":
            return os.path.join(KEYS_DIR, keys_sorted[-1])
        if choice.isdigit() and 1 <= int(choice) <= len(keys_sorted):
            return os.path.join(KEYS_DIR, keys_sorted[int(choice)-1])
        print("Invalid choice, try again.")

# ---------------- File Encryption ----------------
def encrypt_file(file_path, key_path):
    if not os.path.exists(file_path):
        print("File not found.")
        return
    if not os.path.exists(key_path):
        print("Key not found.")
        return
    if ".enc_" in file_path:
        print("File is already encrypted.")
        return

    try:
        key = load_key(key_path)
        fernet = Fernet(key)
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)

        key_name = os.path.splitext(os.path.basename(key_path))[0]
        output_file = file_path + f".enc_{key_name}"

        with open(output_file, "wb") as f:
            f.write(encrypted)

        print(f"File encrypted: {output_file}")
        print(f"Used key: {key_path}")
    except Exception as e:
        print(f"Encryption error: {str(e)}")

# ---------------- File Decryption ----------------
def decrypt_file(file_path, key_path):
    if not os.path.exists(file_path):
        print("File not found.")
        return
    if not os.path.exists(key_path):
        print("Key not found.")
        return
    if ".enc_" not in file_path:
        print("This file does not appear to be encrypted.")
        return

    try:
        key = load_key(key_path)
        fernet = Fernet(key)
        with open(file_path, "rb") as f:
            decrypted = fernet.decrypt(f.read())

        output_file = file_path.split(".enc_")[0]
        with open(output_file, "wb") as f:
            f.write(decrypted)

        print(f"File decrypted: {output_file}")
        print(f"Used key: {key_path}")
    except InvalidToken:
        print("Decryption failed: Incorrect key for this file.")
    except Exception as e:
        print(f"Decryption error: {str(e)}")

# ---------------- CLI ----------------
def main():
    parser = argparse.ArgumentParser(description="Cryptora - File Encryption/Decryption CLI")
    parser.add_argument("action", choices=["encrypt", "decrypt", "genkey", "listkeys"], help="Action to perform")
    parser.add_argument("-f", "--file", help="File path to encrypt/decrypt")
    parser.add_argument("-k", "--key", help="Key file path (default: latest key)")
    parser.add_argument("--selectkey", action="store_true", help="Interactively select a key from available keys")
    args = parser.parse_args()

    if args.action == "genkey":
        generate_key()
        return

    if args.action == "listkeys":
        list_keys()
        return

    if args.selectkey:
        key_path = select_key_interactively()
        if not key_path:
            return
    else:
        key_path = args.key if args.key else get_latest_key()
        if not key_path:
            print("No key found. Generate a key first using 'genkey'.")
            return

    if not args.file:
        print("Please provide a file path using -f")
        return

    if args.action == "encrypt":
        encrypt_file(args.file, key_path)
    elif args.action == "decrypt":
        decrypt_file(args.file, key_path)

if __name__ == "__main__":
    main()
