import hashlib, uuid

def hash_password(password: str) -> str:
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(str(password + salt).encode('utf-8')).hexdigest()
    return salt, hashed_password
