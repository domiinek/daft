from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def our_requests(request: Request):
    return{"method": request.method}