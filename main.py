from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel


app = FastAPI()

class Post(BaseModel):
    title: str
    description: str
    img: int 
    published : bool = True
    ratings : Optional[int] = None


@app.get("/")
async def root():
    return {"message" : "Hey Prince!"}

@app.get("/admin")
def admin():
    return {
        "message": "Hey Prince!,\nIt\'s Admin this side!",
        "status": 200,
        "success": True
    }

@app.post("/createPost") 
def createPost(payload: dict = Body(...) ):
    print(payload)
    return {
        "message": "Hey Prince!,\nA new post has been created!",
        "status": 201,
        "success": True,
        "data":{
            "title": payload['name'],
            "description": payload['description'],
            "img": payload['img']
        }
    }

@app.post("/createPost/v2")
def createPostWithModel(newPost: Post):
    return {
        "message": "Hey Prince!,\nA new post has been created!",
        "status": 201,
        "success": True,
        "data": newPost.dict() 
    }