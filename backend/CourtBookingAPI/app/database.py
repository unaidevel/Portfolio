import os
from sqlalchemy import create_engine
from fastapi import Depends
from sqlmodel import Session
from typing import Annotated


DATABASE_URL = ''

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

