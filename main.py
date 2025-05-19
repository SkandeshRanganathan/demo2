from fastapi import FastAPI, HTTPException, status
from tortoise.contrib.fastapi import register_tortoise
from app.routers import posts, users, auth
from app import schemas, models, utils
from pydantic import BaseModel

app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


register_tortoise(
    app,
    db_url="postgresql://postgres:Skandesh2005*@localhost/fastapi",
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostSchema):
    id: int

    class Config:
        orm_mode = True

@app.post("/posts", response_model=PostResponse)
async def create_post(post: PostSchema):
    new_post = await models.Post.create(**post.model_dump())
    return await PostResponse.from_tortoise_orm(new_post)

@app.get("/posts", response_model=list[PostResponse])
async def get_posts():
    posts = await models.Post.all()
    return posts

@app.get("/posts/{id}", response_model=PostResponse)
async def get_post(id: int):
    post = await models.Post.get_or_none(id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return await PostResponse.from_tortoise_orm(post)

@app.put("/posts/{id}", response_model=PostResponse)
async def update_post(id: int, updated_post: PostSchema):
    post = await models.Post.get_or_none(id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await post.update_from_dict(updated_post.model_dump())
    await post.save()
    return await PostResponse.from_tortoise_orm(post)

@app.delete("/posts/{id}")
async def delete_post(id: int):
    post = await models.Post.get_or_none(id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await post.delete()
    return {"message": "Post deleted"}

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def createuser(user: schemas.UserCreate):
    hashed = utils.hash(user.password)
    user.password = hashed
    new_user = await models.User.create(**user.model_dump())
    return await schemas.UserOut.from_tortoise_orm(new_user)
