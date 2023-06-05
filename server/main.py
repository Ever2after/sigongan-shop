import sys
from pathlib import Path
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))

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
    print(input)
    output = chat.getChat(input, [])
    return {'output' : output}