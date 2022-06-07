from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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




@app.get("/")
def home():
    return "Hello, World!"

@app.get("/v1/repositories")
def home():
    return "Hello, World!"


@app.get("/v1/entries")
def home():
    return "Hello, World!"

@app.get("/v1/entries/{id}")
def home(id):
    return "Hello, World!"
