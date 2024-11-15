from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class EmailRequest(BaseModel):
    email: EmailStr