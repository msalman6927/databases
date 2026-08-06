from fastapi import FastAPI
from routers import users, posts, friends

app = FastAPI(title="Mini Facebook API")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(friends.router, prefix="/friends", tags=["Friends"])

@app.get("/")
def root():
    return {"status": "Mini Facebook API is running"}