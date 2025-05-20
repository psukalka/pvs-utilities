import uuid

from datetime import datetime
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Posts API", description="A Simple API for creating and retrieving posts")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

posts_db = {}
users_db = {}

class User(BaseModel):
    id: str
    username: str

def get_current_user(user_id: str = "default-user"):
    if user_id not in users_db:
        users_db[user_id] = User(id=user_id, username=f"user-{user_id}")
    return users_db.get(user_id)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Posts API"}

@app.post("/posts/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, user: User = Depends(get_current_user)):
    post_id = str(uuid.uuid4())
    post_data = Post(
        id=post_id,
        user_id=user.id,
        created_at=datetime.now(),
        **post.model_dump()
    )

    if user.id not in posts_db:
        posts_db[user.id] = dict()
    posts_db[user.id][post_id] = post_data

    return post_data

@app.get("/posts/", response_model=List[Post])
def read_posts(user: User=Depends(get_current_user)):
    if user.id not in posts_db:
        return []
    return list(posts_db[user.id].values())

@app.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: str, user: User=Depends(get_current_user)):
    if user.id not in posts_db or post_id not in posts_db[user.id]:
        raise HTTPException(status_code=404, detail="Post Not Found")
    return posts_db[user.id][post_id]

@app.delete("/posts/{post_id}", response_model=Post)
def delete_post(post_id: str, user: User=Depends(get_current_user)):
    if user.id not in posts_db or post_id not in posts_db[user.id]:
        raise HTTPException(status_code=404, detail="Post Not Found")
    del posts_db[user.id][post_id]
    return {"message": f"Post: {post_id} is deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)