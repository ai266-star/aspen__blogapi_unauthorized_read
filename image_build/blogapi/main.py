"""
Blog API with IDOR vulnerability.
Users can read and modify posts they don't own.
"""
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# Simple in-memory storage
posts_db = {}
next_post_id = 1
users_db = {"user1": "password1", "user2": "password2", "admin": "admin"}


class Post(BaseModel):
    title: str
    content: str
    is_draft: bool = False


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: str
    is_draft: bool
    created_at: str


def get_current_user(x_user_id: str = Header(None)) -> str:
    """Extract user_id from header."""
    if not x_user_id or x_user_id not in users_db:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_user_id


@app.post("/posts", response_model=PostResponse)
def create_post(post: Post, x_user_id: str = Header(None)):
    """Create a new post."""
    user = get_current_user(x_user_id)
    global next_post_id
    post_id = next_post_id
    next_post_id += 1
    
    posts_db[post_id] = {
        "id": post_id,
        "title": post.title,
        "content": post.content,
        "author_id": user,
        "is_draft": post.is_draft,
        "created_at": datetime.utcnow().isoformat()
    }
    return posts_db[post_id]


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, x_user_id: str = Header(None)):
    """
    Get a post by ID.
    VULNERABILITY: Does not check if the user owns the post.
    Non-admins can read any post, including private drafts.
    """
    user = get_current_user(x_user_id)
    
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post = posts_db[post_id]
    
    # BUG: Should check ownership or draft status here, but doesn't
    # Non-admin users should NOT be able to read drafts they don't own
    
    return post


@app.get("/posts", response_model=List[PostResponse])
def list_posts(x_user_id: str = Header(None)):
    """
    List all posts.
    VULNERABILITY: Returns all posts including drafts from other authors.
    Non-admins can see draft posts from other users.
    """
    user = get_current_user(x_user_id)
    
    # BUG: Should filter by ownership or published status
    # Returns ALL posts regardless of draft status or ownership
    return list(posts_db.values())


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: Post, x_user_id: str = Header(None)):
    """
    Update a post.
    VULNERABILITY: Does not check if the user owns the post.
    Non-admins can modify any post.
    """
    user = get_current_user(x_user_id)
    
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # BUG: Should check if user is the author (unless admin)
    # This allows any user to modify any post
    
    posts_db[post_id].update({
        "title": post.title,
        "content": post.content,
        "is_draft": post.is_draft
    })
    
    return posts_db[post_id]


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, x_user_id: str = Header(None)):
    """
    Delete a post.
    VULNERABILITY: Does not check if the user owns the post.
    Non-admins can delete any post.
    """
    user = get_current_user(x_user_id)
    
    if post_id not in posts_db:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # BUG: Should check ownership before deletion
    del posts_db[post_id]
    return {"message": "Post deleted"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}
