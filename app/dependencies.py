from fastapi import Security, HTTPException
from fastapi.security import APIKeyCookie

token_cookie_scheme = APIKeyCookie(name="X-Chatter-Token")

def verify_session_token(x_chatter_token: str = Security(token_cookie_scheme)):
    if not x_chatter_token:
        raise HTTPException(status_code=401, detail="Unathorized")
    return x_chatter_token
