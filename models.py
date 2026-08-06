from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    bio: Optional[str] = ""

class UserLogin(BaseModel):
    email: str
    password: str

class PostCreate(BaseModel):
    content: str

class CommentCreate(BaseModel):
    text: str

class FriendRequest(BaseModel):
    receiver_id: str