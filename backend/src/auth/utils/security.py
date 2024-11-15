from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verifyAccessToken(token: str, secret: str, algo: str):
    try:
        return jwt.decode(token, secret, algorithms=algo)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def createAccesstoken(data: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.now() + expiry
    data.update({"exp": expire})
    return jwt.encode(data, secret, algorithm=algo)
