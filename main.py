import json
import requests
from revChatGPT.V3 import Chatbot
from fastapi import FastAPI, Header
from pydantic import BaseModel
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt

app = FastAPI()

chatbot = Chatbot(
    api_key="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")
api = WXAPPAPI(appid="wx82b6e5319c0bb866",
               app_secret="d8a36e72da68319f1eb66afd00a35d7d")


class QuestionItem(BaseModel):
    message: str


class LoginItem(BaseModel):
    code: str
    encrypted_data: str
    iv: str


@app.post("/user/login")
async def login(loginItem: LoginItem):
    return {
        "data": response
    }


@app.post("/chat/ask")
async def ask(questionItem: QuestionItem, auth_key: str = Header(None)):
    if (auth_key == None):
        return {"message": "请先激活"}
    # 取出QuestionItem中的question
    message = questionItem.message
    if (message == None or message == ""):
        return {"message": "请输入问题"}
    return {"message": chatbot.ask(message)}


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    print("Start")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
