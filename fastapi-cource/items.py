from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False
    
class User(BaseModel):
    name: str
    email: str
    password: str
    
class UserResponse(BaseModel):
    message: str
    name: str
    email: str
    
@app.post('/items')
def create_item(payload: Item):
    return {
        'message': 'Item created.',
        'item': payload
    }
    
@app.post("/users", response_model=UserResponse)
def create_user(payload: User):
    return {
        "message": "User created",
        "name": payload.name,
        "email": payload.email
    }
