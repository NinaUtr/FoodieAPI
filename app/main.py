from fastapi import FastAPI

app = FastAPI()


@app.get("/get_hello")
async def get_hello():
    return {"message": "hello"}
