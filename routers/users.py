from fastapi import APIRouter
from models import UserRegister, UserLogin
from database import users_col
import bcrypt
from datetime import datetime

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):
    try:
        existing = users_col.find_one({"email": user.email})
        if existing:
            return {"status": "failed", "error": "Email already exists"}

        hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

        result = users_col.insert_one({
            "name": user.name,
            "email": user.email,
            "password": hashed.decode("utf-8"),  # string form mein save
            "bio": user.bio,
            "created_at": str(datetime.now())
        })

        return {
            "status": "success",
            "message": "User registered",
            "data": {"id": str(result.inserted_id)}
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@router.post("/login")
def login(user: UserLogin):
    try:
        found = users_col.find_one({"email": user.email})
        if not found:
            return {"status": "failed", "error": "User not found"}

        # Naya tarika verify karne ka
        password_match = bcrypt.checkpw(
            user.password.encode("utf-8"),
            found["password"].encode("utf-8")
        )

        if not password_match:
            return {"status": "failed", "error": "Wrong password"}

        return {
            "status": "success",
            "message": "Login successful",
            "data": {
                "id": str(found["_id"]),
                "name": found["name"],
                "email": found["email"]
            }
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@router.get("/profile/{user_id}")
def get_profile(user_id: str):
    try:
        from bson import ObjectId
        user = users_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"status": "failed", "error": "User not found"}

        return {
            "status": "success",
            "data": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "bio": user["bio"],
                "created_at": user["created_at"]
            }
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}