from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hellow World'}

@app.get('/items/{item_id}')
def find_item(item_id: int):
    return {'Item Id': item_id}

@app.get('/items')
def search_item(query: Optional[int] = None):
    return {'Item Id': query}

@app.get('/products')
def list_products(skip: int = 0, limit: int = 1):
    return { 'skip': skip, 'limit': limit }