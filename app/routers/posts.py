from .. import models,schemas
from typing import List
from fastapi import Body,  HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import   get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session=Depends(get_db)):
    posts =db.query(models.Post).all()
    return   posts

@router.post("/createPost", status_code=201)
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


@router.post("/createPost/v2",status_code=status.HTTP_201_CREATED,  response_model = schemas.CustomPostResponse)
def createPostWithModel(newPost: schemas.PostCreate, db: Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #     (newPost.title,newPost.content, newPost.published))
    # new_post = cursor.fetchone()
    # conn.commit() # To save the changes to db
    new_post = models.Post(**newPost.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {
        "message": "Hey Prince!,\nA new post has been created!",
        "status": 201,
        "success": True,
        "data": new_post,
    }

@router.get("/{id}", response_model=schemas.Post)
def getPostById(id: int, db:Session=Depends(get_db)): 
    # cursor.execute("SELECT * FROM posts WHERE id=%s", str(id,))
    # post = cursor.fetchone() 
    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
    #     )

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (id,))
    # deletedPost = cursor.fetchone()
    # conn.commit()
    deletedPost = db.query(models.Post).filter(models.Post.id == id)
    if deletedPost.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not Found")
    deletedPost.delete(synchronize_session=False)
    db.commit()

   
    return Response(status_code=status.HTTP_204_NO_CONTENT,)

@router.put("/{id}",response_model=schemas.CustomPostResponse)
def update_post(id: int, post: schemas.PostCreate, db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s,published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.published,id))
    # updated_post = cursor.fetchone()
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updatedPost = updated_post_query.first()
   
    if updated_post_query == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found"
        )
    
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {
        "message": "Update post",
        "status": 200,
        "success": True,
        "data": updated_post_query.first(),
    }
