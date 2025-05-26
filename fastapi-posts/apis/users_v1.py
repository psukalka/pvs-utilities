from fastapi import APIRouter
from db.database import users_db
from models.users import User

router = APIRouter()


class UsersV1():
    def get_current_user(self, user_id: str = "default-user"):
        if user_id not in users_db:
            users_db[user_id] = User(id=user_id, username=f"user-{user_id}")
        return users_db.get(user_id)
