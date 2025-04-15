from app.models import UserBase, UserInDb, UserPassword, UserPublic, Booking, Court
from fastapi import APIRouter, Depends, status
from app.database import SessionDep
from typing import Annotated
from portfolio_project.backend.CourtBookingAPI.app.routes import Token, get_current_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException


router = APIRouter()


@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(SessionDep, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='User not found', headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")





@router.post('/user/', response_model=UserPublic)
async def create_user(user: UserInDb, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user




@router.post('/user/me/', response_model=UserPublic)
async def read_user_me(
    current_user: Annotated[UserInDb, Depends(get_current_user)]
):
    return current_user


@router.post('/courts', response_model=Court)
async def create_court(court: Court, session: SessionDep, current_user):
    session.add(court)
    session.commit()
    session.refresh(court)
    return court


@router.post('/booking/', response_model=Booking)
async def create_reserve():
    pass

