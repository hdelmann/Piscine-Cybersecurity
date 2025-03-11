import os
import sys
import json
import re
import time
import base64
import struct
import hashlib
import hmac
import keyring
from Crypto.Cipher import AES

STORAGE_FILE = "storage.json"
SERVICE_NAME = "my_encryption_service"

def load_storage():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    return {"last_execution": 0, "counter": 0}

def save_storage(data):
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file)

def read_file_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except (OSError, UnicodeDecodeError):
        return None

def is_hex_regex(s):
    return bool(re.fullmatch(r'[0-9A-Fa-f]+', s))

def check_key(key):
    if is_hex_regex(key) and len(key) >= 64:
        return key
    if os.path.isfile(key):
        content = read_file_content(key)
        if is_hex_regex(content) and len(content) >= 64:
            return content
    return None

def get_key():
    key = keyring.get_password(SERVICE_NAME, "encryption_key")
    if key is None:
        key = os.urandom(32)
        keyring.set_password(SERVICE_NAME, "encryption_key", key.hex())
    return bytes.fromhex(key.decode() if isinstance(key, bytes) else key)

def encrypt(hex_key, key_encrypting):
    cipher = AES.new(key_encrypting, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(hex_key.encode())
    return base64.b64encode(cipher.nonce + ciphertext).decode()

def decrypt(encrypted_hex_key, key_encrypting):
    data = base64.b64decode(encrypted_hex_key)
    nonce, ciphertext = data[:16], data[16:]
    cipher = AES.new(key_encrypting, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode()

def hotp(K, C):
    K = K.encode()
    c = struct.pack(">Q", C)
    hmac_ = hmac.new(K, c, hashlib.sha1).digest()
    offset = hmac_[-1] & 0x0F
    selected_bytes = hmac_[offset:offset + 4]  
    integer_32bit = struct.unpack(">I", selected_bytes)[0]  
    binary = integer_32bit & 0x7FFFFFFF  
    otp = binary % (10 ** 6)
    return str(otp).zfill(6)

def main():
    if len(sys.argv) < 3:
        print(f"ft_opt need 2 arguments")
        exit(1)

    if sys.argv[1] not in ("-k", "-g"):
        print(f"Usage : ./ft_opt -g < hexadecimal key>, to save a key")
        print(f"                 -k \"ft_opt.key\", to generate password")
        exit(1)

    storage = load_storage()

    if sys.argv[1] == "-g":
        key = check_key(sys.argv[2])
        if key is None:
            print(f"Key is not valid: Key must be a hexadecimal of at least 64 characters")
            exit(1)
        key_encrypting = get_key()
        with open("ft_opt.key", "w") as file:
            file.write(encrypt(key, key_encrypting))

    if sys.argv[1] == "-k":
        if sys.argv[2] != "ft_opt.key":
            print(f"Usage : ./ft_opt -k needs the file: \"ft_opt.key\" to work")
            exit(1)
        if not os.path.exists("ft_opt.key"):
            print("Error: ft_opt.key not found. Generate it first with -g option.")
            exit(1)
        with open("ft_opt.key", "r") as file:
            key_decrypt = decrypt(file.read(), get_key())

        current_time = time.time()
        if current_time - storage["last_execution"] > 60:
            storage["last_execution"] = current_time
            storage["counter"] += 1
            save_storage(storage)

        print(storage["counter"])
        opt_code = hotp(key_decrypt, storage["counter"])
        print(opt_code)

main()
