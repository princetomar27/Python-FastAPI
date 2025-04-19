from random import randrange
import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import models,schemas, utils
from .routers import posts, user,auth

# import models from ./models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)