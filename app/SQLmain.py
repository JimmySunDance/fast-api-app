from typing import Optional, List

import psycopg2 as psy
import time
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models
from . import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psy.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="password123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connetction successful")
        break
    except Exception as error:
        print("Failed to connect to databases")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get("/posts", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    ## As SQL ###
    cursor.execute(
        """
        SELECT * FROM posts
        """
    )
    posts = cursor.fetchall()
    return posts


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    ## As SQL ###
    cursor.execute(
        """
        INSERT INTO posts (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *
        """,
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
    ## As SQL ###
    cursor.execute(
        """
        SELECT * FROM posts WHERE id = %s
        """,
        (str(id)),
    )
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    ## As SQL ###
    cursor.execute(
        """
        DELETE FROM posts WHERE id = %s
        RETURNING *
        """,
        (str(id)),
    )
    deleted_post = cursor.fetchone()

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    conn.commit()  # SQL commit
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.PostResponse)
async def update_post(
    id: int, post_update: schemas.PostCreate, db: Session = Depends(get_db)
):
    ## As SQL ###
    cursor.execute(
        """
        UPDATE posts
        SET title = %s, content = %s, published = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            post_update.title,
            post_update.content,
            post_update.published,
            str(id),
        ),
    )
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist",
        )

    conn.commit()  # SQL commit
    return updated_post
