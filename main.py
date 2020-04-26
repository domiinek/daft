from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
from hashlib import sha256

import secrets


app = FastAPI()
security = HTTPBasic()
app.session_tokens = []
app.secret_key = "my secret key"



@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcoming():
    return {"message": "Some stupid message"}

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