from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine
from app.routes import router
app = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

router.register()

@app.on_event('startup')
def on_startup():
    create_db_and_tables()


