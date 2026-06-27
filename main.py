from fastapi import FastAPI
from routers import auth, users

app = FastAPI(title='Blog-Post API', description='A simple blog post api')

app.include_router(auth.router)
app.include_router(users.router)

@app.get('/root')
async def root() -> dict:
    return {'msg': 'root'}