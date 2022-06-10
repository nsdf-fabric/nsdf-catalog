from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

#import src.crud.search as crud

from src.auth.jwthandler import get_current_user
from src.schemas.repositories import RepositoryOutSchema, RepositoryInSchema, UpdateRepository
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/search",
    response_model=List[RepositoryOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_repositories():
    return await crud.get_results()




@router.get(
    "/detail/{entry_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def get_detail(entry_id: int, current_user: UserOutSchema = Depends(get_current_user)):
    return await crud.get_result()















"""

@app.get("/v1/repositories")
def home():
    return "Hello, World!"


@app.get("/v1/entries")
def home():
    return "Hello, World!"

@app.get("/v1/entries/{id}")
def home(id):
    return "Hello, World!"


"""
