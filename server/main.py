import sys
from pathlib import Path
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))
sys.path.append('../tools')

from chat import *
from tools import parser

app = FastAPI()

_chat = Chat4me()
_parser = parser.Parser()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/chat/{input}")
def get_output(input: str):
    type, message, data = _chat.getChat(input, [])
    return {
        'type': type,
        'message': message,
        'data': data
    }

@app.get('/report/title/{input}')
def get_title(input: str):
    title = _parser.getReportTitle(input)
    return {
        'title' : title
    }