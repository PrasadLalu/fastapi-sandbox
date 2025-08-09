from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Payload(BaseModel):
    a: int
    b: int

@app.get('/health-check')
def health_check():
    return 'Healthy...'

@app.post('/add')
def add_numbers(payload: Payload):
    return payload.a + payload.b

@app.post('/subtract')
def subtract_numbers(payload: Payload) -> int:
    return payload.a - payload.b
