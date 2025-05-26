from fastapi import APIRouter
from apis.posts_v1 import PostsV1

api_router = APIRouter()
posts_v1 = PostsV1()

api_router.add_api_route("/posts/", posts_v1.create_post, methods=["POST"], status_code=201, tags=["posts"])
api_router.add_api_route("/posts/", posts_v1.read_posts, methods=["GET"], status_code=200, tags=["posts"])
api_router.add_api_route("/posts/{post_id}/", posts_v1.read_post, methods=["GET"], status_code=200, tags=["posts"])
api_router.add_api_route("/posts/{post_id}/", posts_v1.delete_post, methods=["DELETE"], status_code=200, tags=["posts"])
