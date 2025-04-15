from app.models import UserBase, UserInDb, UserPassword, UserPublic, Booking, Court
from fastapi import APIRouter, Depends, status
from app.database import SessionDep
from typing import Annotated
from app.routes.auth import Token, oauth2_scheme, get_current_user, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hashed
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from app.models import TokenRefresh
from sqlmodel import select


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
async def create_user(user: UserPassword, session: SessionDep):
    hashed_password = get_password_hashed(user.password)
    user_in_db = UserInDb(
        username=user.username,
        hashed_password=hashed_password,
        is_active=True,
        role='user'
    )
    session.add(user_in_db)
    session.commit()
    session.refresh(user_in_db)
    return user_in_db


@router.post('/logout/')
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    result = session.exec(select(TokenRefresh).where(TokenRefresh.token == token)).first()
    if result:
        session.delete(result)
        session.commit()
    
    return {"message": "Logged out succesfully"}



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
async def create_reserve(
    booking: Booking,
    session: SessionDep,
    current_user: Annotated[UserInDb, Depends(get_current_user)]
):
    booking.user_id = current_user.id
    session.add(booking)
    session.commit()
    session.refresh(booking)
    return booking


from app.routes.auth import RoleChecker

admin_only = RoleChecker(allowed_roles=['admin'])

@router.post('/admin-only/')
async def admin_only_endpoint(
    current_user: Annotated[UserInDb, Depends(admin_only)]
):
    return {"message": "You have admin access"}
