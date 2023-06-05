import sys
from pathlib import Path
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))
sys.path.append('../tools')

from chat import *

app = FastAPI()

chat = Chat4me()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/chat/{input}")
def get_output(input: str):
    type, message, data = chat.getChat(input, [])
    return {
        'type': type,
        'message': message,
        'data': data
    }