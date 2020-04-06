from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.api_route(path="/method", method=["GET", "POST", "PUT", "DELETE"])
def requests():
	return{"method": requests.method}