# keygen.py
from cryptography.fernet import Fernet

def generate_key(path="secret.key"):
    key = Fernet.generate_key()
    with open(path, "wb") as f:
        f.write(key)
    print(f"Key generated and saved to {path}")
    print("Keep this file secret. Share it only with trusted clients.")

if __name__ == "__main__":
    generate_key()
