from random import randrange
from typing import Optional
import psycopg2
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None

# Setup postgres db connection
while True:

    try:
        conn = psycopg2.connect(host='localhost',port=5433,database='fastapi',user='postgres',password='prince123',cursor_factory=RealDictCursor)
        cursor = conn.cursor() # Open a cursor to executre SQL statements
        print("Database connection established !")
        break

    except Exception as error :
        print ("Error while connecting to PostgreSQL", error)
        time.sleep(2)
   

 
my_posts = [
    {
        "title": "Title Post 1",
        "content": "content Post 1",
        "img": 1,
        "published": True,
        "ratings": 4,
        "id": 1,
    },
    {
        "title": "Title Post 2",
        "content": "content Post 2",
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
    cursor.execute("""SELECT * FROM posts """)
    posts =cursor.fetchall()
    print(posts)
    return {  
        "data": posts,
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
            "content": payload["content"],
            "img": payload["img"],
        },
    }


@app.post("/createPost/v2")
def createPostWithModel(newPost: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
        (newPost.title,newPost.content, newPost.published))
    new_post = cursor.fetchone()
    conn.commit() # To save the changes to db
    return {
        "message": "Hey Prince!,\nA new post has been created!",
        "status": 201,
        "success": True,
        "data": new_post ,
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
    cursor.execute("SELECT * FROM posts WHERE id=%s", str(id,))
    post = cursor.fetchone() 
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    deletedPost = cursor.fetchone()
    conn.commit()
    if deletedPost == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not Found") 
    return Response(status_code=status.HTTP_204_NO_CONTENT,)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s,published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published,id))
    updated_post = cursor.fetchone()
   
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return {
        "message": "Update post",
        "status": 200,
        "success": True,
        "data": updated_post,
    }
