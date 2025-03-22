from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

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