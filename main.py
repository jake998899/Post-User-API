from fastapi import FastAPI

app = FastAPI()

@app.get('/root')
async def root() -> dict:
    return {'msg': 'root'}