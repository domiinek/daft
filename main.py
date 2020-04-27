from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, Request, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256
from fastapi.templating import Jinja2Templates


import secrets
from typing import Dict

from pydantic import BaseModel



templates = Jinja2Templates(directory="templates")
app = FastAPI()
security = HTTPBasic()
app.session_tokens = []
app.secret_key = "my secret key"



@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome(request: Request, session_token: str = Cookie(None)):
    if session_token not in app.session_tokens:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return templates.TemplateResponse("welcome.html", {"request": request, "user": "trudnY"})

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




@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}

