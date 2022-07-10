from typing import List
from uuid import UUID
import os

from fastapi import APIRouter, Depends, HTTPException

#import src.crud.search as crud

from src.auth.jwthandler import get_current_user
from src.schemas.token import Status


from src.status import status

# Database ##########################################################
# clickhouse

try:
    clickhouse_host = os.environ.get("DATABASE_HOST")

    from clickhouse_driver import Client
    client = Client(clickhouse_host)

    status["database_connection"] = "ok"
except:
    status["database_connection"] = "failure"






# Validation Models (inputs and response) ###########################
from pydantic import BaseModel

# get actual schema for validation
index_fields = client.execute('DESCRIBE nsdf_catalog_index')
allowed_names = [fieldinfo[0] for fieldinfo in index_fields]


class Entry(BaseModel):
    id: str
    name: str
    size: int
    origin_uri: str
    origin_id: str
    replicas: List[str]
    tags: List[str]


class SearchQuery(BaseModel):
    filter: str
    sortBy: str
    descending: bool
    limit: int
    offset: int


class SearchResult(BaseModel):
    rowsNumber: int
    rows: List[Entry]


# Helpers ###########################################################

def results_to_dictionaries(results):
    return list(map(lambda result: dict(zip(allowed_names, result)), results))


# Route Handlers ####################################################
router = APIRouter()

@router.get(
    "/status",
    #dependencies=[Depends(get_current_user)],
)
async def get_status():
    return status


@router.get(
    "/search",
    response_model=List[Entry],
    #dependencies=[Depends(get_current_user)],
)
async def get_search(
    filter: str = "", 
    sortBy: str = "id", 
    descending: bool = False, 
    limit: int = 10, 
    offset: int or None = None,
    rowsPerPage: int or None =  None,
    page: int or None = None
):

    # TODO: Switch this over to an ORM, and then if we keep using clickhouse use e.g., its postgres interface
    # Reasoning:
    # - This code is too complicated to keep safe against SQL injections
    # - ORM offer adapters to many different DBMS (but add a little bit of overhead)


    # sanitize inputs 
    if rowsPerPage is not None:
        limit = rowsPerPage

    if page is not None:
        offset = (page -1) * limit

    if offset is None:
        offset = 0

    order = "ASC"
    if descending:
        order = "DESC"

    # reject any string that is not a column name for 
    if sortBy in allowed_names:
        order_by = sortBy
    else:
        raise HTTPException(status_code=403, detail="Invalid request parameter: sortBy")



    if filter == "":
        results = client.execute(f"""
            SELECT * 
            FROM nsdf_catalog_index
            ORDER BY {order_by} {order}  
            LIMIT {limit}
            OFFSET {offset}
        """)
    else:
        filter = filter.lower()

        results = client.execute(f"""
            SELECT * 
            FROM nsdf_catalog_index 
            WHERE 
                lower(name) LIKE '%{filter}%' OR
                id LIKE '%{filter}%'
            ORDER BY {order_by} {order}  
            LIMIT {limit} 
            OFFSET {offset}
        """)
        # attach names, and convert to dictionary



    return results_to_dictionaries(results)



@router.get(
    "/entry/{entry_id}",
    response_model=Entry,
    #dependencies=[Depends(get_current_user)],
)
async def get_entry(
    entry_id: UUID
):
    query = f"""
        SELECT * FROM nsdf_catalog_index 
        WHERE id LIKE '{entry_id}'
        LIMIT 1
        """
    print(query)
    results = client.execute(query)
    results = list(map(lambda result: dict(zip(allowed_names, result)), results))

    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Entry not found")

    return results[0]





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
