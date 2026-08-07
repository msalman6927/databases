from fastapi import APIRouter
from models import PostCreate, CommentCreate
from database import posts_col, users_col
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/create/{user_id}")
def create_post(user_id: str, post: PostCreate):
    try:
        # User exist karta hai?
        user = users_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"status": "failed", "error": "User not found"}

        result = posts_col.insert_one({
            "user_id": user_id,
            "user_name": user["name"],
            "content": post.content,
            "likes": [],        # empty list — koi like nahi abhi
            "comments": [],     # empty list — koi comment nahi abhi
            "created_at": str(datetime.now())
        })

        return {
            "status": "success",
            "message": "Post created",
            "data": {"id": str(result.inserted_id)}
        }
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@router.get("/all")
def get_all_posts():
    try:
        posts = posts_col.find().sort("created_at", -1)
        list_posts = []
        for post in posts:
            list_posts.append({
                "id": str(post["_id"]),
                "user_name": post["user_name"],
                "content": post["content"],
                "total_likes": len(post["likes"]),
                "total_comments": len(post["comments"]),
                "comments": post["comments"],
                "created_at": post["created_at"]
            })
        return {"status": "success", "data": list_posts}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@router.post("/like/{post_id}/{user_id}")
def like_post(post_id: str, user_id: str):
    try:
        post = posts_col.find_one({"_id": ObjectId(post_id)})
        if not post:
            return {"status": "failed", "error": "Post not found"}

        # Agar pehle se like hai toh unlike karo
        if user_id in post["likes"]:
            posts_col.update_one(
                {"_id": ObjectId(post_id)},
                {"$pull": {"likes": user_id}}  # list se nikalo
            )
            return {"status": "success", "message": "Unliked"}
        else:
            posts_col.update_one(
                {"_id": ObjectId(post_id)},
                {"$push": {"likes": user_id}}  # list mein daalo
            )
            return {"status": "success", "message": "Liked"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


@router.post("/comment/{post_id}/{user_id}")
def add_comment(post_id: str, user_id: str, comment: CommentCreate):
    try:
        user = users_col.find_one({"_id": ObjectId(user_id)})
        post = posts_col.find_one({"_id": ObjectId(post_id)})

        if not user or not post:
            return {"status": "failed", "error": "User or Post not found"}

        new_comment = {
            "user_id": user_id,
            "user_name": user["name"],
            "text": comment.text,
            "created_at": str(datetime.now())
        }

        posts_col.update_one(
            {"_id": ObjectId(post_id)},
            {"$push": {"comments": new_comment}}
        )

        return {"status": "success", "message": "Comment added"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}