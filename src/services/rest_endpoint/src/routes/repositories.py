from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.repositories as crud
from src.auth.jwthandler import get_current_user
from src.schemas.repositories import RepositoryOutSchema, RepositoryInSchema, UpdateRepository
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/repositories",
    response_model=List[RepositoryOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_repositories():
    return await crud.get_repositories()


@router.get(
    "/repositories/{repository_id}",
    response_model=RepositoryOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_repository(repository_id: int) -> RepositoryOutSchema:
    try:
        return await crud.get_repository(repository_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Repository does not exist",
        )


@router.post(
    "/repositories", response_model=RepositoryOutSchema, dependencies=[Depends(get_current_user)]
)
async def create_repository(
    repository: RepositoryInSchema, current_user: UserOutSchema = Depends(get_current_user)
) -> RepositoryOutSchema:
    return await crud.create_repository(repository, current_user)


@router.patch(
    "/repositories/{repository_id}",
    dependencies=[Depends(get_current_user)],
    response_model=RepositoryOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_repository(
    repository_id: int,
    repository: UpdateRepository,
    current_user: UserOutSchema = Depends(get_current_user),
) -> RepositoryOutSchema:
    return await crud.update_repository(repository_id, repository, current_user)


@router.delete(
    "/repositories/{repository_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_repository(
    repository_id: int, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_repository(repository_id, current_user)

