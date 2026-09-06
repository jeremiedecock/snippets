import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
security = HTTPBasic()

def check(credentials: HTTPBasicCredentials = Depends(security)):
    ok_user = secrets.compare_digest(credentials.username, "alice")
    ok_pass = secrets.compare_digest(credentials.password, "motdepasse")
    if not (ok_user and ok_pass):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            headers={"WWW-Authenticate": "Basic"})

@app.get("/", dependencies=[Depends(check)])
def hello():
    return {"message": "hello"}