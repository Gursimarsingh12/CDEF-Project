from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>']

def rawPasswordToHashed(rawPassword: str):
    return pwdContext.hash(rawPassword)

def verifyPassword(plainPassword: str, hashedPassword: str):
    return pwdContext.verify(plainPassword, hashedPassword)

def isPasswordStrongEnough(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False
    return True