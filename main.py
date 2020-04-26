from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import FastAPI, Response, status
from fastapi import Depends, Cookie, HTTPException
import secrets


app = FastAPI()
security = HTTPBasic()


def username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_login = secrets.compare_digest(credentials.login, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")

    if not (correct_login and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            
        )
    return credentials.login


@app.get("/")
def read_root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcoming():
    return {"message": "Some stupid message"}

@app.post("/login")
def new_login(new_user = Depends(username)):
    
    session_token = sha256(bytes(f"{login}{password}", encoding='utf8')).hexdigest()
    app.tokens_list.append(session_token)
    
    response.set_cookie(key="session_token", value=session_token)
    
        
    response = RedirectResponse(url = "/welcome")
    response.status_code = status.HTTP_302_FOUND
    
    return response