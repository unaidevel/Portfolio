import os
from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine


app = FastAPI()



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event('startup')
def on_startup():
    create_db_and_tables()


class Hola(SQLModel):
    hola: str
    conatras: str
    gs: int

@app.post('/', response_model=Hola)
async def holaa(hola: Hola):
    return f'Su mensaje es {hola}'
