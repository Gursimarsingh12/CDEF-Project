from typing import Union
from pydantic import BaseModel, EmailStr
from datetime import datetime

class EmailUser(BaseModel):
    _id: Union[str, None] = None
    name: str
    email: EmailStr
    password: str
    createdAt: datetime