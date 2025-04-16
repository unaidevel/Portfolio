from models import UserInDb
from database import SessionDep
from uuid import uuid4
from datetime import date
from passlib.context import CryptContext
from routes.auth import pwd_context
from sqlmodel import select
from sqlmodel import Session
from database import engine


session = Session(engine)



admin_user = UserInDb(
    id=uuid4(),
    username='', #New username
    full_name='Admin User',
    email='', #New email
    role='admin', #The role, can be staff
    birth_date=date(1999, 1, 1),
    is_active=True,
    disabled=False,
    hashed_password=pwd_context.hash('your_secure_password')
)

existing_user = session.exec(select(UserInDb).where(UserInDb.email == admin_user.email)).first()

if not existing_user:
    session.add(admin_user)
    session.commit()
    print('Admin user created')
else:
    print('Admin user already exists')



session.close()