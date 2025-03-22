from random import randrange
from typing import Optional

from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    description: str
    img: int
    published: bool = True
    ratings: Optional[int] = None


my_posts = [
    {
        "title": "Title Post 1",
        "description": "Description Post 1",
        "img": 1,
        "published": True,
        "ratings": 4,
        "id": 1,
    },
    {
        "title": "Title Post 2",
        "description": "Description Post 2",
        "img": 2,
        "published": False,
        "ratings": 5,
        "id": 2,
    },
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hey Prince!"}


@app.get("/posts")
def get_posts():
    return {
        "data": my_posts,
    }


@app.get("/admin")
def admin():
    return {
        "message": "Hey Prince!,\nIt's Admin this side!",
        "status": 200,
        "success": True,
    }


@app.post("/createPost", status_code=201)
def createPost(payload: dict = Body(...)):
    print(payload)
    return {
        "message": "Hey Prince!,\nA new post has been created!",
        "status": 201,
        "success": True,
        "data": {
            "title": payload["name"],
            "description": payload["description"],
            "img": payload["img"],
        },
    }


@app.post("/createPost/v2")
def createPostWithModel(newPost: Post):
    post_dict = newPost.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {
        "message": "Hey Prince!,\nA new post has been created!",
        "status": 201,
        "success": True,
        "data": post_dict,
    }


@app.get("/posts/latest")
def getLatestPost():
    post = my_posts[len(my_posts) - 1]
    return {
        "message": "Hey Prince!,\nThe latest post is:",
        "status": 200,
        "success": True,
        "data": post,
    }


@app.get("/posts/{id}")
def getPostById(id: int, response: Response):
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     "message": "Post not found",
        #     "status": response.status_code,
        #     "success": False
        # }
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    postIndex = find_index_post(id)
    if postIndex is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[postIndex] = post_dict
    return {
        "message": "Update post",
        "status": 200,
        "success": True,
        "data": post_dict,
    }
