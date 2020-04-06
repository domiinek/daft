from fastapi import FastAPI
from typing import Dict

app = FastAPI()


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.api_route(path="/method", methods=["GET", "POST", "PUT", "DELETE"])
def our_requests(request: Request):
    return{"method": request.method}