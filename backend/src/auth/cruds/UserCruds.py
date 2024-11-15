from datetime import datetime, timedelta
from typing import Optional
from bson import ObjectId
from fastapi.security import OAuth2PasswordRequestForm
from auth.models.EmailUser import EmailUser
from auth.DatabaseController import getTokenCollection, getUsersCollection
from fastapi import Depends, HTTPException, status
from auth.utils.PasswordHelper import isPasswordStrongEnough, rawPasswordToHashed, verifyPassword
from auth.request.RegisterUserRequest import RegisterUserRequest
from auth.response.UserResponse import UserResponse
from auth.response.LoginResponse import LoginResponse
from auth.utils.security import createAccesstoken, oauth2_scheme, verifyAccessToken
from config import Config

async def createUser(userRequest: RegisterUserRequest) -> UserResponse:
    usersCollection = await getUsersCollection()
    user_exist = await usersCollection.find_one({"email": userRequest.email})
    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    if not isPasswordStrongEnough(userRequest.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not strong enough")
    user = {
        "name": userRequest.name,
        "email": userRequest.email,
        "password": rawPasswordToHashed(userRequest.password),
        "createdAt": datetime.now(),
    }
    result = await usersCollection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return UserResponse(**user)

async def getCurrentUser(token: str = Depends(oauth2_scheme)) -> UserResponse:
    data = verifyAccessToken(token, Config.JWT_SECRET, Config.JWT_ALGORITHM)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    user_id: Optional[str] = data.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token structure"
        )
    usersCollection = await getUsersCollection()
    user = await usersCollection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user)

async def refreshAccessToken(refreshToken: str):
    data = verifyAccessToken(refreshToken, Config.JWT_SECRET, Config.JWT_ALGORITHM)
    userId = data.get("sub")
    tokensCollection = await getTokenCollection()
    tokenData = await tokensCollection.find_one({"user_id": ObjectId(userId), "refresh_key": refreshToken})
    if not tokenData:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    newAccessToken = createAccesstoken({"sub": str(userId)}, Config.JWT_SECRET, Config.JWT_ALGORITHM, timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": newAccessToken}

async def login_user(form: OAuth2PasswordRequestForm = Depends()) -> LoginResponse:
    usersCollection = await getUsersCollection()
    user = await usersCollection.find_one({"email": form.username})
    if not user or not verifyPassword(form.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    user_id = str(user["_id"])
    access_token = createAccesstoken({"sub": user_id}, Config.JWT_SECRET, Config.JWT_ALGORITHM, timedelta(minutes=15))
    refresh_token = createAccesstoken({"sub": user_id}, Config.JWT_SECRET, Config.JWT_ALGORITHM, timedelta(days=7))
    
    token_data = {
        "user_id": ObjectId(user_id),
        "access_token": access_token,
        "refresh_token": refresh_token,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(days=7)
    }
    tokensCollection = await getTokenCollection()
    await tokensCollection.replace_one({"user_id": ObjectId(user_id)}, token_data, upsert=True)
    loginResponse = LoginResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer", expires_in=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return loginResponse
