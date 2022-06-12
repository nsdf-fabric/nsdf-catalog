from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# NOTE: import 'from src.routes import users, search' must be after 'Tortoise.init_models'
# https://stackoverflow.com/questions/65531387/tortoise-orm-for-python-no-returns-relations-of-entities-pyndantic-fastapi
from src.routes import auth
from src.routes import search


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(search.router)


@app.get("/")
def home():
    return "Hello, NSDF Data Catalog User!"

