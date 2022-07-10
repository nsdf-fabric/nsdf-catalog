from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm



from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


router = APIRouter()



@router.post("/auth/token")
async def get_token():

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "anonymous"}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,      # prevents client-side scripts from accessing cookie, against XSS attacks
        max_age=1800,
        expires=1800,       # expire after 30 minutes
        samesite="Lax",     # cookies are not send with every request, against CSRF attacks
        secure=False,       # ensure/disable HTTPS, TODO: set to True for production!
    )

    return response


@router.post("/auth/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,      # prevents client-side scripts from accessing cookie, against XSS attacks
        max_age=1800,
        expires=1800,       # expire after 30 minutes
        samesite="Lax",     # cookies are not send with every request, against CSRF attacks
        secure=False,       # ensure/disable HTTPS, TODO: set to True for production!
    )

    return response
