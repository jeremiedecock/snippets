from typing import Union

from fastapi import FastAPI, HTTPException, Depends, Request

# https://stackoverflow.com/questions/64146591/custom-authentication-for-fastapi

# Generate random token: tr -dc A-Za-z0-9 </dev/urandom | head -c 64 ; echo ''
SUBMIT_API_TOKEN = "Dj5XjzKoQjHpsNHgsG1wlpSUZuc6n3hVG5UHOFa6WmdmGHl28PaXC2qY3dkp2bq7"

app = FastAPI()


def check_api_token(req: Request):
    if "api-token" in req.headers:
        if req.headers["api-token"] != SUBMIT_API_TOKEN:
            raise HTTPException(status_code=401, detail="access denied")
    else:
        raise HTTPException(status_code=401, detail="missing Token")

    return True


@app.post("/")
def read_root(authorized: bool = Depends(check_api_token)):
    if authorized:
        return {"Access": "allowed!"}
