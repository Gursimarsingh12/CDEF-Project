from pydantic import BaseModel
from bson import ObjectId
from typing import Optional
from pydantic.fields import Field
from datetime import datetime
from uuid import uuid4

class UserToken(BaseModel):
    _id: str
    user_id: ObjectId
    access_key: Optional[str] = None
    refresh_key: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now())
    expires_at: datetime