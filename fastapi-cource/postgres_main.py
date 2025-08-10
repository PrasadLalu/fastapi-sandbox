import os
from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Optional
from sqlmodel import SQLModel, Field, Session
from sqlmodel import create_engine, select
from contextlib import asynccontextmanager

load_dotenv()

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: bool = False

postgres_url = os.getenv('DATABASE_URL')
engine = create_engine(postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start
    create_db_and_tables()
    yield
    # Shutdown

app = FastAPI(lifespan=lifespan)

@app.post('/items')
def create_item(item: Item):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    
@app.get('/items')
def list_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items
