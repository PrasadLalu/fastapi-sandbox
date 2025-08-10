from fastapi import FastAPI
from typing import Optional, List
from sqlmodel import Session, Field, SQLModel
from sqlmodel import create_engine, select
from contextlib import asynccontextmanager

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    is_offer: Optional[bool] = Field(default=False)

sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=True)

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

@app.get('/items', response_model=List[Item])
def list_items():
    with Session(engine) as session:
        items = session.exec(select(Item)).all()
        return items

# Learning@9023