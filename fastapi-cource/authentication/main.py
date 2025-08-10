from fastapi import FastAPI, HTTPException
from authentication.db import database, metadata, engine
from authentication.schemas import CreateUser, LoginUser
from authentication.models import users
from passlib.context import CryptContext

app = FastAPI()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Create tables on startup
metadata.create_all(engine)

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

@app.post('/register')
async def register_user(user: CreateUser):
    query = users.select().where(users.c.username == user.username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=409, detail='Username already exists')

    hashed_password = pwd_context.hash(user.password)
    query = users.insert().values(username=user.username, password=hashed_password)
    await database.execute(query)
    return {'message': 'User registered successfully'}

@app.post('/login')
async def login_user(user: LoginUser):
    query = users.select().where(users.c.username == user.username)
    db_user = await database.fetch_one(query)
    if not db_user or not pwd_context.verify(user.password, db_user['password']):
        raise HTTPException(status_code=401, detail='Invalid username or password')

    return {'message': 'Login successful'}
