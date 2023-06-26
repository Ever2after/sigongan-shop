import sys
from pathlib import Path
from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio

wd = Path(__file__).parent.parent.resolve()
sys.path.append(str(wd))
sys.path.append('../tools')

from chat import *
from tools import parser

app = FastAPI()

_chat = Chat4me()
_parser = parser.Parser()

class Message(BaseModel):
    content : str


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post('/chat')
async def get_answer(request: Request):
    body = await request.json()
    msgs = body['messages']
    data = body['data']
    message, data = await _chat.getChat(msgs, data)
    return {
        'message': message,
        'data': data
    }

@app.get('/report/title/{input}')
def get_title(input: str):
    title = _parser.getReportTitle(input)
    return {
        'title' : title
    }