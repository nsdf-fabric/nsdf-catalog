from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import Repositories
from src.schemas.repositories import RepositoryOutSchema
from src.schemas.token import Status


async def get_repositories():
    return await RepositoryOutSchema.from_queryset(repositories.all())


async def get_repository(repository_id) -> RepositoryOutSchema:
    return await RepositoryOutSchema.from_queryset_single(repositories.get(id=repository_id))


async def create_repository(repository, current_user) -> RepositoryOutSchema:
    repository_dict = repository.dict(exclude_unset=True)
    repository_dict["user_id"] = current_user.id
    repository_obj = await repositories.create(**repository_dict)
    return await RepositoryOutSchema.from_tortoise_orm(repository_obj)


async def update_repository(repository_id, repository, current_user) -> RepositoryOutSchema:
    try:
        db_repository = await RepositoryOutSchema.from_queryset_single(repositories.get(id=repository_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Repository {repository_id} not found")

    if db_repository.author.id == current_user.id:
        await repositories.filter(id=repository_id).update(**repository.dict(exclude_unset=True))
        return await RepositoryOutSchema.from_queryset_single(repositories.get(id=repository_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_repository(repository_id, current_user) -> Status:
    try:
        db_repository = await RepositoryOutSchema.from_queryset_single(repositories.get(id=repository_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Repository {repository_id} not found")

    if db_repository.author.id == current_user.id:
        deleted_count = await repositories.filter(id=repository_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Repository {repository_id} not found")
        return Status(message=f"Deleted repository {repository_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")
