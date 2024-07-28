from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
from typing import List
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Pydantic models
class Blog(BaseModel):
    title: str
    content: str
    categories: List[int]

class Comment(BaseModel):
    content: str

# Endpoints
@app.post("/blog")
async def create_blog(blog: Blog, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO blog (title, content, createdById, modifiedById) VALUES (%s, %s, %s, %s)", 
                       (blog.title, blog.content, user_id, user_id))
        blog_id = cursor.lastrowid
        for category_id in blog.categories:
            cursor.execute("INSERT INTO blog_category (blogId, categoryId) VALUES (%s, %s)", (blog_id, category_id))
        conn.commit()
        return {"message": "Blog created successfully", "blog_id": blog_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/blog/{blog_id}")
async def get_blog(blog_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Get blog details
        cursor.execute("SELECT * FROM blog WHERE id = %s", (blog_id,))
        blog = cursor.fetchone()
        
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        # Get categories
        cursor.execute("""
            SELECT c.id, c.name
            FROM category c
            JOIN blog_category bc ON c.id = bc.categoryId
            WHERE bc.blogId = %s
        """, (blog_id,))
        blog['categories'] = cursor.fetchall()
        
        # Get likes
        cursor.execute("SELECT userId FROM blog_like WHERE blogId = %s", (blog_id,))
        blog['likes'] = [row['userId'] for row in cursor.fetchall()]
        
        # Get comments with their likes
        cursor.execute("""
            SELECT c.*, GROUP_CONCAT(cl.userId) as like_user_ids
            FROM comment c
            LEFT JOIN comment_like cl ON c.id = cl.commentId
            WHERE c.blogId = %s
            GROUP BY c.id
        """, (blog_id,))
        comments = cursor.fetchall()

        # Process the likes for each comment
        for comment in comments:
            comment['likes'] = (
                [int(user_id) for user_id in comment['like_user_ids'].split(',')]
                if comment['like_user_ids']
                else []
            )
            del comment['like_user_ids']

        blog['comments'] = comments
        
        return blog
    finally:
        cursor.close()
        conn.close()

@app.get("/blog/category/{category_id}")
async def get_blogs_by_category(category_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT b.* FROM blog b
            JOIN blog_category bc ON b.id = bc.blogId
            WHERE bc.categoryId = %s
        """, (category_id,))
        blogs = cursor.fetchall()
        return blogs
    finally:
        cursor.close()
        conn.close()

@app.post("/blog/{blog_id}/comment")
async def add_comment(blog_id: int, comment: Comment, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO comment (blogId, content, createdById, modifiedById) VALUES (%s, %s, %s, %s)", 
                       (blog_id, comment.content, user_id, user_id))
        conn.commit()
        return {"message": "Comment added successfully", "comment_id": cursor.lastrowid}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/blog/{blog_id}/like")
async def like_blog(blog_id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO blog_like (blogId, userId) VALUES (%s, %s)", (blog_id, user_id))
        conn.commit()
        return {"message": "Blog liked successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/comment/{comment_id}/like")
async def like_comment(comment_id: int, user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO comment_like (commentId, userId) VALUES (%s, %s)", (comment_id, user_id))
        conn.commit()
        return {"message": "Comment liked successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/heartbeat")
async def heartbeat():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blog LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"status": "alive", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}