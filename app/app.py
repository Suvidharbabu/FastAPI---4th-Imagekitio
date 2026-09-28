from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption = caption,
        url = "dummy url",
        file_type = "photo",
        file_name = "dummy name" 
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )

    return {
        "posts": posts_data
    }




# text_posts = {}

# @app.get("/posts")
# def get_all_posts(limit: int):
#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts

# @app.get("/posts/{id}")
# def get_post(id: int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found")
    
#     return text_posts.get(id)

# @app.post("/posts")
# def create_post(post: PostResponse):
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys()) + 1] = new_post
#     return new_post

# @app.delete("/posts/{id}")
# def delete_post(id: int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="Post not found")
    
#     return text_posts.del(id)





