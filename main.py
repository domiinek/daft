from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get(path="/method", method=["GET", "POST", "PUT", "DELETE"])
def write_requests(requests:Request):
	return{"method": requests.method}