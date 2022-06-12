from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

#import src.crud.search as crud

from src.auth.jwthandler import get_current_user
from src.schemas.token import Status


router = APIRouter()


@router.get(
    "/search",
    #response_model=List[RepositoryOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_repositories():
    #return await crud.get_results()
    return {}




@router.get(
    "/detail/{entry_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def get_detail(entry_id: int):
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

# Some notes about the conventions used for this API

# Collections use plural names.
# NSDF Data Catalog features only 3 collections:
# - Entries
# - Repositories
# - Users


# Querying/Filtering/Sorting:
# each collection provides some basic functionality for query/adjust the output
# ?query=<query>

# ?<fieldname>=<predicate>

# ?sort=<filedname:{asc/desc}>
# ?offset=<number>
# ?limit=<number>
# ?page=<number>
# ?per_page=<number>

# ?fields=<a list of field names, namespaced fields field1.subfield, comma sperated>

# ?envelope=<true/false/0/1>
# ?embed=<list of field names, similar to fields>


# Nesting of APIS:
# /users                all users
# /users/123            specific user
# /users/123/orders     all orders of users    
# /users/123/orders/12  specific order of user



# Headers that should be anounced:


# At a minimum, include the following headers:
#
#    X-Rate-Limit-Limit - The number of allowed requests in the current period
#    X-Rate-Limit-Remaining - The number of remaining requests in the current period
#    X-Rate-Limit-Reset - The number of seconds left in the current period




# Errors:

# {
#   "error": 1234,
#   "message": "something failed",
#   "detail": "addition details about this error"
# }
