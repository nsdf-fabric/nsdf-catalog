from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Repositories


RepositoryInSchema = pydantic_model_creator(
    Repositories, 
    name="RepositoryIn", 
    exclude=["author_id"], 
    exclude_readonly=True
)

RepositoryOutSchema = pydantic_model_creator(
    Repositories, 
    name="Repository", 
    exclude =[
      "modified_at", "author.password", "author.created_at", "author.modified_at"
    ]
)


class UpdateRepository(BaseModel):
    title: Optional[str]
    content: Optional[str]
