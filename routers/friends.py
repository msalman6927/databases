from fastapi import APIRouter
from models import FriendRequest
from database import friends_col, users_col
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/send/{sender_id}")
def send_request(sender_id: str, req: FriendRequest):
    try:
        # Already request hai?
        existing = friends_col.find_one({
            "sender_id": sender_id,
            "receiver_id": req.receiver_id
        })
        if existing:
            return {"status": "failed", "error": "Request already sent"}

        friends_col.insert_one({
            "sender_id": sender_id,
            "receiver_id": req.receiver_id,
            "status": "pending",
            "created_at": str(datetime.now())
        })

        return {"status": "success", "message": "Friend request sent","request_id":friends_col.inserted_id}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@router.put("/respond/{request_id}")
def respond_request(request_id: str, action: str):
    # action = "accepted" ya "rejected"
    try:
        result = friends_col.update_one(
            {"_id": ObjectId(request_id)},
            {"$set": {"status": action}}
        )
        if result.modified_count == 0:
            return {"status": "failed", "error": "Request not found"}

        return {"status": "success", "message": f"Request {action}"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@router.get("/list/{user_id}")
def get_friends(user_id: str):
    try:
        # Woh requests jahan status accepted hai
        friend_docs = friends_col.find({
            "$or": [
                {"sender_id": user_id, "status": "accepted"},
                {"receiver_id": user_id, "status": "accepted"}
            ]
        })

        friends = []
        for doc in friend_docs:
            # Doosra wala user kaun hai?
            other_id = doc["receiver_id"] if doc["sender_id"] == user_id else doc["sender_id"]
            other_user = users_col.find_one({"_id": ObjectId(other_id)})
            if other_user:
                friends.append({
                    "id": str(other_user["_id"]),
                    "name": other_user["name"]
                })

        return {"status": "success", "data": friends}
    except Exception as e:
        return {"status": "failed", "error": str(e)}