from fastapi import FastAPI, Body
from revChatGPT.V1 import Chatbot
from starlette.responses import StreamingResponse
import time
from pydantic import BaseModel

app = FastAPI();

chatbot = Chatbot(config={
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJqaWV6aG91d29ya0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZ2VvaXBfY291bnRyeSI6IlVTIn0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci1FdTI3SjhGeWpSa3YyWlhHVUFtMDdHNzQifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAzODQ0MjA1NjQyNzY1OTgzOTQ3IiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY3Njg5MjkwMCwiZXhwIjoxNjc4MTAyNTAwLCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9mZmxpbmVfYWNjZXNzIn0.G9cXqSJGWWELVds0oiWKQFpTyQ7pwpgRYhp6g-iHWSKiQa2TBksZD_gLpxwhrlf3iybpRi7nUoYngJPdZACaqfkzDXgDIAupl828XlKgLzTyZEeD_lYMmg1WXxcG0LfdQliH_H_Mpzzz6TlfVATHgRIsXcuvdWjHBU8kvB6DNWj-u3waM7yPPhRZBrD9fYkuKXQJV-IYoqqwLv6ZMDIFY-kERCFnZK92gSLJeg_d78Svik9sSnAuaP-DOFiNJatKehLcOEjduy2eG3Pjf-DiQQ6KzijWxFN9jYgd8dOOQJwRJL-p7f3ZU6W7iJIXLdppeclgVBUggwCDB_CY3NSJ1w"
})

class Message(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


def generate_events():
    yield "event: message\n"
    yield "data: Hello, world!\n\n"
    time.sleep(1)
    yield "event: message\n"
    yield "data: How are you?\n\n"
    time.sleep(1)
    yield "event: message\n"
    yield "data: Bye!\n\n"
    
def ask(question: str):
    print("Chatbot: ")
    prev_text = ""
    for data in chatbot.ask(
        question,
        "2c6abc5b-99e3-4e93-9a69-aefbe33c07d8"
    ):
        message = data["message"][len(prev_text) :]
        print(message, end="", flush=True)
        prev_text = data["message"]
        yield message

@app.get('/get-conversations')
def get_conversations():
    return chatbot.get_conversations(0, 20);

@app.post("/events")
def events(message: str = Body(..., embed=True)):
      return ask(message)
#     return StreamingResponse(ask(message), media_type="text/event-stream")
       

if __name__ == "__main__":
    print("Starting server...")
    # uvicorn.run(app, host="0.0.0.0", port=8000)
