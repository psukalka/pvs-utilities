import uuid
from datetime import datetime
from fastapi import Depends, HTTPException

from apis.users_v1 import UsersV1
from models.posts import PostCreate, Post
from models.users import User
from db.database import posts_db


class PostsV1():
    def create_post(self, post: PostCreate, user: User = Depends(UsersV1().get_current_user)):
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

    def read_posts(self, user: User = Depends(UsersV1().get_current_user)):
        if user.id not in posts_db:
            return []
        return list(posts_db[user.id].values())

    def read_post(self, post_id: str, user: User = Depends(UsersV1().get_current_user)):
        if user.id not in posts_db or post_id not in posts_db[user.id]:
            raise HTTPException(status_code=404, detail="Post Not Found")
        return posts_db[user.id][post_id]

    def delete_post(self, post_id: str, user: User = Depends(UsersV1().get_current_user)):
        if user.id not in posts_db or post_id not in posts_db[user.id]:
            raise HTTPException(status_code=404, detail="Post Not Found")
        del posts_db[user.id][post_id]
        return {"message": f"Post: {post_id} is deleted"}
