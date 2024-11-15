from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    _id: str
    name: str
    email: EmailStr
    createdAt: Union[str, None, datetime] = None