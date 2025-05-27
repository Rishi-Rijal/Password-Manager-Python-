from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_password(password: str) -> str:
    key = load_key()
    f = Fernet(key)
    return f.encrypt(password.encode()).decode() 


def decrypt_password(token: str) -> str:
    key = load_key()
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()
