from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, Request, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256
from fastapi.templating import Jinja2Templates


import secrets
from typing import Dict

from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    surename: str

templates = Jinja2Templates(directory="templates")
app = FastAPI()
security = HTTPBasic()
app.session_tokens = []
app.secret_key = "my secret key"
app.counter: int = 0
app.storage: Dict[int, Patient] = {}



@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome(request: Request, session_token: str = Cookie(None)):
    if session_token in app.session_tokens:
        return templates.TemplateResponse("welcome.html", {"request": request, "user": "trudnY"})
    raise HTTPException(status_code=401,  detail="login required")

        

@app.post("/login")
def login_auth(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    correct_username  = secrets.compare_digest(credentials.username, "trudnY")
    correct_password  = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password ):
        raise HTTPException(status_code=401,  detail="Incorrect email or password", headers={"WWW-Authenticate": "Basic"})
    session_token = sha256(
        bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.session_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    response.headers["Location"] = "/welcome"
    response.status_code = status.HTTP_302_FOUND

@app.post("/logout")
def log_out(response: Response, request: Request, session_token: str = Cookie(None)):
    if session_token in app.session_tokens:
        app.session_tokens.remove(session_token)
        response.headers["Location"]="/"
    raise HTTPException(status_code=401,  detail="login required")


@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}

@app.post("/patient")
def show_data(patient: Patient):
    if session_token in app.session_tokens:
        resp = {"id": app.counter, "patient": patient}
        app.storage[app.counter] = patient
        app.counter += 1
        return resp


@app.get("/patient/{pk}")
def show_patient(pk: int):
    if session_token in app.session_tokens:
        if pk in app.storage:
            return app.storage.get(pk)
        return Response(status_code=status.HTTP_204_NO_CONTENT)