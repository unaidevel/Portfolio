from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from database import SessionDep
from models import UserBase, UserPublic, UserPassword, UserInDb 
from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from datetime import timedelta, datetime, timezone
import jwt
from typing import Annotated
from jwt.exceptions import InvalidTokenError
from config import settings



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hashed(password):
    pwd_context.hash(password)


def get_user(username: str, session: SessionDep) -> UserInDb | None:
    user = session.exec(UserInDb).filter(UserInDb.username == username).first()
    if user:
        return UserPublic(username=user.username, is_active=user.is_active)
        # user_dict = user.__dict__ #As i saw, if i dont have schemas, its essential to convert the pydantic to dict, and remove the password
        # user_dict.pop('hashed_password', None)
        # return user_dict
    return None



def authenticate_user(username: str, password: str, session:SessionDep):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('username')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception
    return user


