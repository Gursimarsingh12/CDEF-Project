from fastapi import APIRouter, Depends, Header, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.cruds.UserCruds import createUser, getCurrentUser, login_user, refreshAccessToken
from auth.request.RegisterUserRequest import RegisterUserRequest
from auth.response.UserResponse import UserResponse
from auth.response.LoginResponse import LoginResponse

auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(getCurrentUser)]
)

guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}}
)

@guest_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(user: RegisterUserRequest = Query()):
    return await createUser(user)

@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_user(form_data)

@guest_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(refresh_token: str = Header(...)):
    return await refreshAccessToken(refresh_token)

@auth_router.get("/me", response_model=UserResponse)
async def read_users_me(user: UserResponse = Depends(getCurrentUser)):
    return user