from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash(password: str):
    return password_hash.hash(password)

def verify(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password) # This function takes a plain password and a hashed password, and returns True if the plain password matches the hashed password, and False otherwise. It uses the verify method of the PasswordHash class to perform the verification.