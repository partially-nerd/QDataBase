from passlib.hash import sha256_crypt
from dotenv import load_dotenv

load_dotenv()
from os import getenv

USER = sha256_crypt.encrypt(getenv("USERNAME"))
PASS = sha256_crypt.encrypt(getenv("PASSWORD"))


def verify_password(username: str, password: str):
    return sha256_crypt.verify(username, USER) and sha256_crypt.verify(password, PASS)
